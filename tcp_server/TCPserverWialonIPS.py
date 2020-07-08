
import asyncio
from time import sleep
import datetime
import libscrc

import global_vars
from db_utils import TransportWialon, TransportDataCustom, TransportDataWialon, CustomUser


class MyException(Exception):
    pass


class TCPserverWialonIPS(asyncio.Protocol):

    def __init__(self, **kwargs):

        # global_vars.main_logger.info("test server init.")

        self.server_host = kwargs.get('server_host')
        self.server_port = kwargs.get('server_port')
        self.max_block_size = kwargs.get('max_block_size')
        self.db_transport = TransportWialon()
        self.db_transport_data = TransportDataWialon()
        self.db_custom_user = CustomUser()
        self.timeout = 5 * 60

    def _timeout(self):
        self.timeout_handle = self.loop.call_later(
            self.timeout, self._timeout,
        )
        # raise MyException("e")

    def run_server(self):
        self.loop = asyncio.get_event_loop()
        self.timeout_handle = self.loop.call_later(
            self.timeout, self._timeout,
        )
        self.loop.create_task(asyncio.start_server(self.handle_client, self.server_host, self.server_port))
        self.loop.run_forever()

    def processDataPacks(self, logged_device, packets):
        for pack in packets:
            print("pack = ", pack)
            if len(pack) <= 4:
                print("------------- CRC -----")
                continue

            dd = pack.split(';')
            if len(dd) > 15:
                #- расширенный пакет данных
                dt = dd[0]
                tm = dd[1]
                lat1 = dd[2]
                lat2 = dd[3]
                lon1 = dd[4]
                lon2 = dd[5]
                speed = dd[6]
                course = dd[7]
                alt = dd[8]
                sats = dd[9]
            else:
                #- сокращенный пакет данных
                dt = dd[0]
                tm = dd[1]
                lat1 = dd[2]
                lat2 = dd[3]
                lon1 = dd[4]
                lon2 = dd[5]
                speed = dd[6]
                course = dd[7]
                alt = dd[8]
                sats = dd[9]

            if dt == "NA" and tm == "NA":
                dt = None
            else:
                dt = datetime.datetime.strptime(dt + " " + tm, "%d%m%y %H%M%S")
            print("---> dt = ", dt)

            if lat1 == "NA":
                lat = None
            else:
                lat = float(lat1[0:2]) + float(lat1[2:7]) / 60

            if lon1 == "NA":
                lon = None
            else:
                lon = float(lon1[0:3]) + float(lon1[3:7]) / 60

            print("---> lat = ", lat)
            print("---> lon = ", lon)

            result, err_msg = self.db_transport_data.save_data(logged_device, dt, lat, lon, course, speed, alt, sats)

        return

    def processRequest(self, req_msg, logged_device):
        print("req_msg = ", req_msg)
        msgs = req_msg.split('#')
        err_msg = ""

        # DEBUG ---------------------------
        # device_id = 1
        # logged_device = device_id

        if msgs[1] == "L":
            imei = msgs[2].split(';')[1]
            print("------------------ LOGIN : IMEI = ", imei)
            device_id, err_msg = self.db_transport.check_login(imei)
            print("device_id = ", device_id)
            if device_id:
                reply = "#AL#1"
                return device_id, reply + '\r\n', err_msg
            else:
                reply = "#AL#0"
                return None, reply + '\r\n', err_msg

        elif msgs[1] == "D":
            reply = "#AD#1"
            return logged_device, reply + '\r\n', err_msg

        elif msgs[1] == "M":
            reply = "#AM#1"
            return logged_device, reply + '\r\n', err_msg

        elif msgs[1] == "P":
            reply = "#AP#1"
            return logged_device, reply + '\r\n', err_msg

        elif msgs[1] == "B":
            data_packs = msgs[2].split('|')
            self.processDataPacks(logged_device, data_packs)
            n_packs = len(data_packs) - 1
            reply = "#AB#" + str(n_packs)
            return logged_device, reply + '\r\n', err_msg

        else:
            reply = ""
            return logged_device, reply + '\r\n', None

    async def handle_client(self, reader, writer):
        request = ""
        tmp_request = ""

        logged_device = None
        global_vars.main_logger.info("Socket opened.")

        while True:
            try:
                tmp_request = (await reader.read(self.max_block_size)).decode('utf8')
            except Exception as e:
                print("============= Exception (1) ==========")
                global_vars.main_logger.error("exception: " + str(e))
                break

            if tmp_request and (len(tmp_request) > 0):
                if "\r\n" not in tmp_request:
                    request += tmp_request
                    continue
                else:
                    request += tmp_request

                request = str(request)
                global_vars.main_logger.info("Message from tracker: " + str(request))
                request = request.rstrip()

                logged_device, reply, err_msg = self.processRequest(request, logged_device)
                request = ""

                """
                try:
                    logged_device, reply, err_msg = self.processRequest(request, logged_device)
                    request = ""
                except MyException as e:
                    print("============= raise MyException (2) ==========")
                    break
                except Exception as e:
                    print("============= Exception (2) ==========", str(e))
                    global_vars.main_logger.error("exception (2): " + str(e))
                    break
                """
                if err_msg:
                    global_vars.main_logger.error(str(err_msg))
                if not logged_device:
                    # print("--------------------- >>> Not logged device ---- >>> exit ---------")
                    break
                # print("handle_client ------------- send -------->: reply = ", reply)

                try:
                    writer.write(reply.encode('utf8'))
                    global_vars.main_logger.info("OUT to tracker: " + str(reply))
                except Exception as e:
                    global_vars.main_logger.error("exception (0): " + str(e))
                # global_vars.main_logger.info("data =" + str(request) + "|")
                # break
            else:
                sleep(0.3)
                break

            try:
                await writer.drain()
            except ConnectionResetError as e:
                global_vars.main_logger.error("exception (1): " + str(e))
                sleep(0.5)
                break
            except BrokenPipeError as e:
                global_vars.main_logger.error("exception (2): " + str(e))
                sleep(0.5)
                break

            # print('------------- waiting ------------')
            # sleep(1)

        writer.close()
        global_vars.main_logger.info("Socket closed.")

        return False
