#include "ps4.h"

#define ENC_SEALEDKEY_LEN 0x60
#define DEC_SEALEDKEY_LEN 0x20

int decryptSealedKey(uint8_t enc_key[ENC_SEALEDKEY_LEN], uint8_t dec_key[DEC_SEALEDKEY_LEN]) {
  uint8_t dummy[0x10];
  UNUSED(dummy);
  uint8_t data[ENC_SEALEDKEY_LEN + DEC_SEALEDKEY_LEN] = {0};

  int fd = open("/dev/sbl_srv", O_RDWR, 0);
  if (fd == -1) {
    return -1;
  }

  memcpy(data, enc_key, ENC_SEALEDKEY_LEN);

  if (ioctl(fd, 0xC0845302, data) == -1) {
    close(fd);
    return -2;
  }

  memcpy(dec_key, &data[ENC_SEALEDKEY_LEN], DEC_SEALEDKEY_LEN);
  close(fd);

  return 0;
}

int decryptSealedKeyAtPath(const char *keyPath, uint8_t decryptedSealedKey[DEC_SEALEDKEY_LEN]) {
  uint8_t sealedKey[ENC_SEALEDKEY_LEN] = {0};

  int fd = open(keyPath, O_RDONLY, 0);
  if (fd == -1) {
    return -1;
  }

  if (read(fd, sealedKey, ENC_SEALEDKEY_LEN) != ENC_SEALEDKEY_LEN) {
    close(fd);
    return -2;
  }
  close(fd);

  if (decryptSealedKey(sealedKey, decryptedSealedKey) != 0) {
    return -3;
  }

  return 0;
}
