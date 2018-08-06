
#include "comm.h"
#include <stdio.h>
#include <heartbeats/heartbeat.h>
#include <string.h>
heartbeat_t* heart;
static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;

// #include <xenstore.h>
#include <stdlib.h>
#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>
using namespace std;




#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#ifdef __cplusplus
}
#endif


extern "C" bool xs_write(struct xs_handle *h, xs_transaction_t t,
        const char *path, const void *data, unsigned int len);
extern "C" void *xs_read(struct xs_handle *h, xs_transaction_t t,
        const char *path, unsigned int *len);


int getDomid(const char* cmd) {
    array<char, 4> buffer;
    string result;
    shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw runtime_error("popen() failed!");
    while (!feof(pipe.get())) {
        if (fgets(buffer.data(), 4, pipe.get()) != nullptr)
            result += buffer.data();
    }
    return stoi(result);
}


void xenstore_write(struct xs_handle *xs, xs_transaction_t th, const char *path, const void *data)
{

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
