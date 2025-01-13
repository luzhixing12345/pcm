
# Intel PCM for vtism

> [pcm](https://github.com/intel/pcm)

this repo is used to get memory bandwidth and latency for vtism

## build

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

## usage

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
cat /sys/kernel/mm/vtism/dump
```