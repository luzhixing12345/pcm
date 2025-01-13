
#include "vtism.h"

#include <stdio.h>
#include <iostream>
#include <unistd.h>

#include <cstdlib>

#define VTISM_SYSFS_PATH         "/sys/kernel/mm/vtism/"
#define VTISM_SYSFS_PCM_PATH     "/sys/kernel/mm/vtism/pcm/"

int vtism_init_success = 0;

void init_vtism() {
    // check if /sys/kernel/mm/vtism/ exists
    if (access(VTISM_SYSFS_PATH, F_OK) != 0) {
        std::cerr << "VTISM not supported\n";
        return;
    }
    if (access(VTISM_SYSFS_PCM_PATH, F_OK) != 0) {
        std::cerr << "VTISM pcm not supported\n";
        return;
    }

    std::cerr << "VTISM init success\n";
    vtism_init_success = 1;
    return;
}

int write_bandwidth(int node, int bw, enum bw_type bw_type) {
    if (node == -1 || !vtism_init_success) {
        return 0;
    }
    FILE *f;
    char filename[100];
    snprintf(
        filename, sizeof(filename), "%snode%d/%s_bw", VTISM_SYSFS_PCM_PATH, node, (bw_type == READ) ? "read" : "write");
    f = fopen(filename, "w");
    if (!f) {
        return -1;
    }
    fprintf(f, "%d", bw);
    fclose(f);
    return 0;
}