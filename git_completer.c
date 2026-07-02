#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char *argv[]) {
    if (argc < 4) {
        return 1;
    }

    char *command = argv[1];      // e.g., "git"
    char *current = argv[2];      // current word being completed
    char *previous = argv[3];     // previous word

    // Get environment variables
    char *comp_line = getenv("COMP_LINE");
    char *comp_point_str = getenv("COMP_POINT");
    int comp_point = comp_point_str ? atoi(comp_point_str) : 0;

    // Simple git completion logic
    if (strcmp(command, "git") == 0) {
        if (strcmp(previous, "remote") == 0) {
            if (strstr(current, "set") == current) {
                printf("set-url\n");
            } else {
                printf("add\n");
                printf("remove\n");
                printf("set-url\n");
                printf("show\n");
            }
        }
        else if (strncmp(current, "remote",2) == 0) {
            printf("remote\n");
            printf("rebase\n");
            printf("reset\n");
        }
    }

    return 0;
}   