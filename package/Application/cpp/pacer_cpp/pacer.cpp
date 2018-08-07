#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#include "comm.h"
#ifdef __cplusplus
}
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vector>

#include <heartbeats/heartbeat.h>
#include <iostream>
#include <map>
#include <string>
using namespace std;

// C function declarations
extern "C" {
	char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
	void xenstore_write(struct xs_handle *, xs_transaction_t , const char *, const void *);
	int xenstore_getDomid();
}



int exec() {
	return 1;
}

#include "pacer.h"
static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;
Pacer::Pacer()
{
 	domid = xenstore_getDomid();
 	xs = xs_daemon_open();
 	heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);
	heart_rate_path = xs_get_domain_path(xs, domid);
	heart_rate_path = (char*)realloc(heart_rate_path, strlen(heart_rate_path) + strlen("/heart_rate") + 1);
	strcat(heart_rate_path, "/heart_rate");
}
char* Pacer::readItem(char * item)
{
	unsigned int len;
	for (map<char *,char *>::iterator it=paths.begin(); it!=paths.end(); ++it)
	{
    	if (strcmp(it->first,item)==0) return xenstore_read(xs,th,it->second,&len);
	}
	return "not found";
}


void Pacer::writeHeartRate()
{
	xenstore_write(xs, th, heart_rate_path, to_string(heart->hb_get_instant_rate(heart)).c_str());
	return;
}
char * Pacer::readHeartRate()
{
	unsigned int len;
	return xenstore_read(xs,th,heart_rate_path,&len);
}
void Pacer::writeItem(char * item, char * content)
{
	unsigned int len;
	for (map<char *,char *>::iterator it=paths.begin(); it!=paths.end(); ++it)
	{
    	if (strcmp(it->first,item)==0)
    	{
    		xenstore_write(xs, th, it->second, to_string(hb_get_instant_rate(heart)).c_str());
    		return;
    	}
	}
	return;
}

void Pacer::setItem(char * item)
{
	char *path;
	path = xs_get_domain_path(xs, domid);
	path = (char*)realloc(path, strlen(path) + strlen(item) + 2);
	strcat(path, "/");
	strcat(path, item);
	paths[item]=path;
}
void Pacer::getItems()
{
	 for (map<char *,char *>::iterator it=paths.begin(); it!=paths.end(); ++it)
    cout << it->first << " => " << it->second << '\n';
}

void Pacer::getDomid()
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

  return domid;
}