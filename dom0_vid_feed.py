from pyxs import Client
import subprocess
import copy
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2



vs= FileVideoStream("rollcar.3gp").start()
time.sleep(1.0)
car = np.zeros((30,144,176,3),dtype=np.uint8)
blank = np.zeros((60,144,176,3),dtype=np.uint8)

for i in range(130):#blank_len+car_len):
    frame = vs.read()
    if i >= 20 and i < 50:
    	car[i-20,:,:,:]=frame
    elif i >= 70:
        blank[i-70,:,:,:]=frame
vs.stop()   

carbackword = np.copy(car)
carbackword = np.flipud(carbackword)
car = np.concatenate((car, np.flipud(car)), axis=0)

# vidarray = np.concatenate((car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,
# 	blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank
# 	,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword
# 	),axis=0)



vidarray_binary = [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1]

vidarray = np.zeros((1,144,176,3),dtype=np.uint8)
for binary in vidarray_binary:
	if binary:
		vidarray = np.concatenate((vidarray,car),axis=0)
	else:
		vidarray = np.concatenate((vidarray,blank),axis=0)
vidarray = np.delete(vidarray, 0, 0)
print(','.join(str(binary) for binary in vidarray_binary))

# vidarray = np.concatenate((car,car,car,car,car,car,car,car,car,
# 	blank,blank,blank,blank,blank,blank,blank
# 	,car,car,car,car,car,car
# 	),axis=0)

# hh=144
# ww=176

# car_len = 75
# blank_len = 25
# rollback_len = 50

# car = np.zeros((30,144,176,3),dtype=np.uint8)
# blank = np.zeros((30,144,176,3),dtype=np.uint8)
# rollback = np.zeros((rollback_len,144,176,3),dtype=np.uint8)

# vs= FileVideoStream("rollcar.3gp").start()
# time.sleep(1.0)
# # for i in range(250):#blank_len+car_len):
# #     frame = vs.read()
# #     if i<car_len and i <50 and i>=20:
# #         car[i-20,:,:,:]=frame
# #     elif i < blank_len+car_len and i >=20:
# #         blank[i-car_len,:,:,:]=frame
# #     elif i >= 200:
# #         rollback[i-200,:,:,:]=frame

# for i in range(100):#blank_len+car_len):
#     frame = vs.read()
#     if i >= 20 and i < 50:
#     	car[i-20,:,:,:]=frame
#     elif i >= 70 and i < 100:
#         blank[i-car_len,:,:,:]=frame



# # vs= FileVideoStream("rollcar.3gp").start()
# # time.sleep(1.0)
# # for i in range(250):#blank_len+car_len):
# #     frame = vs.read()
# #     if i<car_len and i <50 and i>=20:
# #         car[i-20,:,:,:]=frame
# #     elif i < blank_len+car_len and i >=20:
# #         blank[i-car_len,:,:,:]=frame
# #     elif i >= 200:
# #         rollback[i-200,:,:,:]=frame


# vs.stop()   

# rollforward = np.copy(rollback)
# rollforward = np.flipud(rollforward)
# carbackword = np.copy(car)
# carbackword = np.flipud(carbackword)
# vidarray = np.concatenate((car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,
# 	blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank
# 	,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword
# 	#car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword,car,carbackword
# 	),axis=0)





misc = open("./modulized/misc.txt","r").read()
fps_val = float(misc.split('\n')[0].split()[1])*2



with Client(xen_bus_path="/dev/xen/xenbus") as c:
	domu_ids=[]
	all_domuid_ids = []
	for x in c.list('/local/domain'.encode()):
		all_domuid_ids.append(x.decode())
	all_domuid_ids.pop(0)
	for x in all_domuid_ids:
		name_path = ("/local/domain/"+x+"/name").encode()
		if c[name_path].decode() == "VM1" or c[name_path].decode() == "VM2":
			domu_ids.append(x)
	print("domU's id:",domu_ids)

	boxes = {}
	keys=['frame_number_entry','box_entry']
	# if domu_ids==[]:
	# 	for x in c.list('/local/domain'.encode()):
	# 		domu_ids.append(x.decode())
	# 		boxes[x.decode()]=tuple()
	# 	domu_ids.pop(0)
	# 	boxes.pop('0')
	COLORS = np.random.uniform(100, 255, size=(len(domu_ids), 3))
	# COLORS= np.array([[100,500,250],[200,50,250]])#np.vstack((np.array([[5,200,250]]),np.array([[100,500,250]])))
	COLORS = [[ 120 , 240 , 120],[ 240 , 120,  240]] # green, pink 
	COLORS = [ [255,144,30],[ 120 , 240 , 120],] # blue # green


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
			key_path_hash=('/local/domain/'+domuid+'/frame_number_entry').encode()
			if c.read(key_path_hash).decode() == "ready":
				ready_domUs.append(domuid)
		for domuid in ready_domUs:
			not_ready_domUs.remove(domuid)
			print("dom",domuid,"ready")

	print("applcation start...")
	time.sleep(1)
	# for domuid in domu_ids:
	# 	key_path_hash=('/local/domain/'+domuid+'/frame_number_entry').encode()
	# 	c.write(key_path_hash,domuid.encode())

	frame_cnt=-1
	for frame in vidarray:
		tn = time.time()
		frame = imutils.resize(frame, width=300)
		frame_cnt+=1
		for domuid in domu_ids:
			key_path_hash=('/local/domain/'+domuid+'/frame_number_entry').encode()
			c.write(key_path_hash,str(frame_cnt).encode()) # write in frame number
		while time.time()- tn < 1/fps_val:
			continue
		idx=-1
		for domuid in domu_ids:
			key_path_hash=('/local/domain/'+domuid+'/box_entry').encode()
			try:
				boxes[domuid]=tuple(map(int, c.read(key_path_hash).decode().split(' ')))#(startX, startY, endX, endY)	
			except:
				boxes[domuid]=(0,0,0,0)
			idx+=1
			(startX, startY, endX, endY) = boxes[domuid]
			if sum((startX, startY, endX, endY))>0:
				label = "domU: {}".format(domuid)
				cv2.rectangle(frame, (startX, startY), (endX, endY),COLORS[idx], 2-idx)  
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(frame, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2-idx)

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF


	for domuid in domu_ids:
		key_path_hash=('/local/domain/'+domuid+'/frame_number_entry').encode()
		c.write(key_path_hash,"done".encode()) # write in frame number	

	cv2.destroyAllWindows()
	print("finish")





