
# Intel PCM for vtism

> [pcm](https://github.com/intel/pcm)

this repo is used to get memory bandwidth and latency for vtism

## build

```bash
git submodule update --init --recursive
```

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

## usage

all the following cmd should run in pcm root path

for bandwidth

```bash
sudo ./build/bin/pcm-memory
```

for latency

```bash
sudo ./build/bin/pcm-raw -el event_file.txt 2>/dev/null -ext | python cal_latency.py
```

## check

```bash
(base) lzx@cxl2:~$ cat /sys/kernel/mm/vtism/dump
node 0 demotion target: 1 2 3
node 1 demotion target: 0 2 3
node 2 has no demotion target(cxl node)
node 3 has no demotion target(cxl node)

node 0: total = 64058 MB(62 GB), free = 59912 MB(58 GB)
node 1: total = 64453 MB(62 GB), free = 46731 MB(45 GB)
node 2: total = 64511 MB(62 GB), free = 64200 MB(62 GB)
node 3: total = 64505 MB(62 GB), free = 64199 MB(62 GB)

  node   read_bw(MB/s)  write_bw(MB/s)  latency(ns) to_cxl_latency(ns)
     0               0               0         186            464
     1               0               0         210           3030
     2               0               0           -              -
     3               0               0           -              -
```