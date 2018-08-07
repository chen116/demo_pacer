#!/bin/sh
# this script is used for d1,d2	to make	all their CPUs busy
num_cpus=$(lscpu | grep -m1 "CPU(s):" | grep -Eo '[0-9]')
for (( c=1; c<=$num_cpus; c++))
do
	yes > /dev/null &
done
# use yes > /dev/null  to make each CPU busy