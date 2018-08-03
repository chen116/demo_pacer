// Brief Sample of using OpenCV dnn module in real time with device capture, video and image.
// VIDEO DEMO: https://www.youtube.com/watch?v=NHtRlndE2cg
//https://docs.opencv.org/3.4.1/da/d9d/tutorial_dnn_yolo.html



// able to cut vid frame
//automatic know its VM1 id


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


#include <heartbeats/heartbeat.h>
#include <string.h>
heartbeat_t* heart;
static const int64_t vic_win_size = 10;
static const int64_t vic_buf_depth = 1000;
static const char* vic_log_file ="vic.log";
static const int64_t vic_min_target = 100;
static const int64_t vic_max_target = 1000;
int main(int argc, char** argv)
{


system("python3 getDomUid.py > id.txt"); 
// system(R"(python3 -c 'from pyxs import Client;c=Client(xen_bus_path="/dev/xen/xenbus");c.connect();print((c.read("domid".encode())).decode());c.close()')"); 
fstream domid_file("id.txt");
int domid;
domid_file >> domid;


    char *path;
    int er;
    struct xs_handle *xs;
    xs_transaction_t th;
    xs = xs_daemon_open();
    path = xs_get_domain_path(xs, domid); 
    path = (char*)realloc(path, strlen(path) + strlen("/heart_rate") + 1);
    if ( path == NULL ) printf("not good\n");
    strcat(path, "/heart_rate");
    printf("%s\n",path);
    heart = heartbeat_init(vic_win_size, vic_buf_depth, vic_log_file, vic_min_target, vic_max_target);

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
    for(;;)
    {
        heartbeat(heart, 1);
        printf("heartbeat: instant rate: %f\n",hb_get_instant_rate(heart) );
        char hr_str[10];
        gcvt(hb_get_instant_rate(heart) , 8, hr_str);
        th = xs_transaction_start(xs);
        er = xs_write(xs, th, path, hr_str, strlen(hr_str));
        xs_transaction_end(xs, th, false);

        Mat frame;
        cap >> frame; // get a new frame from camera/video or read image
        if (frame.empty())
        {
            waitKey();
            break;
        }
        if (frame.channels() == 4)
            cvtColor(frame, frame, COLOR_BGRA2BGR);
        Mat inputBlob = blobFromImage(frame, 1 / 255.F, Size(416, 416), Scalar(), true, false); //Convert Mat to batch of images
        net.setInput(inputBlob, "data");                   //set the network input
        Mat detectionMat = net.forward("detection_out");   //compute output
        vector<double> layersTimings;
        double tick_freq = getTickFrequency();
        double time_ms = net.getPerfProfile(layersTimings) / tick_freq * 1000;
        putText(frame, format("FPS: %.2f ; time: %.2f ms", 1000.f / time_ms, time_ms),
                Point(20, 20), 0, 0.5, Scalar(0, 0, 255));
        float confidenceThreshold = parser.get<float>("min_confidence");
        for (int i = 0; i < detectionMat.rows; i++)
        {
            const int probability_index = 5;
            const int probability_size = detectionMat.cols - probability_index;
            float *prob_array_ptr = &detectionMat.at<float>(i, probability_index);
            size_t objectClass = max_element(prob_array_ptr, prob_array_ptr + probability_size) - prob_array_ptr;
            float confidence = detectionMat.at<float>(i, (int)objectClass + probability_index);
            if (confidence > confidenceThreshold)
            {
                float x_center = detectionMat.at<float>(i, 0) * frame.cols;
                float y_center = detectionMat.at<float>(i, 1) * frame.rows;
                float width = detectionMat.at<float>(i, 2) * frame.cols;
                float height = detectionMat.at<float>(i, 3) * frame.rows;
                Point p1(cvRound(x_center - width / 2), cvRound(y_center - height / 2));
                Point p2(cvRound(x_center + width / 2), cvRound(y_center + height / 2));
                Rect object(p1, p2);
                Scalar object_roi_color(0, 255, 0);
                if (object_roi_style == "box")
                {
                    rectangle(frame, object, object_roi_color);
                }
                else
                {
                    Point p_center(cvRound(x_center), cvRound(y_center));
                    line(frame, object.tl(), p_center, object_roi_color, 1);
                }
                String className = objectClass < classNamesVec.size() ? classNamesVec[objectClass] : cv::format("unknown(%d)", objectClass);
                String label = format("%s: %.2f", className.c_str(), confidence);
                int baseLine = 0;
                Size labelSize = getTextSize(label, FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);
                rectangle(frame, Rect(p1, Size(labelSize.width, labelSize.height + baseLine)),
                          object_roi_color, FILLED);
                putText(frame, label, p1 + Point(0, labelSize.height),
                        FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0,0,0));
            }
        }
        if(writer.isOpened())
        {
            writer.write(frame);
        }
        imshow("YOLO: Detections", frame);
        if (waitKey(1) >= 0) break;
    }
    heartbeat_finish(heart);
xs_daemon_close(xs);
free(path);
    return 0;
} // main