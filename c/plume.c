#include "git2.h"
#include "toml.h"
#include "string.h"
#include <stdio.h>
#include <stdlib.h>


void add_plugin(const char *url) {
    printf("Installiere Plugin: %s\n", url);

}

void remove_plugin(const char *plugin) {
    printf("Entferne Plugin: %s\n", plugin);
}

void show_plugins() {
    printf("Installierte Plugins:\n");
}

void sync_plugins() {
    printf("Installierte Plugins:\n");
}

void update_plugins() {
    printf("Installierte Plugins:\n");
}

void print_help() {
    printf("Verwendung: plume <befehl> [argument]\n");
    printf("Befehle:\n");
    printf("  add <url>       Fügt ein Plugin hinzu\n");
    printf("  remove <plugin> Entfernt ein Plugin\n");
    printf("  show            Zeigt installierte Plugins\n");
    printf("  sync            Installiert fehlende Plugins\n");
    printf("  update          Aktualisiert installierte Plugins\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_help();
        return EXIT_FAILURE;
    }

    if (strcmp(argv[1], "add") == 0) {
        if (argc < 3) {
                fprintf(stderr, "Fehlendes Argument: URL\n");
                return EXIT_FAILURE;
            }
            add_plugin(argv[2]);
    } else if (strcmp(argv[1], "remove") == 0) {
        if (argc < 3) {
            fprintf(stderr, "Fehlendes Argument: Plugin-Name\n");
            return EXIT_FAILURE;
        }
        remove_plugin(argv[2]);
    } else if (strcmp(argv[1], "show") == 0) {
        show_plugins();
    } else if (strcmp(argv[1], "sync") == 0) {
        sync_plugins();
    } else if (strcmp(argv[1], "update") == 0) {
        update_plugins();
    } else {
        fprintf(stderr, "Unbekanntes Kommando: %s\n", argv[1]);
        print_help();
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
