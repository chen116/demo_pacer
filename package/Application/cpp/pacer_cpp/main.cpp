#include "pacer.h"

#include <stdio.h>
// mypacer.heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);
// mypacer.domid = getDomid();  
// mypacer.xs = xs_daemon_open();
// mypacer.base_path = xs_get_domain_path(xs, domid);





int main(int argc, char** argv)
{

	// init_pacer() 
	// add_entry()
	// heartbeat()
	// send()
	// finish()

	Pacer mypacer;
	printf("%d\n",mypacer.getDomid() );
	mypacer.setItem("box_entry");
	mypacer.getItems();


	heartbeat(mypacer.heart, 1);

	printf("%s\n",mypacer.readItem("box_entry"));
	printf("%s\n",mypacer.readHeartRate());
	heartbeat(mypacer.heart, 1);
	mypacer.writeHeartRate();
	printf("%s\n",mypacer.readHeartRate());

	// int domid=getDomid();//exec(R"(python3 -c 'from pyxs import Client;c=Client(xen_bus_path="/dev/xen/xenbus");c.connect();print((c.read("domid".encode())).decode());c.close()')"); 
 //    printf("domid %d\n",domid);
 //    mypacer.domid = domid;
 //    printf("mypacer id %d\n",mypacer.domid );



    // heartbeat_finish(mypacer.heart);


    return 0;


}