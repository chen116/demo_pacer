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
static const char* about =
"This sample uses You only look once (YOLO)-Detector (https://arxiv.org/abs/1612.08242) to detect objects on camera/video/image.\n"
"Models can be downloaded here: https://pjreddie.com/darknet/yolo/\n"
"Default network is 416x416.\n"
"Class names can be downloaded here: https://github.com/pjreddie/darknet/tree/master/data\n";
static const char* params =
"{ help           | false | print usage         }"
"{ cfg            |  yolov2-tiny.cfg   | model configuration }"
"{ model          |    yolov2-tiny.weights   | model weights       }"
"{ camera_device  | 0     | camera device number}"
"{ source         |  rollcar.3gp    | video or image for detection}"
"{ out            |       | path to output video file}"
"{ fps            | 3     | frame per second }"
"{ style          | box   | box or line style draw }"
"{ min_confidence | 0.24  | min confidence      }"
"{ class_names    |  coco.names   | File with class names, [PATH-TO-DARKNET]/data/coco.names }";






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
#include <string>
#include <iterator>

#include <heartbeats/heartbeat.h>

heartbeat_t* heart;
static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;

#include <vector>

extern "C" char * xenstore_read(struct xs_handle*  ,xs_transaction_t , const char*  , unsigned int * );
extern "C" int xenstore_write(struct xs_handle *h, xs_transaction_t t, const char *path, const void *data);

int main(int argc, char** argv)
{

//yolo
CommandLineParser parser(argc, argv, params);
if (parser.get<bool>("help"))
{
    cout << about << endl;
    parser.printMessage();
    return 0;
}
String modelConfiguration = parser.get<String>("cfg");
String modelBinary = parser.get<String>("model");
cout<<modelBinary<<" "<<modelConfiguration <<endl;
dnn::Net net = readNetFromDarknet(modelConfiguration, modelBinary);
if (net.empty())
{
    cerr << "Can't load network by using the following files: " << endl;
    cerr << "cfg-file:     " << modelConfiguration << endl;
    cerr << "weights-file: " << modelBinary << endl;
    cerr << "Models can be downloaded here:" << endl;
    cerr << "https://pjreddie.com/darknet/yolo/" << endl;
    exit(-1);
}
VideoCapture cap;
VideoWriter writer;
int codec = CV_FOURCC('M', 'J', 'P', 'G');
double fps = parser.get<float>("fps");
if (parser.get<String>("source").empty())
{
    int cameraDevice = parser.get<int>("camera_device");
    cap = VideoCapture(cameraDevice);
    if(!cap.isOpened())
    {
        cout << "Couldn't find camera: " << cameraDevice << endl;
        return -1;
    }
}
else
{
    cap.open(parser.get<String>("source"));
    if(!cap.isOpened())
    {
        cout << "Couldn't open image or video: " << parser.get<String>("video") << endl;
        return -1;
    }
}
if(!parser.get<String>("out").empty())
{
    writer.open(parser.get<String>("out"), codec, fps, Size((int)cap.get(CAP_PROP_FRAME_WIDTH),(int)cap.get(CAP_PROP_FRAME_HEIGHT)), 1);
}
vector<String> classNamesVec;
ifstream classNamesFile(parser.get<String>("class_names").c_str());
if (classNamesFile.is_open())
{
    string className = "";
    while (std::getline(classNamesFile, className))
        classNamesVec.push_back(className);
}
String object_roi_style = parser.get<String>("style");








	system("python3 getDomUid.py > id.txt"); 
	// system(R"(python3 -c 'from pyxs import Client;c=Client(xen_bus_path="/dev/xen/xenbus");c.connect();print((c.read("domid".encode())).decode());c.close()')"); 
	fstream domid_file("id.txt");
	int domid;
	domid_file >> domid;


    char *frame_num_path;
    char *box_path;
	int er;
	unsigned int len;
    struct xs_handle *xs;
    xs_transaction_t th;
    xs = xs_daemon_open();
    frame_num_path = xs_get_domain_path(xs, domid); 
    box_path = xs_get_domain_path(xs, domid);
    frame_num_path = (char*)realloc(frame_num_path, strlen(frame_num_path) + strlen("/frame_number_entry") + 1);
    strcat(frame_num_path, "/frame_number_entry");
    box_path = (char*)realloc(box_path, strlen(box_path) + strlen("/box_entry") + 1);
    strcat(box_path, "/box_entry");

    printf("%s\n",frame_num_path);
	int g;
	char * item;

	while (strcmp("init",item)!=0)
	{
		item = xenstore_read(xs,th,frame_num_path,&len);
	} 

	item = xenstore_read(xs,th,box_path,&len);
	string init_video_data = string(item);
	istringstream iss(item);
	vector<string> init_video_data_vec(std::istream_iterator<std::string>{iss}, std::istream_iterator<std::string>());
	
	int hw_size,lw_size;
	if (init_video_data_vec[0]=="init")
	{
		hw_size=stoi(init_video_data_vec[1]);
		lw_size=stoi(init_video_data_vec[2]);
	}
	vector<int> vidarray_binary;
    std::stringstream ss(init_video_data_vec[3]);
    int i;
    while (ss >> i)
    {
        vidarray_binary.push_back(i);
        if (ss.peek() == ',') ss.ignore();
    }
    for (i=0; i< vidarray_binary.size(); i++)
        std::cout << vidarray_binary.at(i)<<std::endl;
	cout <<endl;


vector<Mat> car;
vector<Mat> no_car;
for (int k = 0; k < 200; ++k)
{
    Mat frame;
    cap >> frame;
    if (k>=20 and k <50)
    {
        car.push_back(frame);
    }
    if (k >= 140)
    {
        no_car.push_back(frame);
    }
    /* code */
}
vector<Mat> flipcar = car; 
reverse(flipcar.begin(),flipcar.end());
for (int k=0;k<flipcar.size();k++)
{
    car.push_back(flipcar[k]);
}

std::vector<Mat> vidarray;
for (i=0; i< vidarray_binary.size(); i++)
{
	if (vidarray_binary.at(i))
	{
		for (int k=0; k< car.size(); k++) vidarray.push_back(car.at(k));
	}
	else
	{
		for (int k=0; k< no_car.size(); k++) vidarray.push_back(no_car.at(k));
	}
}

string box_coords = "0 0 0 0";
xenstore_write(xs, th, box_path, box_coords.c_str());
xenstore_write(xs, th, frame_num_path, "ready");

int frame_num;
item = xenstore_read(xs,th,frame_num_path,&len);
int prev_frame_num = -1;
int frame_size = vidarray_binary[0];
int detect_car = vidarray_binary[0];
int prev_frame_size = 0;


while (strcmp("done",item)!=0)
{
	frame_num = atoi(item);
	if (frame_num > prev_frame_num) 
	{
		cout << frame_num << endl;
		prev_frame_num = frame_num;









	}
	






	item=xenstore_read(xs,th,frame_num_path,&len);
}



// Mat new_img;
// resize(frame, new_frame, cv::Size(), frame_size/176, frame_size/176);


	return 0;

}

