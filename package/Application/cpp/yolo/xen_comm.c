#include <stdio.h>
#include <xenstore.h>
#include <heartbeats/heartbeat.h>
#include <string.h>
heartbeat_t* heart;
static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;


int hi( )
{
    char *path;
	int er;
	char * buf;
	// unsigned int *len =  (unsigned int*) malloc(sizeof(unsigned int));
	// int len = 42;

	unsigned int len;
    struct xs_handle *xs;
    xs_transaction_t th;
    xs = xs_daemon_open();

    path = xs_get_domain_path(xs, 10); 
    path = (char*)realloc(path, strlen(path) + strlen("/frame_number_entry") + 1);
    strcat(path, "/frame_number_entry");
    printf("%s\n",path);
	th = xs_transaction_start(xs);
	buf = xs_read(xs, th, path, &len);
	xs_transaction_end(xs, th, false);
	printf("%s\n",buf );

	return 1;
}
