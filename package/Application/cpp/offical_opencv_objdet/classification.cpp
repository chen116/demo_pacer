//g++ cobj.cpp -o app `pkg-config --cflags --libs opencv` -std=c++11 





#include <opencv2/dnn.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/core/utils/trace.hpp>
using namespace cv;
using namespace cv::dnn;
#include <fstream>
#include <iostream>
#include <cstdlib>
using namespace std;
void postprocess(Mat& frame, const std::vector<Mat>& outs, Net& net)
{
    float confThreshold = 0.5;
    static std::vector<int> outLayers = net.getUnconnectedOutLayers();
    static std::string outLayerType = net.getLayer(outLayers[0])->type;

    std::vector<int> classIds;
    std::vector<float> confidences;
    std::vector<Rect> boxes;
    cout << outLayerType << endl;
    if (net.getLayer(0)->outputNameToIndex("im_info") != -1)  // Faster-RCNN or R-FCN
    {
        // Network produces output blob with a shape 1x1xNx7 where N is a number of
        // detections and an every detection is a vector of values
        // [batchId, classId, confidence, left, top, right, bottom]
        CV_Assert(outs.size() == 1);
        float* data = (float*)outs[0].data;
        for (size_t i = 0; i < outs[0].total(); i += 7)
        {
            float confidence = data[i + 2];
            if (confidence > confThreshold)
            {
                int left = (int)data[i + 3];
                int top = (int)data[i + 4];
                int right = (int)data[i + 5];
                int bottom = (int)data[i + 6];
                int width = right - left + 1;
                int height = bottom - top + 1;
                classIds.push_back((int)(data[i + 1]) - 1);  // Skip 0th background class id.
                boxes.push_back(Rect(left, top, width, height));
                confidences.push_back(confidence);
            }
        }
    }
    else if (outLayerType == "DetectionOutput")
    {
        // Network produces output blob with a shape 1x1xNx7 where N is a number of
        // detections and an every detection is a vector of values
        // [batchId, classId, confidence, left, top, right, bottom]
        CV_Assert(outs.size() == 1);
        float* data = (float*)outs[0].data;
        for (size_t i = 0; i < outs[0].total(); i += 7)
        {
            float confidence = data[i + 2];
            if (confidence > confThreshold)
            {
                int left = (int)(data[i + 3] * frame.cols);
                int top = (int)(data[i + 4] * frame.rows);
                int right = (int)(data[i + 5] * frame.cols);
                int bottom = (int)(data[i + 6] * frame.rows);
                int width = right - left + 1;
                int height = bottom - top + 1;
                classIds.push_back((int)(data[i + 1]) - 1);  // Skip 0th background class id.
                boxes.push_back(Rect(left, top, width, height));
                confidences.push_back(confidence);
            }
        }
    }
    else if (outLayerType == "Region")
    {
        for (size_t i = 0; i < outs.size(); ++i)
        {
            // Network produces output blob with a shape NxC where N is a number of
            // detected objects and C is a number of classes + 4 where the first 4
            // numbers are [center_x, center_y, width, height]
            float* data = (float*)outs[i].data;
            for (int j = 0; j < outs[i].rows; ++j, data += outs[i].cols)
            {
                Mat scores = outs[i].row(j).colRange(5, outs[i].cols);
                Point classIdPoint;
                double confidence;
                minMaxLoc(scores, 0, &confidence, 0, &classIdPoint);
                if (confidence > confThreshold)
                {
                    int centerX = (int)(data[0] * frame.cols);
                    int centerY = (int)(data[1] * frame.rows);
                    int width = (int)(data[2] * frame.cols);
                    int height = (int)(data[3] * frame.rows);
                    int left = centerX - width / 2;
                    int top = centerY - height / 2;

                    classIds.push_back(classIdPoint.x);
                    confidences.push_back((float)confidence);
                    boxes.push_back(Rect(left, top, width, height));
                }
            }
        }
    }
    else
        CV_Error(Error::StsNotImplemented, "Unknown output layer type: " + outLayerType);

    // std::vector<int> indices;
    // NMSBoxes(boxes, confidences, confThreshold, nmsThreshold, indices);
    // for (size_t i = 0; i < indices.size(); ++i)
    // {
    //     int idx = indices[i];
    //     Rect box = boxes[idx];
    //     drawPred(classIds[idx], confidences[idx], box.x, box.y,
    //              box.x + box.width, box.y + box.height, frame);
    // }
}


