#!/bin/sh
num_cpus=$(lscpu | grep -m1 "CPU(s):" | grep -Eo '[0-9]')
for (( c=1; c<=$num_cpus; c++))
do
	yes > /dev/null &
done
