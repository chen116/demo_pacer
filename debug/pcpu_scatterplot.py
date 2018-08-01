import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", default="data.txt", help="file")
args = vars(ap.parse_args())


s = pd.Series()

pcpu = []
data = open(args["file"],"r").read()
for eachLine in data:
    if len(eachLine)>1:
    	line = eachLine.split()
    	if len(line) == 3 :
        # get line with structure 0v1 5.2343243 1
        	vmid = int(line[0].split('v')[0])
        	vcpu = int(line[0].split('v')[1])
        	time = float(line[1])
        	pcpu = int(line[2])
        
        VMs_id.append(float(line[1]))
