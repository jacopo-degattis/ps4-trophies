
#include "crypto.h"
#include "kern.h"
#include "ps4.h"

#define ENC_SEALEDKEY_LEN 0x60
#define DEC_SEALEDKEY_LEN 0x20

#define debug(sock, format, ...)                       \
  do {                                                 \
    char buffer[512];                                  \
    int size = sprintf(buffer, format, ##__VA_ARGS__); \
    sceNetSend(sock, buffer, size, 0);                 \
  } while (0)
int sock;

void binary_to_hex_string(const uint8_t *data, size_t data_len, char *hex_str, size_t hex_str_len) {
  for (size_t i = 0; i < data_len && (i * 2 + 2) < hex_str_len; i++) {
    sprintf(hex_str + (i * 2), "%02X", data[i]);
  }
  hex_str[data_len * 2] = '\0'; // Null terminate
}

void other_hex_to_string(const uint8_t *data, size_t data_len, char *hex_str, size_t hex_str_len) {
  // Make sure we have enough space (2 chars per byte + null terminator)
  if (hex_str_len < (data_len * 2 + 1)) {
    // Not enough space, handle error or truncate
    return;
  }

  for (size_t i = 0; i < data_len; i++) {
    sprintf(hex_str + (i * 2), "%02X", data[i]);
  }
  hex_str[data_len * 2] = '\0'; // Null terminate
}

size_t page_size = 0x4000;

typedef struct sealedkey_t {
  const unsigned char MAGIC[8];
  const unsigned char CAT[8];
  const unsigned char IV[16];
  const unsigned char KEY[32];
  const unsigned char SHA256[32];
} PfsSKKey;

// My user reference
const char *USER1 = "10000000";
const char *usb0 = "/mnt/usb0/";
const char *usb1 = "/mnt/usb1/";
const char *pfs = "dec_pfsSK.Key";
const char *home = "/user/home/";
char *usb_error = "[-] ERROR: Can't access usb0 nor usb1!\n[-] Will return now to caller.\n";

void SetupNetwork() {
  char socketName[] = "debug";
  struct sockaddr_in server;

  server.sin_len = sizeof(server);
  server.sin_family = AF_INET;
  sceNetInetPton(2, "192.168.1.132", &server.sin_addr);
  server.sin_port = sceNetHtons(18194);
  memset(server.sin_zero, 0, sizeof(server.sin_zero));

  sock = sceNetSocket(socketName, AF_INET, SOCK_DGRAM, 0);
  sceNetConnect(sock, (struct sockaddr *)&server, sizeof(server));

  debug(sock, "debugnet Initialized\n");
}

int _main(struct thread *td) {
  UNUSED(td);

  // Initialize PS4 Kernel, libc, and networking
  initKernel();
  initLibc();
  initSysUtil();
  initNetwork();
  SetupNetwork();

  // jailbreak();
  syscall(11, &kpayload, NULL);

  printf_notification("Done, decrypting...");

  PfsSKKey sealed_key;
  char hexBuffer[DEC_SEALEDKEY_LEN * 2 + 1];
  uint8_t decryptedSealedKey[DEC_SEALEDKEY_LEN];

  FILE *keyFile = fopen("/mnt/usb0/pfskeyencrypted", "rb");

  if (!keyFile) {
    printf_notification("Unable to read input file");
    return 1;
  }

  if (fread(&sealed_key, sizeof(PfsSKKey), 1, keyFile) != 1) {
    debug(sock, "Unable to read inside struct");
    fclose(keyFile);
    return 1;
  }
  fclose(keyFile);

  // Verify magic bytes
  if (memcmp(sealed_key.MAGIC, "pfsSKKey", 8) != 0) {
    debug(sock, "Invalid sealed key format (wrong magic bytes)");
    return 1;
  }

  debug(sock, "Magic: %.8s\n", sealed_key.MAGIC);
  debug(sock, "Category: %.8s\n", sealed_key.CAT);

  char IVhexBuffer[sizeof(sealed_key.IV) * 2 + 1];
  other_hex_to_string(sealed_key.IV, sizeof(sealed_key.IV), IVhexBuffer, sizeof(IVhexBuffer));

  debug(sock, "IV: %s", IVhexBuffer);

  int ret = decryptSealedKeyAtPath("/mnt/usb0/pfskeyencrypted", decryptedSealedKey);

  if (ret < 0) {
    debug(sock, "Error return code is: %d", ret);
    return ret;
  }

  binary_to_hex_string(decryptedSealedKey, DEC_SEALEDKEY_LEN, hexBuffer, sizeof(hexBuffer));

  debug(sock, "Decrypted key: %s", hexBuffer);

  FILE *dump = fopen("/mnt/usb1/decryptedSaveDataKey.bin", "w");
  fwrite(decryptedSealedKey, sizeof(decryptedSealedKey), 1, dump);
  fclose(dump);

  printf_notification("Decrypted!!!");

  return 0;
}