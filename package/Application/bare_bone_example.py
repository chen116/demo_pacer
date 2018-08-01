import time
import numpy as np
# create heartbeat

matsize = 650
a= np.random.rand(matsize, matsize)
b= np.random.rand(matsize, matsize)	

# loop

for i in range(50):

	# processing

	tn = time.time()
	c= np.matmul(b,a.T)

	c= np.matmul(b,a.T)
	print(1/(time.time()-tn))
	# hb.heartbeat_beat()
	# instant_heartrate = hb.get_instant_heartrate()
	# print("get_instant_heartrate:",instant_heartrate)
	# send heart rate to Dom0
	#comm.write("heart_rate", instant_heartrate)

# loop
for i in range(50):

	# processing
	tn = time.time()

	c= np.matmul(b,a.T)
	print("        ",1/(time.time()-tn))



	# hb.heartbeat_beat()
	# instant_heartrate = hb.get_instant_heartrate()
	# print("		get_instant_heartrate:",instant_heartrate)
	# send heart rate to Dom0
	#comm.write("heart_rate", instant_heartrate)


