
#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#ifdef __cplusplus
}
#endif
#include <heartbeats/heartbeat.h>
#include <vector>
#include <iostream>
#include <map>
#include <string>
using namespace std;


class Pacer
{
private:
    int domid;
    struct xs_handle* xs;
    xs_transaction_t th;
    char * base_path;
    heartbeat_t * heart;
    map<char *,char * > paths;


public:
  Pacer();
  int getDomid();
  int getItems();

};
