#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include <windows.h>
#include <glib.h>

#ifndef MAX_PATH
#define MAX_PATH 260
#endif

const char *exec_get_cmd_path() {
    g_autofree char *systemPath = g_malloc(MAX_PATH*sizeof(char));
    const char *cmdPath;
    if (GetSystemDirectoryA(systemPath, MAX_PATH) == 0 || strcat_s(systemPath, MAX_PATH, "\\cmd.exe")) {
        fprintf(stderr, "Could not find cmd.exe path, using default.");
        cmdPath = "C:\\Windows\\System32\\cmd.exe";
    } else {
        cmdPath = g_steal_pointer(&systemPath);
    }
    return cmdPath;
}

int main() {
	const char *cmdPath = exec_get_cmd_path();
	printf("Cmd path is: %s\n", cmdPath);
	return 0;
}
