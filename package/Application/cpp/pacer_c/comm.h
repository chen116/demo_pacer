
#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#ifdef __cplusplus
}
#endif
#include <heartbeats/heartbeat.h>

typedef struct pacer_t {
        int domid;
        xs_handle_t* xs;
        xs_transaction_t th;
        char * base_path;
        heartbeat_t * heart;
}pacer;
// extern "C" char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
// extern "C" int xenstore_write(struct xs_handle *, xs_transaction_t , const char *, const void *);

char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
void xenstore_write(struct xs_handle *, xs_transaction_t , const char *, const void *);
int getDomid();