

#include <xenstore.h>


char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
int xenstore_write(struct xs_handle *, xs_transaction_t , const char *, const void *);
int getDomid();