//rief Sample of using OpenCV dnn module in real time with device capture, video and image.
// VIDEO DEMO: https://www.youtube.com/watch?v=NHtRlndE2cg
//https://docs.opencv.org/3.4.1/da/d9d/tutorial_dnn_yolo.html



// able to cut vid frame
//resize()
//automatic know its VM's id, sort of, better to do inline
// get coordinates:



#include <opencv2/dnn.hpp>
#include <opencv2/dnn/shape_utils.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <fstream>
#include <iostream>
using namespace std;
using namespace cv;
using namespace cv::dnn;




#include <stdlib.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <xenstore.h>
#ifdef __cplusplus
}
#endif
#include <cstdlib>
#include <fstream>
#include <iostream>


#include <heartbeats/heartbeat.h>
#include <string.h>
heartbeat_t* heart;
static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;

#include <vector>



extern "C" char * cpp_xs_read(xs_handle* xs ,xs_transaction_t th, const char* path , unsigned int *len)
{
	char * buf;
	th = xs_transaction_start(xs);
	buf = xs_read(xs, th, path, len);
    xs_transaction_end(xs, th, false);

    return buf;
}

int main(int argc, char** argv)
{

//get domu id.
	system("python3 getDomUid.py > id.txt"); 
// system(R"(python3 -c 'from pyxs import Client;c=Client(xen_bus_path="/dev/xen/xenbus");c.connect();print((c.read("domid".encode())).decode());c.close()')"); 
	fstream domid_file("id.txt");
	int domid;
	domid_file >> domid;

    char *path;
	int er;
	char * buf;
	// unsigned int *len =  (unsigned int*) malloc(sizeof(unsigned int));
	// int len = 42;

	unsigned int len;


    struct xs_handle *xs;
    xs_transaction_t th;
    xs = xs_daemon_open();

    path = xs_get_domain_path(xs, domid); 
    path = (char*)realloc(path, strlen(path) + strlen("/frame_number_entry") + 1);
    strcat(path, "/frame_number_entry");
    printf("%s\n",path);
    while (strcmp(buf,"init"))//buf[0]!='i')
    {
    	buf = cpp_xs_read(xs, th, path, &len);
  //   	th = xs_transaction_start(xs);
		// buf = xs_read(xs, th, path, len);
  //   	xs_transaction_end(xs, th, false);

    }
    cout << buf;

    heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);
        

    heartbeat(heart, 1);
    printf("heartbeat: instant rate: %f\n",hb_get_instant_rate(heart) );
    char hr_str[10];
    gcvt(hb_get_instant_rate(heart) , 8, hr_str);


heartbeat_finish(heart);
xs_daemon_close(xs);
free(path);
free(len);

return 0;


}