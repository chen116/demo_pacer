#!/bin/sh
yum install -y wget
yum install -y git
yum install -y epel-release 
yum install -y python34 
yum install -y python34-setuptools 
yum install -y python34-devel 
yum -y install python34-tkinter
easy_install-3.4 pip 
pip3 install matplotlib 
pip3 install numpy 
pip3 install imutils
pip3 install opencv-python-headless
wget http://semanchuk.com/philip/sysv_ipc/sysv_ipc-1.0.0.tar.gz && tar -xzf sysv_ipc-1.0.0.tar.gz && cd sysv_ipc-1.0.0 && python3 setup.py install && cd /root/
git clone https://github.com/selectel/pyxs && cd pyxs && python3 setup.py install && cd /root/ 
cd /root && git clone https://github.com/chen116/demo_pacer.git && cd demo_pacer