// int main(int argc, char** argv)
// {

// //get domu id.
// 	system("python3 getDomUid.py > id.txt"); 
// // system(R"(python3 -c 'from pyxs import Client;c=Client(xen_bus_path="/dev/xen/xenbus");c.connect();print((c.read("domid".encode())).decode());c.close()')"); 
// 	fstream domid_file("id.txt");
// 	int domid;
// 	domid_file >> domid;

//     char *path;
// 	int er;
// 	char * buf;
// 	// unsigned int *len =  (unsigned int*) malloc(sizeof(unsigned int));
// 	// int len = 42;

// 	unsigned int len;


//     struct xs_handle *xs;
//     xs_transaction_t th;
//     xs = xs_daemon_open();

//     path = xs_get_domain_path(xs, domid); 
//     path = (char*)realloc(path, strlen(path) + strlen("/frame_number_entry") + 1);
//     strcat(path, "/frame_number_entry");
//     printf("%s\n",path);
//     while (strcmp(buf,"init"))//buf[0]!='i')
//     {
//     	buf = cpp_xs_read(xs, th, path, &len);
//   //   	th = xs_transaction_start(xs);
// 		// buf = xs_read(xs, th, path, len);
//   //   	xs_transaction_end(xs, th, false);

//     }
//     cout << buf;

//     heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);
        

//     heartbeat(heart, 1);
//     printf("heartbeat: instant rate: %f\n",hb_get_instant_rate(heart) );
//     char hr_str[10];
//     gcvt(hb_get_instant_rate(heart) , 8, hr_str);


// heartbeat_finish(heart);
// xs_daemon_close(xs);
// free(path);
// // free(len);

// return 0;


// }