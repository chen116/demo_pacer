
#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#ifdef __cplusplus
}
#endif
#include <heartbeats/heartbeat.h>
#include <map>
using namespace std;

// Pacer class
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
    void getEntrys();
    void setEntry(char *);
    char* readEntry(char *);
    char* readHeartRate();
    void writeEntry(char *, const char *);
    void writeInstantHeartRate();
    void writeWindowHeartRate();
    void writeGlobalHeartRate();
    void beat();
    void setWindowSize(const int64_t);

};
