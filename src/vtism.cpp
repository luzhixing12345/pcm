
#include "vtism.h"

#include <stdio.h>
#include <unistd.h>

#include <cstdlib>

#define VTISM_SYSFS_PATH     "/sys/kernel/mm/vtism/"
#define VTISM_SYSFS_PCM_PATH "/sys/kernel/mm/vtism/pcm/"

int init_vtism() {
    // check if /sys/kernel/mm/vtism/ exists
    if (access(VTISM_SYSFS_PATH, F_OK) != 0) {
        printf("VTISM not supported\n");
        exit(0);
    }
    if (access(VTISM_SYSFS_PCM_PATH, F_OK) != 0) {
        printf("VTISM interface not supported\n");
        exit(0);
    }

    return 0;
}

int write_bandwidth(int node, int bw, enum bw_type bw_type) {
    if (node == -1) {
        return 0;
    }
    FILE *f;
    char filename[100];
    snprintf(
        filename, sizeof(filename), "%snode%d/%s_bw", VTISM_SYSFS_PCM_PATH, node, (bw_type == READ) ? "read" : "write");
    // f = fopen(filename, "w");
    // if (!f) {
    //     return -1;
    // }
    // fprintf(f, "%d", bw);
    // fclose(f);
    // printf("write %s %d\n", filename, bw);
    return 0;
}