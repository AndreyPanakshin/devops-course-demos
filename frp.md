# FRP (Fast Reverse Proxy) - Демо

## Введение

FRP - это высокопроизводительный reverse proxy, который помогает публиковать локальный сервер за NAT или firewall в интернет через сервер с публичным IP.

## Архитектура FRP

- **frps** (FRP Server) - сервер, работающий на машине с публичным IP
- **frpc** (FRP Client) - клиент, работающий на локальной машине за NAT

## Установка FRP

### Скачивание релиза

```bash
# Скачать последний релиз
wget https://github.com/fatedier/frp/releases/download/v0.52.3/frp_0.52.3_linux_amd64.tar.gz

# Распаковать
tar -xzf frp_0.52.3_linux_amd64.tar.gz
cd frp_0.52.3_linux_amd64

# Скопировать исполняемые файлы
sudo cp frps /usr/local/bin/
sudo cp frpc /usr/local/bin/
```

## Настройка FRP Server

### Базовая конфигурация сервера

```toml
# frps.toml
bindPort = 7000
```

### Расширенная конфигурация сервера

```toml
# frps.toml
bindPort = 7000
vhostHTTPPort = 80
vhostHTTPSPort = 443

# Аутентификация
auth.method = "token"
auth.token = "your-secret-token"

# Dashboard
webServer.addr = "0.0.0.0"
webServer.port = 7500
webServer.user = "admin"
webServer.password = "admin123"

# Логирование
log.to = "./frps.log"
log.level = "info"
log.maxDays = 3

# Ограничения
transport.maxPoolCount = 50
```

### Запуск FRP Server

```bash
# Запуск в фоне
./frps -c frps.toml &

# Создание systemd сервиса
sudo tee /etc/systemd/system/frps.service << EOF
[Unit]
Description=FRP Server
After=network.target

[Service]
Type=simple
User=frp
ExecStart=/usr/local/bin/frps -c /etc/frp/frps.toml
Restart=always
RestartSec=20

[Install]
WantedBy=multi-user.target
EOF

# Включение автозапуска
sudo systemctl enable frps
sudo systemctl start frps
```

## Настройка FRP Client

### HTTP проксирование

```toml
# frpc.toml
serverAddr = "your-server-ip"
serverPort = 7000
auth.token = "your-secret-token"

[[proxies]]
name = "web"
type = "http"
localPort = 8080
customDomains = ["example.com"]
```

### HTTPS проксирование

```toml
[[proxies]]
name = "web-secure"
type = "https"
localPort = 8443
customDomains = ["secure.example.com"]
```

### TCP проксирование

```toml
[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000
```

### UDP проксирование

```toml
[[proxies]]
name = "dns"
type = "udp"
localIP = "127.0.0.1"
localPort = 53
remotePort = 6053
```

### STCP (Secure TCP)

```toml
# На клиенте-сервере
[[proxies]]
name = "secret_tcp"
type = "stcp"
secretKey = "abcdefg"
localIP = "127.0.0.1"
localPort = 22

# На клиенте-пользователе
[[visitors]]
name = "secret_tcp_visitor"
type = "stcp"
serverName = "secret_tcp"
secretKey = "abcdefg"
bindAddr = "127.0.0.1"
bindPort = 6000
```

## Продвинутые возможности

### Балансировка нагрузки

```toml
[[proxies]]
name = "web1"
type = "http"
localPort = 8080
customDomains = ["app.example.com"]
group = "web"
groupKey = "123456"

[[proxies]]
name = "web2"
type = "http"
localPort = 8081
customDomains = ["app.example.com"]
group = "web"
groupKey = "123456"
```

### Мониторинг здоровья

```toml
[[proxies]]
name = "web"
type = "http"
localPort = 8080
customDomains = ["example.com"]
healthCheck.type = "http"
healthCheck.timeoutS = 3
healthCheck.maxFailed = 3
healthCheck.intervalS = 10
healthCheck.path = "/health"
```

### Ограничение пропускной способности

```toml
[[proxies]]
name = "ssh"
type = "tcp"
localPort = 22
remotePort = 6000
transport.bandwidthLimit = "1MB"
```

### Сжатие трафика

```toml
[[proxies]]
name = "web"
type = "http"
localPort = 8080
customDomains = ["example.com"]
transport.useCompression = true
```

## Безопасность FRP

### TLS шифрование

```toml
# frps.toml
transport.tls.force = true

# frpc.toml
transport.tls.enable = true
```

### Ограничение портов

```toml
# frps.toml
transport.tcpMux.keepAliveInterval = 60
allowPorts = [
  { start = 2000, end = 3000 },
  { single = 3001 },
  { single = 3003 },
  { start = 4000, end = 50000 }
]
```

### Whitelist клиентов

```toml
# frps.toml
auth.method = "token"
auth.additionalScopes = ["HeartBeats", "NewWorkConns"]
```

## Мониторинг и логирование

### Dashboard сервера

```bash
# Доступ к веб-интерфейсу
http://server-ip:7500
```

### Статистика клиента

```toml
# frpc.toml
webServer.addr = "127.0.0.1"
webServer.port = 7400
webServer.user = "admin"
webServer.password = "admin123"
```

### Логирование

```toml
# Детальное логирование
log.to = "./frpc.log"
log.level = "trace"
log.maxDays = 7

# Отключение логов
log.disablePrintColor = true
```

## Использование с systemd

### Создание пользователя

```bash
sudo useradd -r -s /bin/false frp
sudo mkdir -p /etc/frp
sudo chown frp:frp /etc/frp
```

### Systemd сервис для клиента

```ini
# /etc/systemd/system/frpc.service
[Unit]
Description=FRP Client
After=network.target

[Service]
Type=simple
User=frp
ExecStart=/usr/local/bin/frpc -c /etc/frp/frpc.toml
Restart=always
RestartSec=20

[Install]
WantedBy=multi-user.target
```

## Сценарии использования

### Публикация веб-сервера разработки

```toml
[[proxies]]
name = "dev-web"
type = "http"
localPort = 3000
customDomains = ["dev.myproject.com"]
```

### Удаленный доступ к SSH

```toml
[[proxies]]
name = "home-ssh"
type = "tcp"
localPort = 22
remotePort = 2222
```

### Доступ к базе данных

```toml
[[proxies]]
name = "mysql"
type = "tcp"
localPort = 3306
remotePort = 3307
```

### Файловый сервер

```toml
[[proxies]]
name = "fileserver"
type = "http"
localPort = 8000
customDomains = ["files.example.com"]
```

## Troubleshooting

### Проверка соединения

```bash
# Проверка доступности сервера
telnet server-ip 7000

# Проверка портов
ss -tlnp | grep frp

# Просмотр логов
tail -f frps.log
tail -f frpc.log
```

### Распространенные проблемы

1. **Порт занят**: Проверить доступность портов
2. **Firewall блокирует**: Открыть необходимые порты
3. **DNS не резолвится**: Настроить A-запись домена
4. **Медленное соединение**: Включить сжатие трафика