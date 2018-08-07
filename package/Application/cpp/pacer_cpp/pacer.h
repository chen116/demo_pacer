
#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#ifdef __cplusplus
}
#endif
#include <heartbeats/heartbeat.h>
// #include <vector>
// #include <iostream>
// #include <map>
// #include <string>


#include <map>
using namespace std;


class Pacer
{
private:
    int domid;
    struct xs_handle* xs;
    xs_transaction_t th;
    heartbeat_t * heart;
    char *heart_rate_path; 
    map<char *,char * > paths;


public:
  Pacer();
  ~Pacer();
  int getDomid();
  void getItems();
  void setItem(char *);
  char* readItem(char *);
  char* readHeartRate();
  void writeItem(char *, const char *);
  void writeInstantHeartRate();
  void writeWindowHeartRate();
  void writeGlobalHeartRate();
  void beat();
  void setWindowSize(const int64_t);

};
