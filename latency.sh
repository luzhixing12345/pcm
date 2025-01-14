#!/bin/bash
sudo ./build/bin/pcm-raw -el event_file.txt 2>/dev/null -ext | python cal_latency.py