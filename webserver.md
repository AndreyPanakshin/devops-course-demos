# Веб-сервер - Демо

## Введение

Веб-сервер - это программа, которая принимает HTTP-запросы и возвращает HTTP-ответы с веб-страницами или другими ресурсами.

## Простой HTTP сервер на Python
https://docs.python.org/3/library/http.server.html

### Создание базового сервера

```bash
cat > server.py << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler

class HelloWorldHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('Hello World'.encode('utf-8'))

def start_server(port=8000):
    server = HTTPServer(('0.0.0.0', port), HelloWorldHandler)
    print(f"Сервер запущен на http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == '__main__':
    start_server()
EOF

python3 server.py
```


### Запуск через командную строку
https://docs.python.org/3/library/http.server.html#http.server.SimpleHTTPRequestHandler

```bash
# Python 3
python -m http.server 8000
```

## Nginx как веб-сервер

### Установка

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx
```

### Базовая конфигурация

```nginx configuration
# /etc/nginx/nginx.conf
user www-data;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;
include /etc/nginx/modules-enabled/*.conf;

events {
	worker_connections 768;
	# multi_accept on;
}

http {

	##
	# Basic Settings
	##

	sendfile on;
	tcp_nopush on;
	types_hash_max_size 2048;
	# server_tokens off;

	# server_names_hash_bucket_size 64;
	# server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	##
	# SSL Settings
	##

	ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;

	##
	# Logging Settings
	##

	access_log /var/log/nginx/access.log;

	##
	# Gzip Settings
	##

	gzip on;

	# gzip_vary on;
	# gzip_proxied any;
	# gzip_comp_level 6;
	# gzip_buffers 16 8k;
	# gzip_http_version 1.1;
	# gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

	##
	# Virtual Host Configs
	##

	include /etc/nginx/conf.d/*.conf;
	include /etc/nginx/sites-enabled/*;
}


#mail {
#	# See sample authentication script at:
#	# http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
#
#	# auth_http localhost/auth.php;
#	# pop3_capabilities "TOP" "USER";
#	# imap_capabilities "IMAP4rev1" "UIDPLUS";
#
#	server {
#		listen     localhost:110;
#		protocol   pop3;
#		proxy      on;
#	}
#
#	server {
#		listen     localhost:143;
#		protocol   imap;
#		proxy      on;
#	}
#}
```

```bash
sudo tee /etc/nginx/sites-available/demo > /dev/null << 'EOF'
server {
    listen 80;
    server_name default_server;
    root /var/www/html;
    index index.html index.htm;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

sudo mkdir -p /var/www/html
sudo tee /var/www/html/index.html > /dev/null << 'EOF'
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Nginx Demo</title>
</head>
<body>
  <h1>🚀 Nginx работает!</h1>
  <p>Это основная демо-страница</p>
</body>
</html>
EOF

sudo ln -s /etc/nginx/sites-available/demo /etc/nginx/sites-enabled/demo
```

### Управление службой

```bash
# Запуск
sudo systemctl start nginx

# Остановка
sudo systemctl stop nginx

# Перезагрузка конфигурации
sudo nginx -s reload

# Проверка конфигурации
sudo nginx -t
```

### Логи

```bash
# Nginx логи
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Apache логи
tail -f /var/log/apache2/access.log
tail -f /var/log/apache2/error.log
```

### Несколько сайтов на одном порту

```bash
sudo tee /etc/nginx/sites-available/demo > /dev/null << 'EOF'
server {
    listen 80;
    server_name first.demo.local;
    root /var/www/html;
    index index.html index.htm;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

sudo tee /etc/nginx/sites-available/demo-second > /dev/null << 'EOF'
server {
    listen 80;
    server_name second.demo.local;
    root /var/www/html-second;
    index index.html index.htm;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

sudo mkdir -p /var/www/html-second
sudo tee /var/www/html-second/index.html > /dev/null << 'EOF'
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Nginx Demo</title>
</head>
<body>
  <h1>🚀 Nginx работает!</h1>
  <p>Это другая демо-страница</p>
</body>
</html>
EOF

sudo ln -s /etc/nginx/sites-available/demo-second /etc/nginx/sites-enabled/demo-second
```

```bash
sudo cp /etc/hosts /etc/hosts.bkp

sudo tee -a /etc/hosts > /dev/null << 'EOF'
192.168.56.103 first.demo.local
192.168.56.103 second.demo.local
EOF
```


### Curl

```
curl -v 192.168.56.103
curl -H "Host: second.demo.local" 192.168.56.103
```
