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
https://docs.docker.com/reference/dockerfile/

## Создание scratch имеджа https://docs.docker.com/build/building/base-images/#create-a-base-image
```bash
cat > Dockerfile << EOF
FROM scratch
EOF

docker build -t hello-scratch:empty . # -t Name and optionally a tag
```

## Создание пустого контейнера
```bash
docker create --name scratch_test --entrypoint /hello hello-scratch:empty
docker export scratch_test -o scratch_test.tar
mkdir out
tar xf scratch_test.tar -C out/

docker cp hello scratch_test:/hello
rm -rf scratch_test.tar
rm -rf out/*
docker export scratch_test -o scratch_test.tar
tar xf scratch_test.tar -C out/

docker start scratch_test
docker inspect scratch_test
docker rm scratch_test
cd ..
```

## Создание имеджа с единственным исполняемым файлом
```bash
mkdir second 
cp hello second/
cd second
cat > Dockerfile << EOF
FROM scratch
COPY hello /hello
ENTRYPOINT ["/hello"]
EOF

docker build -t hello-scratch:hello . # -t Name and optionally a tag

docker save hello-scratch:hello -o image_scratch_test.tar
mkdir image_out
tar xf image_scratch_test.tar -C image_out/
```

```bash
docker create --name scratch_test hello-scratch:hello
docker export scratch_test -o scratch_test.tar
mkdir out
tar xf scratch_test.tar -C out/
```

[//]: # (TODO: https://github.com/wagoodman/dive)

# Имеджи
https://docs.docker.com/engine/storage/drivers/

## Имедж состоит из слоев
```bash
docker inspect hello-scratch:hello  | grep -A 5 RootFS
cat /var/lib/docker/image/overlay2/layerdb/sha256/<Docker Image Layer ID>/cache-id
ls -la /var/lib/docker/overlay2/<Overlay Layer ID>/diff
```

## Файловая система контейнера это writable слой + слои имеджа
```bash
docker inspect scratch_test  | grep  Dir
```
LowerDir - Слои из имеджа + служебный init слой
UpperDir - Writable слой
MergedDir - Итоговая ФС

## Благодаря слоистой ФС экономим диск
```bash
docker pull nginx:latest
docker run -d --name nginx1 nginx:latest
docker run -d --name nginx2 nginx:latest
docker run -d --name nginx3 nginx:latest

docker inspect nginx1 | grep LowerDir > nginx1.txt
docker inspect nginx2 | grep LowerDir > nginx2.txt
docker inspect nginx3 | grep LowerDir > nginx3.txt
vimdiff nginx1.txt nginx2.txt
vimdiff nginx1.txt nginx3.txt
```

## Сopy-on-Write strategy
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

```bash
docker inspect nginx1 | grep UpperDir
```

# Registry
```bash
docker images

docker tag nginx:latest abrakadabra:latest

# https://hub.docker.com/repository
docker login
docker tag <old tag> <new tag>
docker push <new tag>

docker pull nginx
docker pull docker.io/nginx:latest
```

# Dockerfile
https://docs.docker.com/reference/dockerfile/