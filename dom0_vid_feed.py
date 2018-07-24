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
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

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





with Client(xen_bus_path="/dev/xen/xenbus") as c:
	domu_ids=[]
	keys=['vid_entry','box_entry']
	if domu_ids==[]:
		for x in c.list('/local/domain'.encode()):
			domu_ids.append(x.decode())
		domu_ids.pop(0)
	not_ready_domUs = copy.deepcopy(domu_ids)
	for domuid in domu_ids:
		permissions = []
		permissions.append(('b'+'0').encode())
		permissions.append(('b'+domuid).encode())
		for key in keys:
			tmp_key_path = ('/local/domain'+'/'+domuid+'/'+key).encode()
			tmp_val = ('init').encode()
			c.write(tmp_key_path,tmp_val)
			c.set_perms(tmp_key_path,permissions)
			print('created',key,'for dom',domuid)

	print('waiting for domUs getting ready...')
	while len(not_ready_domUs)>0:
		ready_domUs = []
		for domuid in not_ready_domUs:
			key_path_hash=('/local/domain/'+domuid+'/vid_entry').encode()
			if c.read(key_path_hash).decode() == "ready":
				ready_domUs.append(domuid)
		for domuid in ready_domUs:
			not_ready_domUs.remove(domuid)
			print("dom",domuid,"ready")

	print("applcation start...")
	for domuid in domu_ids:
		key_path_hash=('/local/domain/'+domuid+'/vid_entry').encode()
		c.write(key_path_hash,domuid.encode())

	frame_cnt=0
	for frame in vidarray:
		cv2.imshow("Frame", frame)
cv2.destroyAllWindows()





