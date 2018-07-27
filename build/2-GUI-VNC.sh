#!/bin/sh
wget https://turbovnc.org/pmwiki/uploads/Downloads/TurboVNC.repo -P /etc/yum.repos.d
yum install turbovnc -y && yum install java-devel -y
yum install epel-release -y
yum groupinstall "X Window System" -y
yum groupinstall "Xfce" -y
