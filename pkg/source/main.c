

#include <dirent.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// Orbis specific header
#include <orbis/libkernel.h>

// Custom functions header
#include "../include/jbc.h"
#include "../include/sqlite3.h"
#include "../include/util.h"

static void terminate(void) {
  logger("BREW", "Exiting...");
  terminate_jbc();
}

int main(void) {
  int sleepSeconds = 2;

  sqlite3 *db = NULL;

  // // Initialize jailbreak
  if (!initialize_jbc() || !initVshDataMount()) {
    Notify("Failed to initialize jailbreak!");
    terminate();
  }
  if (sqlite3_open_v2("/user/home/148c2012/trophy/db/trophy_local.db", &db,
                      SQLITE_OPEN_READONLY, "orbis_rw") != SQLITE_OK) {
    logger("BREW", "Error open memvfs: %s", sqlite3_errmsg(db));
    terminate();
  }

  logger("BREW", "Hello motherfucker! Waiting %d seconds!", sleepSeconds);
  sceKernelUsleep(2 * 1000000);
  logger("BREW", "Done. Infinitely looping...");

  for (;;) {
  }
}
