
#include <stdio.h>


int main() {
    char buffer[16];
    printf("Igrese por favor sus datos");
    scanf("%s", &buffer);
    printf("Datos : %s", buffer);
    return 0;
}

/*
int authed = 0;
char password_buffer[16];
strcopy(password_buffer, your_password)
if (strcmp(password_buffer, password) == 0) {
            authed = 1;
}
else {
            authed = 0;
}
*/