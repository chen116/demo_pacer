
import apid
import time
class ResourceAllocation:
	def __init__(self,static_alloc, timeslice_us,min_heart_rate,max_heart_rate,algo,domuid,other_domuid,shared_data,rtxen_or_credit):
		self.static_alloc = static_alloc
		self.timeslice_us = timeslice_us
		self.mid=(min_heart_rate+max_heart_rate)/2
		self.min_heart_rate=min_heart_rate
		self.max_heart_rate=max_heart_rate
		self.pid = apid.AdapPID(self.mid,1,min_heart_rate,max_heart_rate)
		self.algo = algo
		self.target_reached_cnt = 0
		self.minn = int(timeslice_us * 0.01)
		self.shared_data = shared_data
		self.domuid = domuid
		self.other_domuid = other_domuid
		self.rtxen_or_credit = rtxen_or_credit
	def exec_sharing(self,cur_bw):
		other_info = self.shared_data[self.other_domuid]
		if self.rtxen_or_credit=="rtxen":
			for vcpu in other_info:
				if vcpu['pcpu']!=-1:
					other_cur_bw=vcpu['b']		
		elif self.rtxen_or_credit=="credit":
			for vcpu in other_info:
				if vcpu['pcpu']!=-1:
					other_cur_bw=vcpu['w']

		if cur_bw+other_cur_bw>self.timeslice_us:
			domu_index_in_pass_val = 0
			if self.domuid>self.other_domuid:
				domu_index_in_pass_val = 1
			my_pass_val = self.shared_data['pass_val'][domu_index_in_pass_val]
			other_pass_val = self.shared_data['pass_val'][(domu_index_in_pass_val+1)%2]
			last_time = self.shared_data['last_time_val']
			now_time = time.time()
			if last_time==0:
				last_time = now_time
				self.shared_data['last_time_val'] = now_time
			self.shared_data["contention_time_passed"]+=now_time-last_time
			self.shared_data['last_time_val'] = now_time
			if my_pass_val<=other_pass_val:
				other_cur_bw=self.timeslice_us-cur_bw
			else:
				cur_bw=self.timeslice_us-other_cur_bw
				self.pid.reset()
			process_unit_time=2.5
			if self.shared_data["contention_time_passed"]>=process_unit_time:# and int(self.shared_data["contention_time_passed"])%5==0:
				self.shared_data["contention_time_passed"]=0
				if my_pass_val<=other_pass_val:
					self.shared_data['pass_val'][domu_index_in_pass_val]+=self.shared_data['stride_val'][domu_index_in_pass_val]
				else:
					self.shared_data['pass_val'][(domu_index_in_pass_val+1)%2]+=self.shared_data['stride_val'][(domu_index_in_pass_val+1)%2]
				with open("info.txt", "a") as myfile:
					myfile.write(self.domuid+" "+self.domuid+" time slice len 6"+ " "+str(now_time)+"\n")							
		else:
			self.shared_data['last_time_val'] = time.time()
		return (cur_bw,other_cur_bw)

	def exec_allocation(self,heart_rate,cur_bw):

		if self.algo==0:
			# static 
			cur_bw = int(self.timeslice_us*self.static_alloc/100)
		elif self.algo==1:
			# amid
			alpha=1
			beta=.9
			free = self.timeslice_us-cur_bw
			if(heart_rate<self.mid):
				if cur_bw<self.timeslice_us-self.minn:
					free=free*beta
					cur_bw=self.timeslice_us-free
				else:
					cur_bw=self.timeslice_us-self.minn
			if(heart_rate>self.mid):
				if cur_bw>self.minn:
					free+=alpha*self.minn
					cur_bw=self.timeslice_us-free
			cur_bw=int(cur_bw)


		elif self.algo==3:
			# apid algo
			output = self.pid.update(heart_rate)
			# output+=self.timeslice_us/2
			if self.pid.start>0:
				tmp_cur_bw = output+cur_bw #int(output*cur_bw+cur_bw)-int(output*cur_bw+cur_bw)%100
				if tmp_cur_bw>=self.timeslice_us-self.minn: #dummy
					cur_bw=self.timeslice_us-self.minn
				elif tmp_cur_bw<=self.minn:#self.timeslice_us/3:
					cur_bw=self.minn#int(self.timeslice_us/3)
				else:
					cur_bw=tmp_cur_bw
			cur_bw=int(cur_bw)


		elif self.algo==4:
			# aimd_range
			alpha=3.5
			beta=.9
			free = self.timeslice_us-cur_bw
			if(heart_rate<self.min_heart_rate):
				if cur_bw<self.timeslice_us-self.minn:
					free=free*beta
					cur_bw=self.timeslice_us-free
				else:
					cur_bw=self.timeslice_us-self.minn
			if(heart_rate>self.max_heart_rate):
				if cur_bw>self.minn:
					free+=alpha*self.minn
					cur_bw=self.timeslice_us-free
			cur_bw=int(cur_bw)



		elif self.algo==5:
			# limd 
			beta=.9
			free = self.timeslice_us-cur_bw		
			if(heart_rate<self.min_heart_rate):
				if cur_bw<self.timeslice_us-self.minn:
					free=free*beta
					cur_bw=self.timeslice_us-free
			if(heart_rate>self.max_heart_rate):
				if cur_bw>self.minn:
					cur_bw-=self.minn
			if heart_rate > self.max_heart_rate:
				self.target_reached_cnt+=1
				if self.target_reached_cnt==16:
					self.target_reached_cnt-=8
					if cur_bw>self.minn:
						cur_bw-=self.minn
			else:
				self.target_reached_cnt=0
			cur_bw=int(cur_bw)

		if cur_bw <= self.minn :
			cur_bw=self.minn
		if cur_bw >= self.timeslice_us-self.minn:
			cur_bw= self.timeslice_us-self.minn
		return(int(cur_bw))


