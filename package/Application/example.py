import time
import numpy as np
# create heartbeat
import heartbeat
window_size_hr=5
sharedmem_id_for_heartbeat = 1024
buffer_depth = 100
log_name = "heartbeat.log"
min_heart_rate = 10 # this is from the original heartbeat module, not used in Pacer
max_heart_rate = 100 # this is from the original heartbeat module, not used in Pacer
hb = heartbeat.Heartbeat(sharedmem_id_for_heartbeat,window_size_hr,buffer_depth,log_name,min_heart_rate,max_heart_rate)

# establish communication with Dom0
import domU_comm
monitoring_items = ["heart_rate"]
comm = domU_comm.DomU(monitoring_items)
matsize = 650
a= np.random.rand(matsize, matsize)
b= np.random.rand(matsize, matsize)	
c= np.matmul(b,a.T)
# loop
for i in range(50):

	# processing


	c= np.matmul(b,a.T)

	c= np.matmul(b,a.T)
	hb.heartbeat_beat()
	instant_heartrate = hb.get_instant_heartrate()
	print("get_instant_heartrate:",instant_heartrate)
	# send heart rate to Dom0
	comm.write("heart_rate", instant_heartrate)

# loop
for i in range(50):

	# processing

	c= np.matmul(b,a.T)



	hb.heartbeat_beat()
	instant_heartrate = hb.get_instant_heartrate()
	print("		get_instant_heartrate:",instant_heartrate)
	# send heart rate to Dom0
	comm.write("heart_rate", instant_heartrate)




comm.write("heart_rate", "done")
hb.heartbeat_finish()