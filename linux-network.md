## Linux network NS

```bash
ip netns help 

ip netns add ns1

ip link add veth1a type veth peer name veth1b
ip link set veth1b netns ns1
ip netns exec ns1 ip link set dev veth1b up
ip link set dev veth1a up

ip netns exec ns1 tcpdump -Xe -l -i veth1b

echo "ff:ff:ff:ff:ff:ff 7a:1c:62:27:e6:98 8102 48 69" | xxd -r -p | socat - INTERFACE:veth1a
```

## Linux Bridge
```bash
ip netns add ns2
ip netns add ns3
ip netns add ns4

ip link add veth2a type veth peer name veth2b
ip link set veth2b netns ns2
ip netns exec ns2 ip link set dev veth2b up
ip link set dev veth2a up

ip link add veth3a type veth peer name veth3b
ip link set veth3b netns ns3
ip netns exec ns3 ip link set dev veth3b up
ip link set dev veth3a up

ip link add veth4a type veth peer name veth4b
ip link set veth4b netns ns4
ip netns exec ns4 ip link set dev veth4b up
ip link set dev veth4a up

ip link add br0 type bridge
ip link set master br0 dev veth1a
ip link set master br0 dev veth2a
ip link set master br0 dev veth3a
ip link set master br0 dev veth4a

ip link set dev br0 up
brctl show br0

ip netns exec ns1 ip addr add 10.10.10.1/24 dev veth1b
ip netns exec ns2 ip addr add 10.10.10.2/24 dev veth2b
ip netns exec ns3 ip addr add 10.10.10.3/24 dev veth3b
ip netns exec ns4 ip addr add 10.10.10.4/24 dev veth4b

ip addr add 10.10.10.11/24 dev veth1a
ip addr add 10.10.10.22/24 dev veth2a
ip addr add 10.10.10.33/24 dev veth3a
ip addr add 10.10.10.44/24 dev veth4a
```