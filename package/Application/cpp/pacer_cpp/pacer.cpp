#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#include "comm.h"
#ifdef __cplusplus
}
#endif




// C function declarations
extern "C" {
	char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
	void xenstore_write(struct xs_handle *, xs_transaction_t , const char *, const void *);
	int getDomid();
}



int exec() {
	return 1;
}

#include "pacer.h"

Pacer::Pacer(int x,int y)
{


  gx = x;
  gy = y;
}

int Pacer::getSum()
{
  return gx + gy;
}

int Pacer::myDomid()
{
	int er;

	unsigned int len;
    struct xs_handle *xs;
    xs_transaction_t th;
    xs = xs_daemon_open();

    char *frame_num_path;
	frame_num_path = xs_get_domain_path(xs, 16); 
	frame_num_path = (char*)realloc(frame_num_path, strlen(frame_num_path) + strlen("/frame_number_entry") + 1);
    strcat(frame_num_path, "/frame_number_entry");

    printf("%s\n",xenstore_read(xs,th,frame_num_path,&len));

  return getDomid();
}