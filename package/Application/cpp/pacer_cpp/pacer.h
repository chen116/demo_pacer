
#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#ifdef __cplusplus
}
#endif
#include <heartbeats/heartbeat.h>
class Pacer
{
private:
    int domid;
    struct xs_handle* xs;
    xs_transaction_t th;
    char * base_path;
    heartbeat_t * heart;

public:
  Pacer();
  int myDomid();

};
