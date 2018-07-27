# with fancy arg, foucsing on just managing 2 vm ( or more if no contention)

# example usage :git pull &&  python3 monitor_dup3.py -d 23,24 -f 10
import sys
sys.path.insert(0, '/root/demo_pacer/')

import host_guest_comm
import xen_interface
import threading
import time
import pprint
import res_alloc
from pyxs import Client

with open("data.txt", "w") as myfile:
	myfile.write("")

import argparse
ap = argparse.ArgumentParser()
# ap.add_argument("-d", "--domUs", help="domUs id,sperate by comma")
ap.add_argument("-t", "--timeslice",type=int, default=10000, help="sched quantum")
ap.add_argument("-f", "--fps", type=float, default=30, help="target fps")
ap.add_argument("-a", "--algo", type=int, default=4, help="algorithm for both")
ap.add_argument("-s", "--static-alloc", type=int, default=10, help="static utilization percentage")
args = vars(ap.parse_args())


monitoring_items = ["heart_rate","sampling_period"]
# monitoring_domU = (args["domUs"]).split(',')
monitoring_domU = ["VM1","VM2"]
dummy_domU = ["d1","d2"]

with Client(xen_bus_path="/dev/xen/xenbus") as c:
	domu_ids=[]
	all_domuid_ids = []
	for uid in c.list('/local/domain'.encode()):
		all_domuid_ids.append(uid.decode())
	all_domuid_ids.pop(0)
	for uid in all_domuid_ids:
		name_path = ("/local/domain/"+uid+"/name").encode()
		if c[name_path].decode() == "VM1":
			monitoring_domU[0] = uid
		if c[name_path].decode() == "VM2":
			monitoring_domU[1] = uid
		if c[name_path].decode() == "d1":
			dummy_domU[0] = uid
		if c[name_path].decode() == "d2":
			dummy_domU[1] = uid



domUs = host_guest_comm.Dom0(monitoring_items,monitoring_domU)

timeslice_us=args["timeslice"]
min_heart_rate = float(args["fps"])
max_heart_rate = float(args["fps"])*1.5


class MonitorThread(threading.Thread):
	def __init__(self, threadLock,shared_data,domuid,rtxen_or_credit,timeslice_us,min_heart_rate,max_heart_rate,keys=['test'],base_path='/local/domain'):
		threading.Thread.__init__(self)
		self.domuid=(domuid)
		self.other_domuid=dummy_domU[0]
		if self.domuid==monitoring_domU[1]:
			self.other_domuid=dummy_domU[1]

		self.algo = args["algo"]
		self.keys=keys
		self.base_path=base_path
		self.threadLock=threadLock
		self.shared_data=shared_data
		self.timeslice_us = timeslice_us
		self.rtxen_or_credit = rtxen_or_credit # 1 is rtds, 0 is credit
		self.allocMod = res_alloc.ResourceAllocation(args["static_alloc"],timeslice_us,min_heart_rate,max_heart_rate,self.algo,self.domuid,self.other_domuid,self.shared_data,rtxen_or_credit)

	def run(self):
		with Client(unix_socket_path="/var/run/xenstored/socket_ro") as c:
			m = c.monitor()
			for key in self.keys:
				tmp_key_path = (self.base_path+'/'+self.domuid+'/'+key).encode()
				token = (key).encode()
				m.watch(tmp_key_path,token)
			msg=""
			while msg!='done':
				path,token=next(m.wait())
				msg=c.read(path).decode()
				self.threadLock.acquire()
				if "sampling_period" in path.decode():
					# self.allocMod.pid.reset()
					if msg.isdigit():
						with open("data.txt", "a") as myfile:
							myfile.write(self.domuid+" "+(msg)+" sampling period"+ " "+str(time.time())+"\n")
				if "heart_rate" in path.decode():
					heart_rate=-1
					try :
						heart_rate = float(msg)
						self.res_allocat(heart_rate)	
					except:
						heart_rate=-1
					# if heart_rate>-1:
					# 	self.res_allocat(heart_rate)					
				self.threadLock.release()
		return

	def res_allocat(self,heart_rate):
		cur_bw = 0
		myinfo = self.shared_data[self.domuid]
		if self.rtxen_or_credit=="rtxen":
			for vcpu in myinfo:
				if vcpu['pcpu']!=-1:
					cur_bw=int(vcpu['b'])
		elif self.rtxen_or_credit=="credit":
			for vcpu in myinfo:
				if vcpu['pcpu']!=-1:
					cur_bw=int(vcpu['w'])
		
		cur_bw = self.allocMod.exec_allocation(heart_rate,cur_bw)
		other_cur_bw = self.timeslice_us - cur_bw
		# (cur_bw,other_cur_bw)=self.allocMod.exec_sharing(cur_bw)

		other_info = self.shared_data[self.other_domuid]
		if self.rtxen_or_credit=="rtxen":
			for vcpu in other_info:
				if vcpu['pcpu']!=-1:
					vcpu['b']=other_cur_bw
			for vcpu in myinfo:
				if vcpu['pcpu']!=-1:
					vcpu['b']=cur_bw
			xen_interface.sched_rtds(self.domuid,self.timeslice_us,cur_bw,[])
			xen_interface.sched_rtds(self.other_domuid,self.timeslice_us,other_cur_bw,[])
		elif self.rtxen_or_credit=="credit":
			for vcpu in other_info:
				if vcpu['pcpu']!=-1:
					vcpu['w']=other_cur_bw
			for vcpu in myinfo:
				if vcpu['pcpu']!=-1:
					vcpu['w']=cur_bw
			xen_interface.sched_credit(self.domuid,cur_bw)
			xen_interface.sched_credit(self.other_domuid,other_cur_bw)



		# buf=10000
		# self.shared_data['cnt'] = (self.shared_data['cnt']+1)%buf
		time_now=str(time.time())
		info = self.domuid+" "+str(heart_rate)+" hr "+time_now+"\n"
		place_holder_for_graph = " x x x x x "
		info += self.domuid + " " +str(cur_bw/self.timeslice_us) + place_holder_for_graph+time_now
		# info += self.other_domuid+ " "+str(other_cur_bw/self.timeslice_us) + place_holder_for_graph+time_now
		with open("data.txt", "a") as myfile:
			myfile.write(info+"\n")
		return

	# https://xenbits.xen.org/docs/unstable/man/xl.1.html#SCHEDULER-SUBCOMMANDS
	# cpupool, vcpupin, rtds-budget,period, extratime, vcpu-list






