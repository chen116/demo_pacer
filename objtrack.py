from imutils.video import VideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS

import argparse
import datetime
import imutils
import time
import cv2
import numpy as np


from tkinter import *
master = Tk()
w = 1000 # width for the Tk root
h = 50 # height for the Tk root
# get screen width and height
ws = master.winfo_screenwidth() # width of the screen
hs = master.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs)-h*2
# set the dimensions of the screen 
# and where it is placed
master.geometry('%dx%d+%d+%d' % (w, h, x, y))
sched_var = StringVar()
sched_var.set("hii")
sched_label = Label(master, textvariable=sched_var,fg = "blue",bg = "white")
sched_label.pack(side=LEFT)

anchors_var = StringVar()
anchors_var.set("Resource:")
anchors_label = Label(master, textvariable=anchors_var,font = "Verdana 10 bold" )
anchors_label.pack(side=LEFT)
anchors_options = [
    ("aimd", 1),
    ("50%",0),
    ("100%", 2),
    ("aimd-r", 4),
    ("apid", 3)
]
checked = IntVar()
checked.set(0) # initialize
previous_checked = checked.get()

for text, mode in anchors_options:
    b = Radiobutton(master, text=text,variable=checked, value=mode)
    b.pack(side=LEFT)


frame_var = StringVar()
frame_var.set(" | Freq:")
frame_label = Label(master, textvariable=frame_var,font = "Verdana 10 bold" )
frame_label.pack(side=LEFT)
FSIZE = [
    ("L", 6),
    ("M", 4),
    ("H", 3)
]
w1 = IntVar()
w1.set(FSIZE[0][1]) # initialize
previous_freq = w1.get()
for text, mode in FSIZE:
    b = Radiobutton(master, text=text,variable=w1, value=mode)
    b.pack(side=LEFT)




import heartbeat
import host_guest_comm
window_size_hr=12
hb = heartbeat.Heartbeat(1024,window_size_hr,100,"vic.log",10,100)
monitoring_items = ["heart_rate","app_mode","frame_size","timeslice"]
comm = host_guest_comm.DomU(monitoring_items)





# # construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("-w", "--width", type=int, default=500, help="im show width")
args = vars(ap.parse_args())



# vs= FileVideoStream(args["video"]).start()
# time.sleep(1.0)

# print('what')
# while vs.more():
#     timer = cv2.getTickCount()
#     frame = vs.read()
#     frame = imutils.resize(frame, width=300)

#     cv2.imshow("vid Feed", frame)
#     cvfps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
#     print(cvfps)



# exit()

 
# # if the video argument is None, then we are reading from webcam
# if args.get("video", None) is None:
#     vs = VideoStream(src=0).start()
#     time.sleep(2.0)
 
# # otherwise, we are reading from a video file
# else:
#     vs = cv2.VideoCapture(args["video"])
 




if "mp4" in args["video"]:
    hh=360
    ww=480

else:
    hh=144
    ww=176

car_len = 75
blank_len = 25
rollback_len = 50
car = np.zeros((car_len,hh,ww,3),dtype=np.uint8)
blank = np.zeros((blank_len,hh,ww,3),dtype=np.uint8)
rollback = np.zeros((rollback_len,hh,ww,3),dtype=np.uint8)


vs= FileVideoStream(args["video"]).start()
time.sleep(1.0)
for i in range(250):#blank_len+car_len):
    frame = vs.read()
    if i<car_len:
        car[i,:,:,:]=frame
    elif i < blank_len+car_len:
        blank[i-car_len,:,:,:]=frame
    elif i >= 200:
        rollback[i-200,:,:,:]=frame


vs.stop()   

vidarray = np.concatenate((car,blank,rollback,car,blank,rollback),axis=0)


# vs = FileVideoStream(args["video"]).start()
# time.sleep(1.0)

# initialize the first frame in the video stream
firstFrame = None

fps = FPS().start()

