
#include <stdio.h>


int main() {
    char buffer[100];
    printf("Igrese por favor sus datos\n");
    scanf("%s", buffer);
    //printf("Datos : %s", buffer);
    printf("Buffer: %p\n",buffer);
    printf(buffer);
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