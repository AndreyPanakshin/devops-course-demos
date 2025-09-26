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

docker build -t hello-scratch:latest . # -t Name and optionally a tag
```

## Создание пустого контейнера
```bash
docker create --name scratch_test --entrypoint /hello hello-scratch
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

docker build -t hello-scratch:latest . # -t Name and optionally a tag
docker create --name scratch_test hello-scratch:latest
docker export scratch_test -o scratch_test.tar
mkdir out
tar xf scratch_test.tar -C out/
docker save hello-scratch:latest -o image_scratch_test.tar
mkdir image_out
tar xf image_scratch_test.tar -C image_out/
```