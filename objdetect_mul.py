from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import threading 
from queue import Queue



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
window_size_hr=6
hb = heartbeat.Heartbeat(1024,window_size_hr,100,"vic.log",10,100)
monitoring_items = ["heart_rate","app_mode","frame_size","timeslice"]
comm = host_guest_comm.DomU(monitoring_items)




ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())


# COLORS=np.array([[5,200,250]])
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

tracking_target = ["cat","person","car","dog"]  # outvid # fastcat
COLORS = np.random.uniform(100, 255, size=(len(CLASSES), 3))


net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")




























class Workers(threading.Thread):
	def __init__(self,threadLock,every_n_frame,thread_id,input_q,output_q):
		threading.Thread.__init__(self)
		self.net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
		self.thread_id=thread_id
		self.input_q=input_q
		self.output_q=output_q
		self.every_n_frame=every_n_frame
		self.n=every_n_frame['n']
		self.threadLock=threadLock
		self.my_every_n_frame_cnt=0
	def run(self):
		# Acquire lock to synchronize thread
		# self.threadLock.acquire()
		while True:

			self.threadLock.acquire()
			self.n = self.every_n_frame['n']
			# self.every_n_frame['cnt']=(self.every_n_frame['cnt']+1)%self.n
			# self.my_every_n_frame_cnt = self.every_n_frame['cnt']
			self.threadLock.release()
			if self.n==-1:
				# self.output_q.put({'cnt':-1})
				break



			stuff = self.input_q.get()

			if stuff['cnt']==-1:
				self.output_q.put({'cnt':-1})
				break
			# self.n = stuff['n']ß
			self.my_every_n_frame_cnt = stuff['cnt']

			blob = stuff['blob']
			if self.my_every_n_frame_cnt%self.n==0:
				self.net.setInput(blob)


				net_result=self.net.forward()
				self.output_q.put({'blob':net_result,'cnt':stuff['cnt']})
				# self.output_q.put({'blob':-1*np.ones((1,1,1,2)),'cnt':stuff['cnt']})


			else:

				self.output_q.put({'blob':-1*np.ones((1,1,1,2)),'cnt':stuff['cnt']})
			# try:
			# 	stuff = self.input_q.get()

			# 	if stuff['cnt']==-1:
			# 		self.output_q.put({'cnt':-1})
			# 		break
			# 	# self.n = stuff['n']
			# 	self.my_every_n_frame_cnt = stuff['cnt']
			# 	net_result=-1*np.ones((1,1,1,2))
			# 	if self.my_every_n_frame_cnt%self.n==0:
			# 		blob = stuff['blob']
			# 		self.net.setInput(blob)
			# 		net_result=self.net.forward()
			# 	try:
			# 		self.output_q.put({'blob':net_result,'cnt':stuff['cnt']})
			# 	except:
			# 		print(thread_id,"thread not gonna wait put")
			# except:
			# 	print(thread_id,"thread not gonna wait get")

input_q = Queue()  # fps is better if queue is higher but then more lags
output_q = Queue()



threads = []
every_n_frame = {'cnt':-1,'n':w1.get()}
threadLock = threading.Lock()
# total_num_threads = 3 # realvid
total_num_threads = 4 # fastcat
num_threads_exiting = 0


for i in range(total_num_threads):
	tmp_thread = Workers(threadLock,every_n_frame,i,input_q,output_q)
	tmp_thread.start()
	threads.append(tmp_thread)


# prev_box = {}
prev_boxes = []
# loop over the frames from the video stream
cnt=0
output_q_cnt=-1





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

rollforward = np.copy(rollback)
rollforward = np.flipud(rollforward)
carbackword = np.copy(car)

carbackword = np.flipud(carbackword)
vidarray = np.concatenate((blank,blank,car,blank,rollback,car,blank,rollback,car,blank,rollback,car,blank,rollback,car,blank,rollback),axis=0)
vidarray = np.concatenate((blank,blank,car,blank,rollback,rollforward,blank,blank,carbackword,blank,blank,car,blank),axis=0)
# vidarray = np.concatenate((blank,blank,car,blank,blank,car,blank,blank,car),axis=0)





firstFrame = None

for frame in vidarray:

