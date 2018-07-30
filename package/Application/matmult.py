import heartbeat
import domU_comm
import numpy as np
import time

# create heartbeat
import heartbeat
window_size_hr=5
sharedmem_id_for_heartbeat = 1024
buffer_depth = 100
log_name = "heartbeat.log"
min_heart_rate = 10 # not used in this demo
max_heart_rate = 100 # not used in this demo
hb = heartbeat.Heartbeat(sharedmem_id_for_heartbeat,window_size_hr,buffer_depth,log_name,min_heart_rate,max_heart_rate)

# establish communication with Dom0
import domU_comm
monitoring_items = ["heart_rate","frame_size"]
comm = domU_comm.DomU(monitoring_items)


matsize = 500
comm.write("frame_size", matsize)
for i in range(50):
	a= np.random.rand(matsize, matsize)
	b= np.random.rand(matsize, matsize)	
	c= np.matmul(b,a.T)
	time.sleep(0.1)
	hb.heartbeat_beat()
	print("get_instant_heartrate:",hb.get_instant_heartrate())
	comm.write("heart_rate", hb.get_window_heartrate())
for i in range(50):
	a= np.random.rand(matsize, matsize)
	b= np.random.rand(matsize, matsize)	
	c= np.matmul(b,a.T)
	time.sleep(0.2)
	hb.heartbeat_beat()
	print("get_instant_heartrate:",hb.get_instant_heartrate())
	comm.write("heart_rate", hb.get_window_heartrate())


comm.write("heart_rate", "done")
hb.heartbeat_finish()