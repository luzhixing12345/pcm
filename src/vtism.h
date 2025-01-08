
#pragma once

int init_vtism(void);

enum bw_type {
    READ,
    WRITE
};

int write_bandwidth(int node, int bw, enum bw_type bw_type);