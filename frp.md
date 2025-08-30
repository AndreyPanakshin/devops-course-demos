# FRP (Fast Reverse Proxy) - Демо

FRP - обратный прокси сервер с поддержкой туннелирования до клиентов
https://github.com/fatedier/frp/

- **frps** (FRP Server) - сервер, работающий на машине с публичным IP
- **frpc** (FRP Client) - клиент, работающий на локальной машине за NAT

### Wildcard DNS запись для course.prafdin.ru

```bash
dig blablabla.course.prafdin.ru
```

### Настройка frps
```toml
[common]
bind_port = 7000

authentication_method = "token"
token = "tokentoken"

vhost_http_port = 80
vhost_https_port = 8443
```

### Запуск frpc

```bash
wget https://github.com/fatedier/frp/releases/download/v0.52.3/frp_0.52.3_linux_amd64.tar.gz

tar -xzf frp_0.52.3_linux_amd64.tar.gz
cd frp_0.52.3_linux_amd64

tee frpc.toml > /dev/null << 'EOF'
serverAddr = "course.prafdin.ru"
serverPort = 7000

auth.method = "token"
auth.token = "tokentoken"

[[proxies]]
name = "p1"
type = "http"
localIP = "127.0.0.1"
localPort = 8080
customDomains = ["p1.course.prafdin.ru"]

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 2222
EOF

tmux new -d -s frpc "frpc -c frpc.toml"
tmux attach -t frpc

cd ~ 
tmux new -d -s b1 "python3 backend-echo.py 8080"

curl p1.course.prafdin.ru

ssh -p 2222 user@course.prafdin.ru
```