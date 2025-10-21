## Bind Mounts

```bash
mkdir ~/demo-bind
echo "Hello from host" > ~/demo-bind/file.txt

docker run --rm -d \
  --name bind-demo \
  --mount type=bind,source=$HOME/demo-bind,target=/data \
  busybox sleep 1000

docker exec -it bind-demo sh
cat /data/host.txt

echo "Edited from container" >> /data/host.txt
exit

cat ~/demo-bind/host.txt

docker exec -it bind-demo sh
mkdir /data/some-dir
touch /data/some-dir/secret.txt
exit 

rm -rf /data/some-dir
```

## Docker volumes
```bash
docker volume create myvol
docker run --rm -d \
  --name volume-demo \
  --mount type=volume,source=myvol,target=/data \
  busybox sleep 1000

docker exec -it volume-demo sh
echo "Data inside volume" > /data/info.txt
exit

docker stop volume-demo

docker run -it --rm \
  --mount type=volume,source=myvol,target=/data \
  busybox cat /data/info.txt
```