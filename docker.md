# Docker

## Создание программы на языке C
```bash
cat > main.c << EOF
#include <stdio.h>

int main() {
    printf("Hello from scratch container!\n");
    return 0;
}
EOF

gcc -static -o hello main.c
```

## Создание image
- Имедж создается из Dockerfile https://docs.docker.com/reference/dockerfile/  
- Имедж создается из другого имеджа 

### Создание scratch имеджа
https://docs.docker.com/build/building/base-images/#create-a-base-image
```bash
cat > Dockerfile << EOF
FROM scratch
EOF

docker build -t hello-scratch . # -t Name and optionally a tag
```

### Создание пустого контейнера
```bash
docker create --name scratch-test --entrypoint /hello hello-scratch

docker ps -a

# https://docs.docker.com/reference/api/engine/version/v1.51/#tag/Container/operation/ContainerList
curl --silent -XGET --unix-socket /run/docker.sock http://localhost/containers/json?all=true | jq . 

docker export scratch-test -o scratch-test.tar
mkdir first
tar xf scratch-test.tar -C first/

docker cp hello scratch-test:/hello

docker export scratch-test -o scratch-test-with-hello.tar
mkdir second
tar xf scratch-test-with-hello.tar -C second/

docker start scratch-test
docker logs scratch-test
docker start scratch-test -a

docker inspect scratch-test
```

### Создание имеджа с единственным исполняемым файлом
```bash
cat > Dockerfile << EOF
FROM scratch
COPY hello /hello
ENTRYPOINT ["/hello"]
EOF

docker build -t hello-img . # -t Name and optionally a tag

docker save hello-img -o image_scratch-test.tar
mkdir out_image
tar xf image_scratch-test.tar -C out_image

mkdir layer 
tar xf out_image/blobs/sha256/3551f8658e6915f7fc0ccb07cef4a590b61a0c2788058688b8c818b002fb0174 -C layer
```

```bash
docker create --name hello-test hello-img
docker export hello-test -o hello-test.tar
mkdir out
tar xf hello-test.tar -C out/
```

## Имеджи
- Имеджи состояни из слоев https://docs.docker.com/engine/storage/drivers/
- Слой это набор изменений файловой системы

### Имедж состоит из слоев
```bash
docker inspect hello-img  | grep -A 5 RootFS
cat /var/lib/docker/image/overlay2/layerdb/sha256/<Docker Image Layer ID>/cache-id;echo
ls -la /var/lib/docker/overlay2/<Overlay Layer ID>/diff

dive hello-img
```

### Файловая система контейнера это writable слой + слои имеджа
```bash
docker inspect hello-test  | grep  Dir

docker inspect hello-scratch  | grep  Dir
```
- LowerDir - Слои из имеджа + служебный init слой
- UpperDir - Writable слой
- MergedDir - Итоговая ФС


### Благодаря слоистой ФС экономим диск
```bash
docker pull nginx
dive nginx

du -sh /var/lib/docker/overlay2/

docker pull nginx:alpine

docker run -d --name nginx1 nginx
docker run -d --name nginx2 nginx
docker run -d --name nginx3 nginx

docker inspect nginx1 | grep LowerDir > nginx1.txt
docker inspect nginx2 | grep LowerDir > nginx2.txt
docker inspect nginx3 | grep LowerDir > nginx3.txt
vimdiff nginx1.txt nginx2.txt
vimdiff nginx1.txt nginx3.txt

docker system df
# du -sh /var/lib/docker/overlay2
```

### Сopy-on-Write strategy
```bash
docker exec -it nginx1 ls
docker exec -it nginx1 bash 
docker inspect nginx1 | grep UpperDir
```

```bash
cat /etc/apt/sources.list.d/debian.sources 

cat > /etc/apt/sources.list.d/debian.sources << EOF
Types: deb
# http://snapshot.debian.org/archive/debian/20250908T000000Z
URIs: http://deb.debian.org/debian
Suites: bookworm bookworm-updates
Components: main
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
EOF
```

## Registry
```bash
docker images

docker tag nginx:latest abrakadabra:latest

# https://hub.docker.com/repository
docker login
docker push abrakadabra:latest

docker pull nginx
docker pull docker.io/nginx:latest
```

## Dockerfile
https://docs.docker.com/reference/dockerfile/