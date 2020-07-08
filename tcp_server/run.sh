#! /bin/sh
#--------------------------------------------------------------------------------------------------------------------------------------------

SERVER_DIR="/home/testersvr/projects/gps_gsm_server_v2"

if [ ! -d ${SERVER_DIR}/.venv3 ]; then
    virtualenv -p `which python3` ${SERVER_DIR}/.venv3/
    . ${SERVER_DIR}/.venv3/bin/activate
    pip install --upgrade pip
    pip install -r ../requirements.txt
    pip freeze
else
    . ${SERVER_DIR}/.venv3/bin/activate
fi

if [ ! -d ./logs ]; then
    mkdir .logs
fi

export DJANGO_PROJECT_PATH="../"

# python 1.py

python tcp_server.py --config=tcp_server.conf

deactivate
