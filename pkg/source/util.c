#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <orbis/libkernel.h>

#include "../include/util.h"
#include <orbis/_types/kernel.h>

void logger(const char *tag, const char *message, ...) {
  time_t now;
  time(&now);

  struct tm *tm_info = localtime(&now);
  char time_str[20];
  strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", tm_info);

  printf("%s [%s]: ", time_str, tag);

  va_list args;
  va_start(args, message);
  vprintf(message, args);
  va_end(args);

  printf("\n");
}

void Notify(const char *fmt, ...) {
  OrbisNotificationRequest buffer;

  va_list args;
  va_start(args, fmt);
  vsprintf(buffer.message, fmt, args);
  va_end(args);

  buffer.type = NotificationRequest;
  buffer.unk3 = 0;
  buffer.useIconImageUri = 1;
  buffer.targetId = -1;
  strcpy(buffer.iconUri, "cxml://psnotification/tex_icon_champions_league");

  sceKernelSendNotificationRequest(0, &buffer, 3120, 0);
}
