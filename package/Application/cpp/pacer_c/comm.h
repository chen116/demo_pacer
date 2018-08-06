
#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#ifdef __cplusplus
}
#endif
#include <heartbeats/heartbeat.h>

struct pacer {
        int domid;
        // struct xs_handle* xs;
        // struct xs_transaction_t th;
        char * base_path;
        heartbeat_t * heart;
};
// extern "C" char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
// extern "C" int xenstore_write(struct xs_handle *, xs_transaction_t , const char *, const void *);

char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
void xenstore_write(struct xs_handle *, xs_transaction_t , const char *, const void *);
int getDomid();