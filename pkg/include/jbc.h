#ifndef ORBIS_JBC_H
#define ORBIS_JBC_H

#include <libjbc.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

#include <orbis/libkernel.h>

int sysKernelGetLowerLimitUpdVersion(int *unk);
int sysKernelGetUpdVersion(int *unk);
int sys_mknod(const char *path, mode_t mode, dev_t dev);
int init_cred(void);
int init_devices(void);
int initVshDataMount(void);
int get_firmware_version(void);
int get_max_pfskey_ver(void);
const char *get_fw_by_pfskey_ver(int key_ver);
int is_jailbroken(void);
int jailbreak(void);
int initialize_jbc(void);
void terminate_jbc(void);

#endif