# Прокси-сервер - Демо

## Введение

Прокси-сервер - сервер-посредник между клиентом и сервером

## Типы прокси-серверов

### Forward Proxy (Прямой прокси)
- Клиент подключается к прокси для доступа к внешним ресурсам
- Скрывает клиента от сервера

### Reverse Proxy (Обратный прокси)
- Прокси принимает запросы от клиентов и перенаправляет их на внутренние серверы
- Скрывает серверы от клиентов

## Nginx как прокси-сервер

### Backend веб-сервер

```bash
tee backend-headers.py > /dev/null << 'EOF'
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        headers_text = "HTTP Request Headers:\n"
        headers_text += f"Method: {self.command}\n"
        headers_text += f"Path: {self.path}\n"
        headers_text += f"Version: {self.request_version}\n\n"
        
        for header, value in self.headers.items():
            headers_text += f"{header}: {value}\n"
        
        self.wfile.write(headers_text.encode('utf-8'))

if __name__ == '__main__':
    port = int(sys.argv[1])
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f"Backend server starting on port {port}...")
    server.serve_forever()
EOF

tee backend-echo.py > /dev/null << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

class HelloWorldHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('Hello World'.encode('utf-8'))

def start_server():
    port = int(sys.argv[1])
    server = HTTPServer(('localhost', port), HelloWorldHandler)
    print(f"Backend server starting on port {port}...")
    server.serve_forever()

if __name__ == '__main__':
    start_server()
EOF

tmux new -d -s b1 "python3 backend-headers.py 8808"
tmux new -d -s b2 "python3 backend-echo.py 8809"
tmux attach -t b1
```

### Reverse Proxy конфигурация

#### Маршрутизация по портам
```bash
sudo tee /etc/nginx/sites-available/proxy-ports > /dev/null << 'EOF'
server {
    listen 8001;
    location / {
        proxy_pass http://localhost:8808;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 8002;
    location / {
        proxy_pass http://localhost:8809;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/proxy-ports /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

#### Маршрутизация по пути
```bash
sudo tee /etc/nginx/sites-available/proxy-path > /dev/null << 'EOF'
server {
    listen 8080;
    
    location /headers {
        proxy_pass http://localhost:8808;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /echo {
        proxy_pass http://localhost:8809;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/proxy-path /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

#### Маршрутизация по хост нейму
```bash
sudo tee /etc/nginx/sites-available/proxy-host > /dev/null << 'EOF'
server {
    listen 9898;
    server_name headers.local;
    
    location / {
        proxy_pass http://localhost:8808;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 9898;
    server_name echo.local;
    
    location / {
        proxy_pass http://localhost:8809;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/proxy-host /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

```bash
sudo cp /etc/hosts /etc/hosts.bkp.$(date +%FT%T.%3N)

sudo tee -a /etc/hosts > /dev/null << 'EOF'
192.168.56.103 headers.local
192.168.56.103 echo.local
EOF

curl headers.local:9898
```