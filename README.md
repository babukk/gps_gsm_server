```
Настройка для запуска в production-mode (для Ubuntu/Debian)

Устанавливаем python-пакет gunicorn:
sudo apt install gunicorn

В файле /home/testersvr/projects/gps_gsm_server_v2/gpsserver/local_settings.py
меняем
DEBUG = True
на 
DEBUG = Falee


Настраиваем запуск через systemd:

-------------------------------- файл /etc/systemd/system/gpsgsmserver.socket
sudo nano /etc/systemd/system/gpsgsmserver.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gpsgsmserver.sock

[Install]
WantedBy=sockets.target
-------------------------------- конец файла /etc/systemd/system/gpsgsmserver.socket


sudo nano /etc/systemd/system/gpsgsmserver.service
Параметр workers определяется так: количество CPU + 1.
-------------------------------- файл /etc/systemd/system/gpsgsmserver.service
[Unit]
Description=gpsgsmserver daemon
Requires=gpsgsmserver.socket
After=network.target

[Service]
User=testersvr
Group=testersvr
WorkingDirectory=/home/testersvr/projects/gps_gsm_server_v2
ExecStart=/home/testersvr/projects/gps_gsm_server_v2/.venv3/bin/gunicorn \
          --access-logfile - \
          --workers 2 \
          --bind unix:/run/gpsgsmserver.sock \
          gpsserver.wsgi:application

[Install]
WantedBy=multi-user.target
-------------------------------- конец файла /etc/systemd/system/gpsgsmserver.service


sudo systemctl start gpsgsmserver.socket
sudo systemctl enable gpsgsmserver.socket


Проверяем ошибки (если есть):
sudo journalctl -u gpsgsmserver.socket

Перезапускаем:
sudo systemctl daemon-reload
sudo systemctl restart gpsgsmserver




Настройка NGINX

Создаём файл:
sudo nano /etc/nginx/sites-available/gpsgsmserver
-------------------------------- файл /etc/nginx/sites-available/gpsgsmserver
server {
    # Если нет домена и используется IP-адрес сервера, то потребуется назначить определенный номер порта:
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/testersvr/projects/gps_gsm_server_v2/static;
    }

    # пока не используется:
    # location /media/ {
    #     alias /home/testersvr/projects/gps_gsm_server_v2/media;
    # }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gpsgsmserver.sock;
    }
}
-------------------------------- конец файла /etc/nginx/sites-available/gpsgsmserver

Создаём symlink:
sudo ln -sf /etc/nginx/sites-available/gpsgsmserver /etc/nginx/sites-enabled/gpsgsmserver

Перезапускаем NGINX:
sudo systemctl restart nginx



Документация по API - в формате Swagger:
/swagger

Пример получения token'а для авторизации:
curl -i http://localhost:8888/api/token/ --header "Content-Type: application/json" --data '{"login":"api_user", "password":"xxxxxxx"}'

HTTP/1.1 200 OK
Date: Sun, 14 Jun 2020 08:48:28 GMT
Server: WSGIServer/0.2 CPython/3.5.2
Content-Type: application/json
Allow: POST, OPTIONS
Vary: Accept
Content-Length: 438
X-Frame-Options: SAMEORIGIN

{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTIyMTA5MDgsInVzZXJfaWQiOjIsInRva2VuX3R5cGUiOiJyZWZyZXNoIiwianRpIjoiMmVjMTQ4OWMzMTk4NDMzMzhmZmRkNDFlNWM1YWY4Y2MifQ.yAyLf6Gq9l-9S3tCj3Uj16jwaaTYOoLhbA3TFwvzx7c","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTIxMjQ4MDgsInVzZXJfaWQiOjIsInRva2VuX3R5cGUiOiJhY2Nlc3MiLCJqdGkiOiI2NmZkY2IwMDY2YjQ0M2M1OWY4NjkyNjgyNjAwNGY4MCJ9.XcR-UEf9ZC83pvFgnmJnT-tws-Y1_Yn-m4G5_XpmnpU"}


```
