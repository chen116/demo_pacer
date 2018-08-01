import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", default="data.txt", help="file")
args = vars(ap.parse_args())


pcpu = []
data = open(args["file"],"r").read()
for eachLine in data:
    if len(eachLine)>1:
        line = eachLine.split()
        VMs_id.append(float(line[1]))