threadLock = threading.Lock()
threads = []
shared_data = xen_interface.get_global_info()

for domuid in domUs.domu_ids:
	rtxen_or_credit="rtxen"
	if domuid in shared_data['credit']:
		rtxen_or_credit="credit"
	if rtxen_or_credit == "credit":
		xen_interface.sched_credit(domuid,timeslice_us*args["static_alloc"]/100)
	else:	
		xen_interface.sched_rtds(domuid,timeslice_us,timeslice_us*args["static_alloc"]/100,[])

shared_data = xen_interface.get_global_info()
shared_data['pass_val']=[0.1,0.2]
shared_data['stride_val']=[10,10]
shared_data['last_time_val']=0
shared_data['contention_time_passed']=0
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(shared_data)

print('monitoring:')
for i in range(2):
	vmstr = 'VM'+str(i+1)
	if monitoring_domU[i] in shared_data['rtxen']:
		print("	rtxen",vmstr,'with domU ID:',monitoring_domU[i],"dummy domU d1 with ID",dummy_domU[i])
	else:
		print("	credit",vmstr,'with domU ID:',monitoring_domU[i],"dummy domU d2 with ID",dummy_domU[i])


with open("misc.txt", "w") as myfile:
	myfile.write("min "+str(args["fps"])+"\n")
	myfile.write("max "+str(args["fps"])+"\n")
	myfile.write("timeslice_us "+str(timeslice_us/1000)+"\n")







for domuid in domUs.domu_ids:
	rtxen_or_credit="rtxen"
	if domuid in shared_data['credit']:
		rtxen_or_credit="credit"

	tmp_thread = MonitorThread(threadLock,shared_data,domuid,rtxen_or_credit,timeslice_us,min_heart_rate,max_heart_rate, monitoring_items)
	tmp_thread.start()
	threads.append(tmp_thread)




# Wait for all MonitorThreads to complete
threads_cnt=0
for t in threads:
	t.join()
	threads_cnt+=1
#print('FINAL COUNT:',shared_data['cnt'])
pp = pprint.PrettyPrinter(indent=2)
print('Final domUs info:')
shared_data_clean_up = xen_interface.get_global_info()
# default_bw=int(timeslice_us/(len(monitoring_domU)))

# for uid in monitoring_domU:
# 	xen_interface.sched_rtds(int(uid),timeslice_us,default_bw,[])





# for domuid in shared_data['rtxen']:
# 	xen_interface.sched_rtds(domuid,timeslice_us,default_bw,[])
# xen_interface.sched_credit_timeslice(timeslice_us/1000)
# for domuid in shared_data['credit']:
# 	xen_interface.sched_credit(domuid,default_bw)
print("Exiting the Monitor, total",threads_cnt,"monitoring threads")

