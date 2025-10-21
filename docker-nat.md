## Access to internet (SNAT)

```bash
sudo tcpdump -i enp0s9 icmp -nn -s 0 -vv -X -tttt
```

```bash
docker run -it --rm nginx:alpine bash
ping -c 1 192.168.57.5
```

## Port publishing (DNAT)

```bash
docker run -d --rm -p 8282:80 --name nginx_p1 nginx:alpine

docker network inspect bridge | grep nginx_p1 -A 3
curl 172.17.0.6:80

curl localhost:8282
curl 192.168.57.1:8282

docker run -d --rm -p 8383:88 --name nginx_p2 nginx:alpine #  !!! 88 dst port
curl localhost:8383 
```