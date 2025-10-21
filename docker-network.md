## Docker network

```bash
docker network ls
# Встроенные драйверы сети https://docs.docker.com/engine/network/drivers/

ip link | grep docker
brctl show

#  У docker0 сеть всегда 172.17.0.1/16
ip -4 a

docker run --rm -d --name nginx_n1 nginx:alpine
docker exec nginx_n1 ip -4 a 
docker network inspect bridge

docker run --rm -d --network host --name nginx_n2 nginx:alpine
docker exec nginx_n2 ip -4 a 


docker run --rm -d --name nginx_n3 nginx:alpine
docker exec nginx_n3 ping -c 1 
```