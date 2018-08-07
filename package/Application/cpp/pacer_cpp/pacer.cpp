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

int Pacer::getDomid()
{
  return getDomid();
}