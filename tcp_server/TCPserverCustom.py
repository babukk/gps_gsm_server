
import asyncio
from time import sleep
import libscrc

import global_vars
from db_utils import Transport, TransportData, CustomUser


class MyException(Exception):
    pass


class TCPserverCustom(asyncio.Protocol):

    def __init__(self, **kwargs):

        # global_vars.main_logger.info("test server init.")

        self.server_host = kwargs.get('server_host')
        self.server_port = kwargs.get('server_port')
        self.max_block_size = kwargs.get('max_block_size')
        self.db_transport = Transport()
        self.db_transport_data = TransportDataCustom()
        self.db_custom_user = CustomUser()
        self.timeout = 5 * 60

    def _timeout(self):
        # print("=================== timeout =================")
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

    def processRequest(self, req_msg, logged_user):
        msgs = req_msg.split(';')

        print("processRequest: ", msgs)

        if msgs[0] == ">000L":
            # print("------------ check_login ----------")
            user_id, err_msg = self.db_custom_user.check_login(msgs[1], msgs[2])
            if user_id:
                print('user_id = ', user_id)
                reply = "000L;OK;0"
                crc16 = format(libscrc.modbus(reply.encode()), '04x')
                return user_id, "<" + reply + ";" + crc16 + '\n', err_msg
            else:
                # print('------ bad login or password --------')
                reply = "000L;Err;2"
                crc16 = format(libscrc.modbus(reply.encode()), '04x')
                return None, "<" + reply + ";" + crc16 + '\n', err_msg

        elif msgs[0] == ">00SD":
            # print("----------->>> transport_data ----> logged_user = ", logged_user)
            if logged_user:
                dt = msgs[1]
                tm = msgs[2]
                lat = msgs[3]
                lon = msgs[4]
                course = msgs[5]
                speed = msgs[6]
                altitude = msgs[7]
                sats = msgs[8]
                flags1 = msgs[9]
                crc16 = msgs[10]
                result, err_msg = self.db_transport_data.save_data(logged_user, dt, tm, lat, lon, course, speed, altitude, sats, flags1)
                if result:
                    # print('---- data saved ----')
                    reply = "00SD;OK;0"
                    crc16 = format(libscrc.modbus(reply.encode()), '04x')
                    return logged_user, "<" + reply + '\n', err_msg
                else:
                    # print('---- data nit saved - error ----')
                    reply = "00SD;Err;1"
                    crc16 = format(libscrc.modbus(reply.encode()), '04x')
                    return logged_user, "<" + reply + '\n', err_msg
            else:
                # print('--- user not logged ----')
                reply = "00SD;Err;3"
                crc16 = format(libscrc.modbus(reply.encode()), '04x')
                global_vars.main_logger.error("Error: not logged.")
                return logged_user, "<" + reply + '\n', None
        else:
            reply = "00SD;Err;4"
            crc16 = format(libscrc.modbus(reply.encode()), '04x')
            return logged_user, "<" + reply + '\n', None

    async def handle_client(self, reader, writer):
        request = None

        logged_user = None

        while True:
            try:
                request = (await reader.read(self.max_block_size)).decode('utf8')
            except Exception as e:
                print("============= Exception (1) ==========")
                global_vars.main_logger.error("exception: " + str(e))
                continue

            if request:
                request = str(request)
                global_vars.main_logger.info(str(request))
                request = request.rstrip()
                try:
                    logged_user, reply, err_msg = self.processRequest(request, logged_user)
                except MyException as e:
                    print("============= raise MyException (2) ==========")
                    break
                except Exception as e:
                    print("============= Exception (2) ==========")
                    break
                if err_msg:
                    global_vars.main_logger.error(str(err_msg))
                if not logged_user:
                    # print("--------------------- >>> Not logged user ---- >>> exit ---------")
                    break
                # print("handle_client --------------------->: reply = ", reply)
                try:
                    writer.write(reply.encode('utf8'))
                    global_vars.main_logger.info("OUTPUT: " + str(reply))
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

        return False
