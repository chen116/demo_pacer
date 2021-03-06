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


void xenstore_write(struct xs_handle *xs, xs_transaction_t th, const char *path, const void *data)
{

	    // heartbeat(heart, 1);
        // printf("heartbeat: instant rate: %f\n",hb_get_instant_rate(heart) );
        // char hr_str[10];
        // gcvt(hb_get_instant_rate(heart) , 8, hr_str);
        // th = xs_transaction_start(xs);
        // er = xs_write(xs, th, path, hr_str, strlen(hr_str));
        // xs_transaction_end(xs, th, false);
		int er;
        th = xs_transaction_start(xs);
        er = xs_write(xs, th, path, data, strlen(data));
        xs_transaction_end(xs, th, false);
        return;
}
char* xenstore_read(struct xs_handle* xs ,xs_transaction_t th, const char* path , unsigned int *len )
{
	char * buf;
	th = xs_transaction_start(xs);
	buf = xs_read(xs, th, path, len);
	xs_transaction_end(xs, th, false);
	return buf;
}
