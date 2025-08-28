# Прокси-сервер - Демо

## Введение

Прокси-сервер - это промежуточный сервер, который выступает посредником между клиентом и целевым сервером. Прокси может кэшировать данные, фильтровать трафик, обеспечивать безопасность и балансировать нагрузку.

## Типы прокси-серверов

### Forward Proxy (Прямой прокси)
- Клиент подключается к прокси для доступа к внешним ресурсам
- Скрывает клиента от сервера

### Reverse Proxy (Обратный прокси)
- Прокси принимает запросы от клиентов и перенаправляет их на внутренние серверы
- Скрывает серверы от клиентов

## Nginx как прокси-сервер

### Reverse Proxy конфигурация

```nginx
server {
    listen 80;
    server_name proxy.example.com;
    
    location / {
        proxy_pass http://backend-server:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Балансировка нагрузки

```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
    }
}
```

### Кэширование

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g 
                 inactive=60m use_temp_path=off;

server {
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 1h;
        proxy_cache_valid 404 1m;
        proxy_pass http://backend;
    }
}
```

## HAProxy

### Установка

```bash
# Ubuntu/Debian
sudo apt install haproxy

# CentOS/RHEL
sudo yum install haproxy
```

### Базовая конфигурация

```haproxy
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend web_frontend
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
    server web3 192.168.1.12:80 check
```

## Squid Proxy

### Установка

```bash
# Ubuntu/Debian
sudo apt install squid

# CentOS/RHEL
sudo yum install squid
```

### Базовая конфигурация

```squid
# /etc/squid/squid.conf
http_port 3128
acl localnet src 192.168.1.0/24
http_access allow localnet
http_access deny all

# Кэширование
cache_dir ufs /var/spool/squid 100 16 256
maximum_object_size 4096 KB
```

## SSL Termination

### Nginx SSL Proxy

```nginx
server {
    listen 443 ssl;
    server_name secure.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://backend:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Мониторинг прокси

### Nginx статистика

```nginx
server {
    listen 8080;
    location /nginx_status {
        stub_status;
        allow 127.0.0.1;
        deny all;
    }
}
```

### HAProxy статистика

```haproxy
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
```

## Тестирование прокси

### Проверка работы

```bash
# Тест через прокси
curl -x http://proxy:3128 http://example.com

# Проверка заголовков
curl -H "X-Forwarded-For: 1.2.3.4" http://proxy/

# Тест балансировки
for i in {1..10}; do curl http://proxy/; done
```