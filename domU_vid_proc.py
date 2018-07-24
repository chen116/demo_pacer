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


vidarray = [1,2,3]


with Client(xen_bus_path="/dev/xen/xenbus") as c:
	domu_id = c.read("domid".encode())
	key_path_hash=('/local/domain/'+domu_id.decode()+'/vid_entry').encode()
	while c.read(key_path_hash).decode() != "init":
		continue
	for x in xrange(1,10):
		print(c.read(key_path_hash).decode())
	# c.write(key_path_hash,('ready').encode())



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





