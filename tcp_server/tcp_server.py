
import sys
import configparser
import getopt
import logging

import global_vars
from logger import logger_worker_init, logger_init

def getConfig(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def get_setting(path, section, setting):
    config = getConfig(path)
    value = config.get(section, setting)

    return value

def main():
    _config_file = "tcp_server.conf"
    _config_section = "server"
    _logger_fname = ""
    _server_host = None
    _server_port = None
    _max_block_size = 1024
    _server_Type = "WialonIPS"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "config=",])
    except:
        print("Undefined option(s).\nUsage: python " + sys.argv[0] + " {-c config_file.conf| --config=config_file.conf}")
        sys.exit(1)

    for oo, a in opts:
        if oo in ("-h", "--help"):
            print("Undefined option(s).\nUsage: python " + sys.argv[0] + " {-c config_file.conf| --config=config_file.conf}")
            sys.exit( 0 )

        elif oo in ("-c", "--config"):
            _config_file = a
        else:
            print("Undefined option(s).\nUsage: python " + sys.argv[0] + " [-c | --config=]config_file ")
            sys.exit(1)

    try: _server_type = get_setting(_config_file, _config_section, "server_type")
    except configparser.NoSectionError as e:  print("section not found: ", str(e))
    except configparser.NoOptionError as e:  print("option not found: ", str(e))
    finally:  pass

    try: _logger_fname = get_setting(_config_file, _config_section, "logger_file")
    except configparser.NoSectionError as e:  print("section not found: ", str(e))
    except configparser.NoOptionError as e:  print("option not found: ", str(e))
    finally:  pass

    try: _server_host = get_setting(_config_file, _config_section, "server_host")
    except configparser.NoSectionError as e:  print("section not found: ", str(e))
    except configparser.NoOptionError as e:  print("option not found: ", str(e))
    finally:  pass

    try: _server_port = get_setting(_config_file, _config_section, "server_port")
    except configparser.NoSectionError as e:  print("section not found: ", str(e))
    except configparser.NoOptionError as e:  print("option not found: ", str(e))
    finally:  pass

    try: _max_block_size = int(get_setting(_config_file, _config_section, "max_block_size"))
    except configparser.NoSectionError as e:  print("section not found: ", str(e))
    except configparser.NoOptionError as e:  print("option not found: ", str(e))
    finally:  pass

    logger_fname = _logger_fname
    q_log_listener, global_vars.logger_queue = logger_init(logger_fname)

    global_vars.main_logger = logging

    print("_server_type = ", _server_type)

    if _server_type == "WialonIPS":
        from TCPserverWialonIPS import TCPserverWialonIPS

        tcp_server = TCPserverWialonIPS(
            server_host=_server_host,
            server_port=_server_port,
            max_block_size=_max_block_size,
        )
    else:
        from TCPserverCustom import TCPserverCustom

        tcp_server = TCPserverCustom(
            server_host=_server_host,
            server_port=_server_port,
            max_block_size=_max_block_size,
        )

    tcp_server.run_server()

if __name__ == "__main__":
    main()
