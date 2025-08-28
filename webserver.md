# Веб-сервер - Демо

## Введение

Веб-сервер - это программа, которая принимает HTTP-запросы и возвращает HTTP-ответы с веб-страницами или другими ресурсами.

## Простой HTTP сервер на Python

### Создание базового сервера

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

def start_server(port=8000, directory='.'):
    os.chdir(directory)
    server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    print(f"Сервер запущен на http://localhost:{port}")
    server.serve_forever()

if __name__ == '__main__':
    start_server()
```

### Запуск через командную строку

```bash
# Python 3
python -m http.server 8000

# Указание директории
python -m http.server 8000 --directory /path/to/files
```

## Nginx как веб-сервер

### Установка

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx
```

### Базовая конфигурация

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html index.htm;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
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

## Apache HTTP Server

### Установка

```bash
# Ubuntu/Debian
sudo apt install apache2
```

### Базовая конфигурация

```apache
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/html
    
    <Directory /var/www/html>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```


## Мониторинг веб-сервера

### Проверка состояния

```bash
# Проверка порта
netstat -tlnp | grep :80

# Проверка процесса
ps aux | grep nginx

# Тестирование HTTP ответа
curl -I http://localhost:80
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

