# Туннелирование - Демо

## Введение

Туннелирование - это процесс инкапсуляции одного протокола внутри другого для создания безопасного или скрытого канала связи через сеть.

## SSH Туннели

### Local Port Forwarding (Локальное перенаправление портов)

```bash
# Перенаправление локального порта 8080 на удаленный сервер:80 через SSH
ssh -L 8080:target-server:80 user@jump-server

# Доступ к базе данных через промежуточный сервер
ssh -L 5432:database-server:5432 user@bastion-host
```

### Remote Port Forwarding (Удаленное перенаправление портов)

```bash
# Открытие локального порта 3000 на удаленном сервере
ssh -R 8080:localhost:3000 user@remote-server

# Обратный туннель для доступа к локальному веб-серверу
ssh -R 80:localhost:8000 user@public-server
```

### Dynamic Port Forwarding (SOCKS прокси)

```bash
# Создание SOCKS прокси на порту 1080
ssh -D 1080 user@remote-server

# Использование с curl
curl --socks5 localhost:1080 http://example.com
```

### Постоянные SSH туннели

```bash
# Создание туннеля в фоне с автоматическим переподключением
ssh -f -N -L 8080:target:80 -o ServerAliveInterval=60 -o ServerAliveCountMax=3 user@server

# Использование autossh для надежности
autossh -f -N -L 8080:target:80 user@server
```

## OpenVPN

### Установка сервера

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openvpn easy-rsa

# Инициализация PKI
make-cadir ~/openvpn-ca
cd ~/openvpn-ca
source vars
./clean-all
./build-ca
./build-key-server server
./build-dh
```

### Конфигурация сервера

```
# /etc/openvpn/server.conf
port 1194
proto udp
dev tun

ca ca.crt
cert server.crt
key server.key
dh dh2048.pem

server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt

push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"

keepalive 10 120
comp-lzo
user nobody
group nobody
persist-key
persist-tun

status openvpn-status.log
verb 3
```

### Конфигурация клиента

```
# client.ovpn
client
dev tun
proto udp

remote your-server-ip 1194
resolv-retry infinite
nobind
persist-key
persist-tun

ca ca.crt
cert client.crt
key client.key

comp-lzo
verb 3
```

## WireGuard

### Установка

```bash
# Ubuntu
sudo apt install wireguard

# Генерация ключей
wg genkey | tee privatekey | wg pubkey > publickey
```

### Конфигурация сервера

```ini
# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = SERVER_PRIVATE_KEY
Address = 10.0.0.1/24
ListenPort = 51820

# Клиент 1
[Peer]
PublicKey = CLIENT1_PUBLIC_KEY
AllowedIPs = 10.0.0.2/32

# Клиент 2
[Peer]
PublicKey = CLIENT2_PUBLIC_KEY
AllowedIPs = 10.0.0.3/32
```

### Конфигурация клиента

```ini
# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = CLIENT_PRIVATE_KEY
Address = 10.0.0.2/24
DNS = 8.8.8.8

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = server-ip:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

### Управление WireGuard

```bash
# Запуск интерфейса
sudo wg-quick up wg0

# Остановка интерфейса
sudo wg-quick down wg0

# Просмотр статуса
sudo wg show

# Автозапуск
sudo systemctl enable wg-quick@wg0
```

## ngrok

### Установка и использование

```bash
# Установка
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Аутентификация
ngrok authtoken YOUR_AUTH_TOKEN

# Туннель для HTTP сервера
ngrok http 8080

# Туннель для TCP порта
ngrok tcp 22

# Кастомный поддомен
ngrok http -subdomain=myapp 8080
```

## Локальный туннель с socat

### TCP туннель

```bash
# Перенаправление порта 8080 на удаленный сервер:80
socat TCP-LISTEN:8080,fork TCP:remote-server:80

# Туннель через UNIX сокет
socat TCP-LISTEN:3306,fork UNIX-CONNECT:/var/run/mysqld/mysqld.sock
```

## stunnel (SSL туннель)

### Конфигурация сервера

```ini
# /etc/stunnel/stunnel.conf
[mysql]
accept = 3307
connect = 3306
cert = /path/to/cert.pem
key = /path/to/key.pem
```

### Конфигурация клиента

```ini
# /etc/stunnel/stunnel.conf
[mysql]
client = yes
accept = 3306
connect = server:3307
```

## Мониторинг туннелей

### SSH туннели

```bash
# Просмотр активных SSH соединений
ss -tlnp | grep ssh

# Проверка SSH процессов
ps aux | grep ssh

# Логи SSH
sudo tail -f /var/log/auth.log
```

### VPN мониторинг

```bash
# OpenVPN статус
sudo systemctl status openvpn@server

# WireGuard статистика
sudo wg show

# Проверка VPN интерфейсов
ip addr show tun0
ip addr show wg0
```

## Безопасность туннелей

### SSH безопасность

```bash
# Использование ключей вместо паролей
ssh-keygen -t ed25519 -C "tunnel-key"
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server

# Ограничение команд в authorized_keys
command="echo 'Only tunneling allowed'",no-pty,no-agent-forwarding ssh-ed25519 AAAAC3...
```

### Firewall правила

```bash
# Разрешение только VPN трафика
sudo ufw allow 51820/udp  # WireGuard
sudo ufw allow 1194/udp   # OpenVPN

# Ограничение SSH доступа
sudo ufw allow from 192.168.1.0/24 to any port 22
```