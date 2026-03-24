# syntax=docker/dockerfile:1
FROM gcc:13

WORKDIR /app

RUN apt-get update && apt-get install -y cmake build-essential && rm -rf /var/lib/apt/lists/*

COPY CMakeLists.txt .
COPY src/ src/

RUN cmake . && make

CMD ["/app/hello"]
