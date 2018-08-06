
#include <stdio.h>
#include <xenstore.h>


char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
void xenstore_write(struct xs_handle *, xs_transaction_t , const char *, const void *);
int getDomid();