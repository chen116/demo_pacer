from pyxs import Client
import subprocess
import copy
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2




ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", default="rollcar.3gp", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

if "mp4" in args["video"]:
    hh=360
    ww=480

else:
    hh=144
    ww=176

# car_len = 75
# blank_len = 25
# rollback_len = 50
# car = np.zeros((car_len,hh,ww,3),dtype=np.uint8)
# blank = np.zeros((blank_len,hh,ww,3),dtype=np.uint8)
# rollback = np.zeros((rollback_len,hh,ww,3),dtype=np.uint8)


# vs= FileVideoStream(args["video"]).start()
# time.sleep(1.0)
# for i in range(250):#blank_len+car_len):
#     frame = vs.read()
#     if i<car_len:
#         car[i,:,:,:]=frame
#     elif i < blank_len+car_len:
#         blank[i-car_len,:,:,:]=frame
#     elif i >= 200:
#         rollback[i-200,:,:,:]=frame


# vs.stop()   

# rollforward = np.copy(rollback)
# rollforward = np.flipud(rollforward)
# carbackword = np.copy(car)

# carbackword = np.flipud(carbackword)
# vidarray = np.concatenate((blank,blank,car,blank,rollback,car,blank,rollback,car,blank,rollback,car,blank,rollback,car,blank,rollback),axis=0)
# vidarray = np.concatenate((car,carbackword,blank,blank,car,blank,rollback,rollforward,blank,blank,carbackword,blank,blank,car,blank),axis=0)
# vidarray = np.concatenate((car,carbackword,blank,blank,car,carbackword,blank,blank,car,carbackword,blank,blank,car,carbackword,blank,blank),axis=0)
# vidarray = np.concatenate((car,blank,blank,car,blank,blank,car,blank,blank,car,blank,blank),axis=0)




car_len = 75
blank_len = 25
rollback_len = 50
car = np.zeros((30,hh,ww,3),dtype=np.uint8)
blank = np.zeros((blank_len,hh,ww,3),dtype=np.uint8)
rollback = np.zeros((rollback_len,hh,ww,3),dtype=np.uint8)


vs= FileVideoStream(args["video"]).start()
time.sleep(1.0)
for i in range(250):#blank_len+car_len):
    frame = vs.read()
    if i<car_len and i <50 and i>=20:
        car[i-20,:,:,:]=frame
    elif i < blank_len+car_len and i >=20:
        blank[i-car_len,:,:,:]=frame
    elif i >= 200:
        rollback[i-200,:,:,:]=frame


vs.stop()   

rollforward = np.copy(rollback)
rollforward = np.flipud(rollforward)
carbackword = np.copy(car)
carbackword = np.flipud(carbackword)

vidarray = np.concatenate((car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,
	blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,
	car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword
	),axis=0)

net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")


import heartbeat
import host_guest_comm
window_size_hr=2
hb = heartbeat.Heartbeat(1024,window_size_hr,100,"vic.log",10,100)
monitoring_items = ["heart_rate","app_mode","frame_size","timeslice"]
comm = host_guest_comm.DomU(monitoring_items)
with Client(xen_bus_path="/dev/xen/xenbus") as c:
	domu_id = c.read("domid".encode())
	key_path_hash_frame_number_entry=('/local/domain/'+domu_id.decode()+'/frame_number_entry').encode()
	key_path_hash_box_entry=('/local/domain/'+domu_id.decode()+'/box_entry').encode()
	while c.read(key_path_hash_frame_number_entry).decode() != "init":
		continue
	(startX, startY, endX, endY)=(0,0,0,0) 
	c.write(key_path_hash_box_entry,(str(startX)+" "+str(startY)+" "+str(endX)+" "+str(endY)).encode())
	c.write(key_path_hash_frame_number_entry,('ready').encode())
	frame_number_entry = "init"
	prev_frame = -1
	self_cnt = 0
	every_n_frame = int(window_size_hr/2)
	detect_car = 1
	prev_detect_car = detect_car
	prev_every_n_frame = every_n_frame
	while frame_number_entry != "done":
		frame_number_entry = c.read(key_path_hash_frame_number_entry).decode()
		try:
			frame_num = int(frame_number_entry)
		except:
			frame_num = -1
		if frame_num > -1 and frame_num>prev_frame:
			frame = vidarray[frame_num]
			frame = imutils.resize(frame, width=300)
			(startX, startY, endX, endY)=(0,0,0,0) 
			if self_cnt%every_n_frame==0:
				(startX, startY, endX, endY)=(0,0,0,0) 
				(h, w) = frame.shape[:2]
				blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), 127.5)			
				net.setInput(blob)
				detections = net.forward()
				for i in np.arange(0, detections.shape[2]):
					confidence = detections[0, 0, i, 2]
					if confidence > 0.5:
						box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
						(startX, startY, endX, endY) = box.astype("int")



				# if sum((startX, startY, endX, endY)) > 0 :
				# 	detect_car = 1
				# else:
				# 	detect_car = 0
				# if prev_detect_car!=detect_car and self_cnt%window_size_hr==0:
				# 	if detect_car:
				# 		every_n_frame = int(window_size_hr/2)
				# 	else:
				# 		every_n_frame = window_size_hr
				# 	prev_detect_car=detect_car
				# 	print("detect car:" ,detect_car)
				# 	comm.write("frame_size",every_n_frame)


				if sum((startX, startY, endX, endY)) > 0 :
					every_n_frame = int(window_size_hr/2)
				else:
					every_n_frame = int(window_size_hr/2)
					
				c.write(key_path_hash_box_entry,(str(startX)+" "+str(startY)+" "+str(endX)+" "+str(endY)).encode())
			prev_frame = frame_num

			hb.heartbeat_beat()
			# print("get_window_heartrate:",hb.get_window_heartrate())
			if self_cnt%every_n_frame==0 and self_cnt>window_size_hr:
				comm.write("heart_rate", hb.get_window_heartrate())
			if prev_every_n_frame!=every_n_frame and self_cnt%every_n_frame==0 :
				prev_every_n_frame=every_n_frame
				comm.write("frame_size",every_n_frame)
			self_cnt+=1




hb.heartbeat_finish()
comm.write("heart_rate", "done")







# with Client(xen_bus_path="/dev/xen/xenbus") as c:
# 	domu_ids=[]
# 	keys=['vid']
# 	if domu_ids==[]:
# 		for x in c.list('/local/domain'.encode()):
# 			domu_ids.append(x.decode())
# 		domu_ids.pop(0)
# 	not_ready_domUs = copy.deepcopy(domu_ids)
# 	for domuid in domu_ids:
# 		permissions = []
# 		permissions.append(('b'+'0').encode())
# 		permissions.append(('b'+domuid).encode())
# 		for key in keys:
# 			tmp_key_path = ('/local/domain'+'/'+domuid+'/'+key).encode()
# 			tmp_val = ('init').encode()
# 			c.write(tmp_key_path,tmp_val)
# 			c.set_perms(tmp_key_path,permissions)
# 			print('created',key,'for dom',domuid)

# 	print('waiting for domUs getting ready...')
# 	while len(not_ready_domUs)>0:
# 		ready_domUs = []
# 		for domuid in not_ready_domUs:
# 			key_path_hash=('/local/domain/'+domu_id+'/vid').encode()
# 			if c.read(key_path_hash).decode() == "ready":
# 				ready_domUs.append(domu_id)
# 		for domuid in ready_domUs:
# 			not_ready_domUs.remove(domuid)
# 			print("dom",domu_id,"ready")

# 	print("applcation start...")
# 	print(vidarray)





