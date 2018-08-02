// gcc -Wall test.c -o test -lxenstore 

#include <stdlib.h>
#include <xenstore.h> 


int main( int argc, const char** argv )
{
    char *path;
    int er;
    struct xs_handle *xs;
    xs_transaction_t th;


    // create and establish connection to xenstore with a path
    xs = xs_daemon_open();
    path = xs_get_domain_path(xs, 4); // domU id , I put 4 for now
    path = (char*)realloc(path, strlen(path) + strlen("/heart_rate") + 1);
    if ( path == NULL ) printf("not good\n");
    strcat(path, "/heart_rate");
    printf("%s\n",path);

	//write to xenstore
    th = xs_transaction_start(xs);
    er = xs_write(xs, th, path, "11.0", strlen("11.0"));
    xs_transaction_end(xs, th, false);

	xs_daemon_close(xs);
	free(path);
}