# loop over the frames of the video
# while vs.more():
t_open=False
f_open=False
ctn=0
for frame in vidarray:
    print("frame:",ctn)
    ctn+=1
    timer = cv2.getTickCount()

    # grab the current frame and initialize the occupied/unoccupied
    # text
    # frame = vs.read()

    # frame = frame if args.get("video", None) is None else frame[1]
    text = "no car"
 
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break
 
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=args["width"])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
 
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue
 
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "car detected"#str(len(cnts))
    # draw the text and timestamp on the frame
    cv2.putText(frame, "-> {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
    #     (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
    # show the frame and record if the user presses a key
    cv2.namedWindow( "Thresh");
    cv2.namedWindow( "Frame Delta" );

    cv2.imshow("Obj Tracking", frame)
    if text == "no car":
        cv2.destroyWindow("Thresh")
        cv2.destroyWindow("Frame Delta")
    else:
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)


    # print(cv2.getTickFrequency() / (cv2.getTickCount() - timer))
    fps.update()

    key = cv2.waitKey(1) & 0xFF
 
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
    if key == ord("t"):
        t_open=not t_open
    if key == ord("f"):
        f_open=not f_open


    # if t_open:
    #     cv2.namedWindow( "Thresh");
    #     cv2.imshow("Thresh", thresh)
    # else:
    #     cv2.namedWindow( "Thresh");
    #     cv2.destroyWindow("Thresh")
    # if f_open:
    #     cv2.namedWindow( "Frame Delta" );
    #     cv2.imshow("Frame Delta", frameDelta)
    # else:
    #     cv2.namedWindow( "Frame Delta" );
    #     cv2.destroyWindow("Frame Delta")

    hb.heartbeat_beat()
    print("get_instant_heartrate:",hb.get_instant_heartrate())
    print("get_window_heartrate:",hb.get_window_heartrate())
    print("get_global_heartrate:",hb.get_global_heartrate())
    if ctn%window_size_hr==0:
        comm.write("heart_rate", hb.get_window_heartrate())
    master.update_idletasks()
    master.update()


hb.heartbeat_finish()
 
# cleanup the camera and close any open windows
fps.stop()
vs.stop() #if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
comm.write("heart_rate", "done")


# import cv2
# import sys
 
# (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
# print(major_ver,minor_ver,subminor_ver)

# # Set up tracker.
# # Instead of MIL, you can also use

# tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE']
# tracker_type = tracker_types[2]

# if int(minor_ver) < 3:
#     tracker = cv2.Tracker_create(tracker_type)
# else:
#     if tracker_type == 'BOOSTING':
#         tracker = cv2.TrackerBoosting_create()
#     if tracker_type == 'MIL':
#         tracker = cv2.TrackerMIL_create()
#     if tracker_type == 'KCF':
#         tracker = cv2.TrackerKCF_create()
#     if tracker_type == 'TLD':
#         tracker = cv2.TrackerTLD_create()
#     if tracker_type == 'MEDIANFLOW':
#         tracker = cv2.TrackerMedianFlow_create()
#     if tracker_type == 'GOTURN':
#         tracker = cv2.TrackerGOTURN_create()
#     if tracker_type == 'MOSSE':
#         tracker = cv2.TrackerMOSSE_create()

# # Read video
# video = cv2.VideoCapture("walkman.mp4")

# # Exit if video not opened.
# if not video.isOpened():
#     print("Could not open video")
#     sys.exit()

# # Read first frame.
# ok, frame = video.read()
# if not ok:
#     print('Cannot read video file')
#     sys.exit()
 
# # Define an initial bounding box
# # bbox = (287, 23, 86, 320)
# bbox = (80, 24, 70, 320)

# # Uncomment the line below to select a different bounding box
# # bbox = cv2.selectROI(frame, False)

# # Initialize tracker with first frame and bounding box
# ok = tracker.init(frame, bbox)
# cnt= -1
# while True:
#     cnt+=1
#     # Read a new frame
#     ok, frame = video.read()
#     if not ok:
#         break
     
#     # Start timer
#     timer = cv2.getTickCount()

#     # Update tracker
#     if cnt%1==0:
#         ok, bbox = tracker.update(frame)

#         # Calculate Frames per second (FPS)
#         fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

#     # Draw bounding box
#     if ok:
#         # Tracking success
#         p1 = (int(bbox[0]), int(bbox[1]))
#         p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
#         cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
#     else :
#         # Tracking failure
#         cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

#     # Display tracker type on frame
#     cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
 
#     # Display FPS on frame
#     cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

#     # Display result
#     cv2.imshow("Tracking", frame)
#     print(fps)

#     # Exit if ESC pressed
#     k = cv2.waitKey(1) & 0xff
#     if k == 27 : break