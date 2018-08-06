char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
int xenstore_write(struct xs_handle *h, xs_transaction_t t, const char *path, const void *data);
int getDomid();