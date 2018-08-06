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


int xenstore_write(struct xs_handle *h, xs_transaction_t t, const char *path, const void *data, unsigned int len)
{
		int er;
        th = xs_transaction_start(xs);
        er = xs_write(xs, th, path, hr_str, strlen(hr_str));
        xs_transaction_end(xs, th, false);
        return er;
}
char* xenstore_read(struct xs_handle* xs ,xs_transaction_t th, const char* path , unsigned int *len )
{
	char * buf;
	th = xs_transaction_start(xs);
	buf = xs_read(xs, th, path, len);
	xs_transaction_end(xs, th, false);
	return buf;
}
