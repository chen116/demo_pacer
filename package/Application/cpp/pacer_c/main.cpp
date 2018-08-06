#ifdef __cplusplus
extern "C" {
#endif
#include "comm.h"
#ifdef __cplusplus
}
int main(int argc, char** argv)
{
	int domid=getDomid();//exec(R"(python3 -c 'from pyxs import Client;c=Client(xen_bus_path="/dev/xen/xenbus");c.connect();print((c.read("domid".encode())).decode());c.close()')"); 
 
    printf("domid %d\n",domid);
    return 0;


}