

import time

import numpy as np

class AdapPID:
	def __init__(self,goal,init_gamma,min_heart_rate,max_heart_rate):
		self.goal=goal
		self.output = 0
		self.gamma = 10
		self.init_gamma = init_gamma
		self.last_time = 0
		self.psn1=0
		self.isn1=0
		self.isn1sn1=0
		self.ds1=0
		self.dsn1=0
		self.start=0
		self.min_heart_rate=min_heart_rate
		self.max_heart_rate=max_heart_rate

	def reset(self):
		self.output = 0
		self.gamma = self.init_gamma
		self.last_time = 0
		self.psn1=0
		self.isn1=0
		self.isn1sn1=0
		self.ds1=0
		self.dsn1=0
		self.start=0		

	def update(self,feedback):

		self.err = self.goal-feedback
		self.gamma = np.log(abs(self.err)+1)/np.log(self.goal)
		current_time = time.time()
		if self.start==0:
			self.delta_time=0
			self.start=1
		else:
			self.delta_time = current_time - self.last_time
		self.output = self.p() + self.i() 
		self.last_time = current_time

		return self.output

	def p(self):
		y1=self.err*1
		p = self.gamma * self.err * y1
		self.psn1+=p*self.delta_time
		# print(self.psn1*y1)
		return self.psn1*y1
	def i(self):
		self.isn1+=self.err*self.delta_time
		y2 = self.isn1
		i = self.gamma * self.err * y2
		self.isn1sn1+=i*self.delta_time
		# print(self.isn1sn1*y2)
		return self.isn1sn1*y2


