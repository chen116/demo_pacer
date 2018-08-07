#ifdef __cplusplus
extern "C" {
#endif
#include "comm.h"
#ifdef __cplusplus
}
#endif

static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;
pacer mypacer;
mypacer.heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);
mypacer.domid = getDomid();  
mypacer.xs = xs_daemon_open();
mypacer.base_path = xs_get_domain_path(xs, domid);


int main(int argc, char** argv)
{
	int domid=getDomid();//exec(R"(python3 -c 'from pyxs import Client;c=Client(xen_bus_path="/dev/xen/xenbus");c.connect();print((c.read("domid".encode())).decode());c.close()')"); 
    printf("domid %d\n",domid);
    mypacer.domid = domid;
    printf("mypacer id %d\n",mypacer.domid );



    heartbeat_finish(mypacer.heart);


    return 0;


}