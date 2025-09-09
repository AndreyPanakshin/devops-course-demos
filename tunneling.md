# Туннелирование - Демо

## Введение

Туннелирование - это процесс инкапсуляции одного протокола внутри другого для создания безопасного или скрытого канала связи через сеть.

## SSH Туннели
https://ekb.it01.su/posts/ssh-tunnelirovaniiu-i-pereadresatsiia-portov

### Local Port Forwarding

```bash
ssh -4 -L 8191:localhost:8809 user@192.168.56.103
```

### Remote Port Forwarding

```bash
ssh -R 0.0.0.0:8080:localhost:8809 root@course.prafdin.ru
```

### Dynamic Port Forwarding
```bash
ssh -D 127.0.0.1:8018 root@course.prafdin.ru
curl --socks5 127.0.0.1:8018 http://ifconfig.me
```