std::vector<String> getOutputsNames(const Net& net)
{
    static std::vector<String> names;
    if (names.empty())
    {
        std::vector<int> outLayers = net.getUnconnectedOutLayers();
        std::vector<String> layersNames = net.getLayerNames();
        names.resize(outLayers.size());
        for (size_t i = 0; i < outLayers.size(); ++i)
        {
            names[i] = layersNames[outLayers[i] - 1];
            cout << outLayers[i] <<endl;
        }
    }
    return names;
}


/* Find best class for the blob (i. e. class with maximal probability) */
static void getMaxClass(const Mat &probBlob, int *classId, double *classProb)
{
    Mat probMat = probBlob.reshape(1, 1); //reshape the blob to 1x1000 matrix
    Point classNumber;
    minMaxLoc(probMat, NULL, classProb, NULL, &classNumber);
    *classId = classNumber.x;
}
static std::vector<String> readClassNames(const char *filename )
{
    std::vector<String> classNames;
    std::ifstream fp(filename);
    if (!fp.is_open())
    {
        std::cerr << "File with classes labels not found: " << filename << std::endl;
        exit(-1);
    }
    std::string name;
    while (!fp.eof())
    {
        std::getline(fp, name);
        if (name.length())
            classNames.push_back( name.substr(name.find(' ')+1) );
    }
    fp.close();
    return classNames;
}
const char* params
    = "{ help           | false | Sample app for loading googlenet model }"
      "{ proto          | ./bvlc_googlenet.prototxt | model configuration }"
      "{ model          | ./bvlc_googlenet.caffemodel | model weights }"
      "{ label          | synset_words.txt | names of ILSVRC2012 classes }"
      "{ image          | space_shuttle.jpg | path to image file }"
      "{ opencl         | false | enable OpenCL }"
;
int main(int argc, char **argv)
{
    CV_TRACE_FUNCTION();
    CommandLineParser parser(argc, argv, params);
    if (parser.get<bool>("help"))
    {
        parser.printMessage();
        return 0;
    }
    String modelTxt = parser.get<string>("proto");
    String modelBin = parser.get<string>("model");
    String imageFile = parser.get<String>("image");
    String classNameFile = parser.get<String>("label");
    Net net;
    try {
        net = dnn::readNetFromCaffe(modelTxt, modelBin);
    }
    catch (const cv::Exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
        if (net.empty())
        {
            std::cerr << "Can't load network by using the following files: " << std::endl;
            std::cerr << "prototxt:   " << modelTxt << std::endl;
            std::cerr << "caffemodel: " << modelBin << std::endl;
            std::cerr << "bvlc_googlenet.caffemodel can be downloaded here:" << std::endl;
            std::cerr << "http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel" << std::endl;
            exit(-1);
        }
    }
    if (parser.get<bool>("opencl"))
    {
        net.setPreferableTarget(DNN_TARGET_OPENCL);
    }
    Mat img = imread(imageFile);
    if (img.empty())
    {
        std::cerr << "Can't read image from the file: " << imageFile << std::endl;
        exit(-1);
    }
    //GoogLeNet accepts only 224x224 BGR-images
    Mat inputBlob = blobFromImage(img, 1.0f, Size(224, 224),
                                  Scalar(104, 117, 123), false);   //Convert Mat to batch of images
    

    net.setInput(inputBlob, "data");        //set the network input
    Mat prob = net.forward("detect");         //compute output



    // int midx, npairs;
    // int nparts = hi.size[1];
    // int H = hi.size[2];
    // int W = hi.size[3];
    // cout << nparts << " " << H<<" "<<W <<endl;


            net.setInput(inputBlob);        //set the network input
            std::vector<Mat> outs;
            net.forward(outs, getOutputsNames(net));
            postprocess(img, outs, net);

    cv::TickMeter t;

    for (int i = 0; i < 10; i++)
    {
        CV_TRACE_REGION("forward");
        net.setInput(inputBlob, "data");        //set the network input
        t.start();
        prob = net.forward("prob");                          //compute output


        t.stop();
    }
    int classId;
    double classProb;
    getMaxClass(prob, &classId, &classProb);//find the best class
    std::vector<String> classNames = readClassNames(classNameFile.c_str());
    std::cout << "Best class: #" << classId << " '" << classNames.at(classId) << "'" << std::endl;
    std::cout << "Probability: " << classProb * 100 << "%" << std::endl;
    std::cout << "Time: " << (double)t.getTimeMilli() / t.getCounter() << " ms (average from " << t.getCounter() << " iterations)" << std::endl;
    return 0;
} //main
// //g++ cobj.cpp -o app `pkg-config --cflags --libs opencv` -std=c++11 





