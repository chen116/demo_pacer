import heartbeat
import host_guest_comm
import numpy as np
import time

window_size_hr=5
hb = heartbeat.Heartbeat(1024,window_size_hr,100,"vic.log",10,100)
monitoring_items = ["heart_rate"]
comm = host_guest_comm.DomU(monitoring_items)



matsize = 500
comm.write("app_mode", 4)
comm.write("frame_size", matsize)
for i in range(50):
	a= np.random.rand(matsize, matsize)
	b= np.random.rand(matsize, matsize)	
	c= np.matmul(b,a.T)
	time.sleep(0.1)
	hb.heartbeat_beat()
	print("get_instant_heartrate:",hb.get_instant_heartrate())
	comm.write("heart_rate", hb.get_window_heartrate())


comm.write("heart_rate", "done")
hb.heartbeat_finish()