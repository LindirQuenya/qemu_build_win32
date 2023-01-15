#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include <windows.h>

#ifndef MAX_PATH
#define MAX_PATH 260
#endif

int main() {
	char *windowsPath = malloc(MAX_PATH*sizeof(char));
	uint32_t windowsPath_len = GetSystemDirectoryA(windowsPath, MAX_PATH);
	if (windowsPath_len == 0) {
		free(windowsPath);
		windowsPath = NULL;
		fprintf(stderr, "Failed to fetch Windows path!");
		return -1;
	}
	printf("MAX_PATH is %d\n", MAX_PATH);
	printf("System path is: '%s'\n", windowsPath);
	if (strcat_s(windowsPath, MAX_PATH, "\\cmd.exe")) {
		free(windowsPath);
		windowsPath = NULL;
		fprintf(stderr, "Failed to combine strings!");
		return -1;
	}
	printf("Combined path is: '%s'\n", windowsPath);
	free(windowsPath);
	windowsPath = NULL;
	return 0;
}