# while vs.more():
	timer = cv2.getTickCount()
	# frame = vs.read()
	frame = imutils.resize(frame, width=300)
	(h, w) = frame.shape[:2]



	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), 127.5)
	threadLock.acquire()
	every_n_frame['n']=w1.get()
	threadLock.release()


	stuff={'blob':blob,'cnt':cnt,'n':w1.get()}
	cnt+=1
	input_q.put(stuff)
	current_freq=w1.get()


    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
    # # if the first frame is None, initialize it
    # if firstFrame is None:
    #     firstFrame = gray
    #     continue
    # # compute the absolute difference between the current frame and
    # # first frame
    # frameDelta = cv2.absdiff(firstFrame, gray)
    # thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
    # # dilate the thresholded image to fill in holes, then find contours
    # # on thresholded image
    # thresh = cv2.dilate(thresh, None, iterations=2)
    # cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    #     cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # for c in cnts:
    #     # if the contour is too small, ignore it
    #     if cv2.contourArea(c) > args["min_area"]:
        	



	if True:#not output_q.empty():
		object_detected = ''
		stuff = output_q.get()
		# stuff=None
		# try:
		# 	stuff = output_q.get_nowait()
		# except:
		# 	print("main not gonna wait get")
		# 	stuff = {'blob':-1*np.ones((1,1,1,2)),'cnt':output_q_cnt}


		# stuff = output_q.get()
		detections = stuff['blob']
		order = stuff['cnt']
		#print('output cnt:',order,'global cnt:',output_q_cnt)
		output_q_cnt+=1



		object_present=0
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
		w1.set(FSIZE[0][1])


		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) > args["min_area"]:
				object_present=1
				w1.set(FSIZE[2][1])






		if object_present:


			if detections[0][0][0][0] == -1:
				if len(prev_boxes)>0:
					for prev_box in prev_boxes:
						startX=prev_box['startX']
						startY=prev_box['startY']
						endX=prev_box['endX']
						endY=prev_box['endY']
						idx=prev_box['idx']
						label=prev_box['label']
						cv2.rectangle(frame, (startX, startY), (endX, endY),
							COLORS[idx], 2)
						y = startY - 15 if startY - 15 > 15 else startY + 15
						cv2.putText(frame, label, (startX, y),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)					
			else:
				prev_boxes=[]
				for i in np.arange(0, detections.shape[2]):
					# extract the confidence (i.e., probability) associated with
					# the prediction
					confidence = detections[0, 0, i, 2]
					idx2 = int(detections[0,0,i,1])
					# filter out weak detections by ensuring the `confidence` is
					# greater than the minimum confidence
					if ((confidence > 0.009) and (CLASSES[idx2] in tracking_target)):
						object_detected = CLASSES[idx2]
						# extract the index of the class label from the
						# `detections`, then compute the (x, y)-coordinates of
						# the bounding box for the object
						# #print('catttttttttttttttttt')
						idx = int(detections[0, 0, i, 1])
						box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
						(startX, startY, endX, endY) = box.astype("int")
					#	#print('startX=',startX)
					#	#print('endX=',endX)

						# label =str(order)+'--'
						label = "{}: {:.2f}%".format(CLASSES[idx],
							confidence * 100)
						cv2.rectangle(frame, (startX, startY), (endX, endY),
							COLORS[idx], 2)
						y = startY - 15 if startY - 15 > 15 else startY + 15
						cv2.putText(frame, label, (startX, y),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
						prev_box = {}
						prev_box['startX']=startX
						prev_box['startY']=startY
						prev_box['endX']=endX
						prev_box['endY']=endY
						prev_box['idx']=idx
						prev_box['label']= label
						prev_boxes.append(prev_box)
						localtrack = 1
						localsearch = 0
						sentlostmessage = 0
						centered = 0		
		# show the output frame
		cv2.imshow("Frame", frame)
		if current_freq!=previous_freq and output_q_cnt%w1.get()==0:
			comm.write("frame_size",current_freq)
			previous_freq=current_freq
		# hb stuff
		# #print("hb: before heartbeat_beat()")
		hb.heartbeat_beat()
		print("get_instant_heartrate:",hb.get_window_heartrate())
		if cnt%window_size_hr==0:
			comm.write("heart_rate", hb.get_window_heartrate())
		# print("get_window_heartrate:",hb.get_window_heartrate())
		# print("get_global_heartrate:",hb.get_global_heartrate())
		master.update_idletasks()
		master.update()




	key = cv2.waitKey(1) & 0xFF
vs.stop() #if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
hb.heartbeat_finish()
comm.write("heart_rate", "done")


threadLock.acquire()
every_n_frame['n']=-1 
threadLock.release()
while not input_q.empty(): 
	x=input_q.get()	 
for i in range(total_num_threads): 
	input_q.put({'cnt':-1})
for t in threads:
	t.join()
