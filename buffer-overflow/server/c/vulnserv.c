
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

int main() {
    int sockfd, csockfd, caddrlen;
    struct sockaddr_in srv_addr, cli_addr;
    char buffer[100];

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        exit(1);
    }

    srv_addr.sin_family = AF_INET;
    srv_addr.sin_addr.s_addr = INADDR_ANY;
    srv_addr.sin_port = htons(9999);
    int res = bind(sockfd, (struct sockaddr*)&srv_addr, sizeof(srv_addr));
    if (res < 0) {
        exit(1);
    }

    listen(sockfd,1);
    caddrlen = sizeof(cli_addr);
    csockfd = accept(sockfd, (struct sockaddr*)&cli_addr, &caddrlen);
    if (csockfd < 0) {
        exit(1);
    }

    recv(csockfd, buffer, 2000, 0);
    printf(buffer);

    close(csockfd);
    close(sockfd);

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