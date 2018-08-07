#!/usr/bin/env bash

# Install prereqs, a xen-combatible kernel is installed from the centos-release-xen repo
yum update -y
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install -y git yum-utils centos-release-xen
yum groupinstall -y "Development Tools" 
yum update -y

# Update bootloader and reboot
echo "Updating bootloader"
grub2-mkconfig -o "$(readlink /etc/grub2.conf)"

# Install additional prereqs
echo "Installing prereqs"
yum-builddep xen -y
yum install -y transfig wget tar less texi2html libaio-devel dev86 glibc-devel e2fsprogs-devel gitk mkinitrd iasl xz-devel bzip2-devel
yum install -y pciutils-libs pciutils-devel SDL-devel libX11-devel gtk2-devel bridge-utils PyXML qemu-common qemu-img mercurial texinfo
yum install -y libidn-devel yajl yajl-devel ocaml ocaml-findlib ocaml-findlib-devel python-devel uuid-devel libuuid-devel openssl-devel
yum install -y python-markdown pandoc systemd-devel glibc-devel.i686
yum install -y dev86 ncurses-devel pandoc 
yum update -y

# Get source, configure and build
echo "Getting RT-Xen source"
git clone https://github.com/PennPanda/RT-Xen.git
cd RT-Xen
echo "Configure build"
./configure --disable-werror --enable-mc
./configure --disable-qemuu-traditional  --with-extra-qemuu-configure-args='--disable-werror'
echo "Building RT-Xen"
make world PYTHON_PREFIX_ARG=
echo "Installing RT-Xen"
make install PYTHON_PREFIX_ARG=
# Reload modules
/sbin/ldconfig

# Fix paths for xen modules
cd /usr/lib/
ln -s /usr/local/lib/libxlutil.so.4.6.0 libxlutil.so.4.6
ln -s /usr/local/lib/libxlutil.so.4.6.0 libxlutil.so
ln -s /usr/local/lib/libxenlight.so.4.6.0 libxenlight.so.4.6
ln -s /usr/local/lib/libxenlight.so.4.6.0 libxenlight.so
ln -s /usr/local/lib/libxenctrl.so.4.6.0 libxenctrl.so.4.6
ln -s /usr/local/lib/libxenguest.so.4.6.0 libxenguest.so.4.6
ln -s /usr/local/lib/libxenguest.so.4.6.0 libxenguest.so
ln -s /usr/local/lib/libxenstat.so.0.0 libxenstat.so.0
ln -s /usr/local/lib/libxenstat.so.0.0 libxenstat.so
ln -s /usr/local/lib/libxenstore.so.3.0.3 libxenstore.so.3.0
ln -s /usr/local/lib/libxenstore.so.3.0.3 libxenstore.so
ln -s /usr/local/lib/libxenvchan.so.1.0.0 libxenvchan.so.1.0
ln -s /usr/local/lib/libxenvchan.so.1.0.0 libxenvchan.so
ln -s /usr/local/lib/libblktapctl.so.1.0.0 libblktapctl.so.1.0
ln -s /usr/local/lib/libblktapctl.so.1.0.0 libblktapctl.so
cd -
/sbin/ldconfig

# Setup Xen services
echo "Enabling Xen services"
chkconfig xencommons on
chkconfig xendomains on
chkconfig xen-watchdog on
echo "xenfs" > /etc/modules-load.d/xenfs.conf

# Configure Dom0
echo "Configuring Dom0"
sed -i 's/#autoballoon="auto"/autoballoon=0/g' /etc/xen/xl.conf
echo 'BOOT_XEN_AS_DEFAULT="yes"' >> /etc/sysconfig/xen-kernel
echo 'XEN_KERNEL_ARGS="dom0_mem=24000M,max:24000M dom0_max_vcpus=8 dom0_vcpus_pin sched=rtds"' >> /etc/sysconfig/xen-kernel
echo 'LINUX_XEN_KERNEL_ARGS="splash quiet"' >> /etc/sysconfig/xen-kernel

# Reconfigure bootloader
echo "Configuring grub"
grub-bootxen.sh

# Install libvirt
echo "Installing libvirt"
yum -y install libvirt

echo "Install done, please reboot now!"