// #include <opencv2/dnn.hpp>
// #include <opencv2/imgproc.hpp>
// #include <opencv2/highgui.hpp>
// #include <opencv2/core/utils/trace.hpp>
// using namespace cv;
// using namespace cv::dnn;
// #include <fstream>
// #include <iostream>
// #include <cstdlib>
// using namespace std;
// /* Find best class for the blob (i. e. class with maximal probability) */
// static void getMaxClass(const Mat &probBlob, int *classId, double *classProb)
// {
//     Mat probMat = probBlob.reshape(1, 1); //reshape the blob to 1x1000 matrix
//     Point classNumber;
//     minMaxLoc(probMat, NULL, classProb, NULL, &classNumber);
//     *classId = classNumber.x;
// }
// static std::vector<String> readClassNames(const char *filename )
// {
//     std::vector<String> classNames;
//     std::ifstream fp(filename);
//     if (!fp.is_open())
//     {
//         std::cerr << "File with classes labels not found: " << filename << std::endl;
//         exit(-1);
//     }
//     std::string name;
//     while (!fp.eof())
//     {
//         std::getline(fp, name);
//         if (name.length())
//             classNames.push_back( name.substr(name.find(' ')+1) );
//     }
//     fp.close();
//     return classNames;
// }
// const char* params
//     = "{ help           | false | Sample app for loading googlenet model }"
//       "{ proto          | ./bvlc_googlenet.prototxt | model configuration }"
//       "{ model          | ./bvlc_googlenet.caffemodel | model weights }"
//       "{ label          | synset_words.txt | names of ILSVRC2012 classes }"
//       "{ image          | space_shuttle.jpg | path to image file }"
//       "{ opencl         | false | enable OpenCL }"
// ;
// int main(int argc, char **argv)
// {
//     CV_TRACE_FUNCTION();
//     CommandLineParser parser(argc, argv, params);
//     if (parser.get<bool>("help"))
//     {
//         parser.printMessage();
//         return 0;
//     }
//     String modelTxt = parser.get<string>("proto");
//     String modelBin = parser.get<string>("model");
//     String imageFile = parser.get<String>("image");
//     String classNameFile = parser.get<String>("label");
//     Net net;
//     try {
//         net = dnn::readNetFromCaffe(modelTxt, modelBin);
//     }
//     catch (const cv::Exception& e) {
//         std::cerr << "Exception: " << e.what() << std::endl;
//         if (net.empty())
//         {
//             std::cerr << "Can't load network by using the following files: " << std::endl;
//             std::cerr << "prototxt:   " << modelTxt << std::endl;
//             std::cerr << "caffemodel: " << modelBin << std::endl;
//             std::cerr << "bvlc_googlenet.caffemodel can be downloaded here:" << std::endl;
//             std::cerr << "http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel" << std::endl;
//             exit(-1);
//         }
//     }
//     if (parser.get<bool>("opencl"))
//     {
//         net.setPreferableTarget(DNN_TARGET_OPENCL);
//     }
//     Mat img = imread(imageFile);
//     if (img.empty())
//     {
//         std::cerr << "Can't read image from the file: " << imageFile << std::endl;
//         exit(-1);
//     }
//     //GoogLeNet accepts only 224x224 BGR-images
//     Mat inputBlob = blobFromImage(img, 1.0f, Size(224, 224),
//                                   Scalar(104, 117, 123), false);   //Convert Mat to batch of images
    

//     net.setInput(inputBlob, "data");        //set the network input
//     Mat prob = net.forward("prob");         //compute output
//  net.setInput(inputBlob, "data");        //set the network input
//     Mat hi = net.forward();

//     int midx, npairs;
//     int nparts = hi.size[1];
//     int H = hi.size[2];
//     int W = hi.size[3];
//     cout << nparts << " " << H<<" "<<W <<endl;

//     cv::TickMeter t;

//     for (int i = 0; i < 10; i++)
//     {
//         CV_TRACE_REGION("forward");
//         net.setInput(inputBlob, "data");        //set the network input
//         t.start();
//         prob = net.forward("prob");                          //compute output


//         t.stop();
//     }
//     int classId;
//     double classProb;
//     getMaxClass(prob, &classId, &classProb);//find the best class
//     std::vector<String> classNames = readClassNames(classNameFile.c_str());
//     std::cout << "Best class: #" << classId << " '" << classNames.at(classId) << "'" << std::endl;
//     std::cout << "Probability: " << classProb * 100 << "%" << std::endl;
//     std::cout << "Time: " << (double)t.getTimeMilli() / t.getCounter() << " ms (average from " << t.getCounter() << " iterations)" << std::endl;
//     return 0;
// } //main