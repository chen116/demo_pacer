#!/usr/bin/env bash

# # 
# # Install main dependencies on CentOS: 
# # Python 3.4.5, CMake 3.10.0, OpenCV 3.3.1
# # Author Andrii Lundiak (landike@gmail.com)
# # 

# https://github.com/ageitgey/face_recognition/issues/191
# https://github.com/opencv/opencv/issues/8471
# https://github.com/Lizmango/CV/issues/5


# Before using CentoOS, this is list of software needed also, 
# but it's not mandatory for the Face Recognition itself.
sudo yum install -y git 
sudo yum install -y gitk
sudo yum install -y cheese


#
# Cmake (https://cmake.org/install/)
# 

sudo yum install -y cmake # installs 2.8.12, which causes error "cmake configuration failed!"
# That is why we need new version (but need to test on new CentOS)

#cd ~/Downloads
# wget https://cmake.org/files/v3.10/cmake-3.10.0.tar.gz
# tar -xf cmake-3.10.0.tar.gz
# cd cmake-3.10.0
# ./configure
# gmake
# sudo gmake install
# and only after this cmake should be added to PATH, 
# or at least "cmake --version" should show new version


#
# Then download, curl, wget, untar, bootstrap, make, install, install other Face Recognition related software
#

# !!!
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_fedora/py_setup_in_fedora.html
# !!!
# https://www.centos.org/forums/viewtopic.php?t=55814

#
# Python 3.4.5
#
# http://ask.xmodulo.com/install-python3-centos.html
# The latest EPEL 7 repository offers python3 (python 3.4 to be exact). 
sudo yum install -y epel-release 

# Now we can install Python 3.4.5
sudo yum install -y python34
sudo yum install -y python34-devel # required by opencv
sudo yum install -y python34-pip  # includes python34-setuptools

# Default repository doens't have python36-devel and python36-numpy, that is why get back to 3.4
# https://rpms.remirepo.net/rpmphp/zoom.php?rpm=numpy
# fast multidimensional array facility for Python 
sudo yum install -y numpy # 1.17 (preinstalled on CentOS?)
sudo yum install -y python34-numpy # requireed by opencv
# anyway, this is important tool

#yum install gcc # already installed on CentOS
sudo yum install -y gcc-c++

# not sure about pkg-config or pkgconfig

#
# Compulsory Dependencies
#
sudo yum install -y gtk2-devel
sudo yum install -y libdc1394-devel
sudo yum install -y libv4l-devel

# yum install ffmpeg-devel  # NOT isnatlled via general yum repositories
sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
sudo yum install -y ffmpeg #2.6.8
sudo yum install -y ffmpeg-devel

sudo yum install -y gstreamer-plugins-base-devel

#
# Optional Dependencies
#
sudo yum install -y libpng-devel
sudo yum install -y libjpeg-turbo-devel
sudo yum install -y jasper-devel
sudo yum install -y openexr-devel
sudo yum install -y libtiff-devel
sudo yum install -y libwebp-devel

# Optional (skipped)
# sudo yum install -y tbb-devel
# with CMake, don’t forget to pass -D WITH_EIGEN=ON.
# sudo yum install -y eigen3-devel
# with CMake, don’t forget to pass -D BUILD_DOCS=ON.
# sudo yum install -y python-sphinx
# sudo yum install -y texlive

# 
# Boost.Python (http://www.boost.org/)
#

# http://www.boost.org/users/download/
# - https://stackoverflow.com/questions/46934760/importerror-libboost-python-so-1-65-1-cannot-open-shared-object-file-no-such
# - https://www.rpmfind.net/linux/rpm2html/search.php?query=libboost_python.so.5
# - http://rpmfind.net/linux/rpm2html/search.php?query=libboost_python.so
# - http://rpmfind.net/linux/rpm2html/search.php?query=libboost_python3.so.1.65.1
# - https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf

# https://github.com/BVLC/caffe/issues/489
# https://github.com/BVLC/caffe/issues/410

# export PYTHON_INCLUDE=/usr/include/python3.4m/
#export PYTHON_INCLUDE=/usr/local/include/python3.6m/

# export PYTHONAPTH=/usr/include/python3.4m/
#export PYTHONAPTH=/usr/local/include/python3.6m/

cd ~/
wget https://dl.bintray.com/boostorg/release/1.65.1/source/boost_1_65_1.tar.gz
tar -xf boost_1_65_1.tar.gz
rm boost_1_65_1.tar.gz
cd boost_1_65_1
./bootstrap.sh --with-libraries=python --with-python=/usr/local/bin/python3 
# IMPORTANT for later proper dlib execution (not visible includes (*.h files))
# export CPLUS_INCLUDE_PATH=/usr/include/python3.4.m # ???
export CPLUS_INCLUDE_PATH=/usr/local/include/python3.6m
export PATH=~/boost_1_65_1:~/boost_1_65_1/stage/lib:$PATH
# IMPORTANT
./b2
sudo ./b2 install


#
# OpenCV 3.3.1
# 

# Do NOT INSTALL from yum, because it's old - 2.4.5 and doesn't work with Python3.x
# And before yo continue, need to delete installed opencv 2.4.5
sudo yum remove opencv # it will also delete opencv-python
# Then download from git repo, checkout to tag 3.3.1 and install from sources
# Let's install all software in user folder.

cd ~/

# AFTER research, looks like we could install openCV 3.3.0 and it might work together with opencv_python==3.3.0.10
# TODO
git clone https://github.com/Itseez/opencv_contrib.git
cd opencv_contrib
git checkout 3.3.1
# ~/opencv_contrib/mdoules Will be used later 

cd ../ # get back to ~/

#
# OpenCV 3.x Core setu
#
git clone https://github.com/Itseez/opencv.git
cd opencv
git checkout 3.3.1

mkdir build
cd build


# https://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D INSTALL_C_EXAMPLES=OFF \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D BUILD_EXAMPLES=OFF ..

# Similar output on CentOS-office and CentOS-VirtualBox
# Video I/O:
# --     DC1394 1.x:                  NO
# --     DC1394 2.x:                  NO
# --     FFMPEG:                      YES
# --       avcodec:                   YES (ver 56.26.100)
# --       avformat:                  YES (ver 56.25.101)
# --       avutil:                    YES (ver 54.20.100)
# --       swscale:                   YES (ver 3.1.101)
# --       avresample:                YES (ver 2.1.0)
# => (looks like FFMPEG is, and might be enough), so let's continue.

# THIS IS GOOD SIGN - Officce
# -- Found PythonInterp: /usr/bin/python2.7 (found suitable version "2.7.5", minimum required is "2.7") 
# -- Found PythonLibs: /lib64/libpython2.7.so (found suitable exact version "2.7.5") 
# -- Found PythonInterp: /usr/bin/python3.4 (found suitable version "3.4.5", minimum required is "3.4") 
# -- Found PythonLibs: /lib64/libpython3.4m.so (found suitable exact version "3.4.5") 

# THIS IS GOOD SIGN - VirtualBox
# -- Found PythonInterp: /usr/bin/python2.7 (found suitable version "2.7.5", minimum required is "2.7") 
# -- Could NOT find PythonLibs (missing: PYTHON_LIBRARIES PYTHON_INCLUDE_DIRS) (Required is exact version "2.7.5")
# -- Found PythonInterp: /usr/bin/python3.4 (found suitable version "3.4.5", minimum required is "3.4") 
# -- Found PythonLibs: /lib64/libpython3.4m.so (found suitable exact version "3.4.5") 

# A few NOT FOUND records, but LOOKS like ok... TODO

# -- Looking for ccache - not found
# -- Looking for io.h - not found
# -- Looking for jbg_newlen - not found
# -- Looking for /usr/include/libpng/png.h - not found
# -- Looking for linux/videodev.h - not found
# -- Looking for linux/videodev2.h - found
# -- Looking for sys/videoio.h - not found
# -- A library with BLAS API not found. Please specify library location.
# -- A library with LAPACK API not found. Please specify library location.
# -- VTK is not found. Please set -DVTK_DIR in CMake to VTK build directory, or to VTK install subdirectory with VTKConfig.cmake file
# -- The protocol buffer compiler is not found (PROTOBUF_PROTOC_EXECUTABLE='')
# -- Module opencv_sfm disabled because the following dependencies are not found: Eigen Glog/Gflags
# --   Matlab:                        Matlab not found or implicitly disabled


#
# Alternatives
#

# cmake -D WITH_OPENCL=OFF 
# -D WITH_CUDA=OFF \
# -D BUILD_opencv_gpu=OFF \
# -D BUILD_opencv_gpuarithm=OFF \
# -D BUILD_opencv_gpubgsegm=OFF \
# -D BUILD_opencv_gpucodec=OFF \
# -D BUILD_opencv_gpufeatures2d=OFF \
# -D BUILD_opencv_gpufilters=OFF \
# -D BUILD_opencv_gpuimgproc=OFF \
# -D BUILD_opencv_gpulegacy=OFF \ 
# -D BUILD_opencv_gpuoptflow=OFF \
# -D BUILD_opencv_gpustereo=OFF \
# -D BUILD_opencv_gpuwarping=OFF ..

# cmake -D CMAKE_BUILD_TYPE=RELEASE \
# -D CMAKE_INSTALL_PREFIX=/usr/local \
# -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3 \
# -D PYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3 \ 
# PYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3 ..

# Using Python 3.4
# cmake -D CMAKE_BUILD_TYPE=RELEASE 
# -D CMAKE_INSTALL_PREFIX=/usr/local \
# -DPYTHON_INCLUDE_DIR=/usr/include/python3.4m/ \
# -DPYTHON_LIBRARY=/usr/lib/libpython3.4.dylib \ 
# -DPYTHON_EXECUTABLE=/usr/bin/python3.4 \
# -DPYTHON_PACKAGES_PATH=/usr/local/lib/python3.4/site-packages/ ..

#
# Alternatives
#

#
# OK, back to OpenCV core and make/install it
#

make -j4
sudo make install

# In office, after OpenCV instalation, restart CentOS needed, 
# because there was memory errors. But even so, did not help with "boost issue".
# On VirtualBox no restart but it did not solved issue with cmake error.
# Additionall for OpenCV (uncludes also numpy and python_nose)


# >>> import sys;
# >>> print(sys.path)
# ['', '/usr/lib64/python34.zip', 
# '/usr/lib64/python3.4', # many py files
# '/usr/lib64/python3.4/plat-linux', # regen
# '/usr/lib64/python3.4/lib-dynload',  # AMNY *.so files
# '/usr/lib64/python3.4/site-packages',  # numpy only
# '/usr/lib/python3.4/site-packages'] # pip, pkg, setup_tools

# import cv 2 doesn't work yet

#
# So we need MAGIC with OpenCV so file and/or $PATH
#

sudo cp ~/opencv/build/lib/python3/cv2.cpython-34m.so /usr/lib/python3.4/site-packages/ # I DID THIS !!!!
# or
# cp /usr/local/lib/python3.4/site-packages/cv2.cpython-34m.so /usr/lib/python3.4/site-packages/cv2/
# maybe need to copy to cv2 folder?

#
# How to check if OpenCV 3.x installed properly for Python 3.x
#
# python3
# >>> import cv2
# >>> print(cv.__version__) # should be 3.3.1, but first it showed me 3.3.0


# Looks like /usr/lib64/python3.4/site-packages/cv2/cv2.cpython-34m.so is 3.3.0 and not I installed 3.3.1


# Logs about so files locations and sizes

# $ ls -la ~/opencv/build/lib/python3/cv2.cpython-34m.so 
# -rwxrwxr-x 1 poc poc 5301880 Dec  7 19:50 /home/poc/opencv/build/lib/python3/cv2.cpython-34m.so

# $ ls -la /usr/lib/python3.4/site-packages/cv2.cpython-34m.so 
# -rwxr-xr-x 1 root root 5301880 Dec  7 20:36 /usr/lib/python3.4/site-packages/cv2.cpython-34m.so

# $ ls -la  /usr/local/lib/python3.4/site-packages/cv2.cpython-34m.so 
# -rwxr-xr-x 1 root root 5301880 Dec  7 19:50 /usr/local/lib/python3.4/site-packages/cv2.cpython-34m.so

# $ ls -la /usr/lib64/python3.4/site-packages/cv2/cv2.cpython-34m.so
# -rwxr-xr-x 1 root root 25676848 Dec  7 20:41 /usr/lib64/python3.4/site-packages/cv2/cv2.cpython-34m.so
# this fiel is from "pip3 install opencv_python==3.3.0.10" and IT IS WRONG for Face Recognitioncode working with OpenCV 3.3.1
# THAT IS WHY WE MUST REPLACE so file.

#
# IMPORTANT !!! this Need to run after "pip3 install -r requirements.txt"
#
sudo cp ~/opencv/build/lib/python3/cv2.cpython-34m.so /usr/lib64/python3.4/site-packages/cv2/

#
# This command need to run alwasy after new "pip3 install -r requirements.txt"
#

#
# THIS IS ALSO BAD
# /usr/lib/python3.4/site-packages/cv2.cpython-34m.so
# 3.3.1
# THIS IS ALSO BAD
# SO WE BETTER use/install opencv_python==3.3.0.10 BUT JUST replace ONE so file, and it all works !!!
#

#
#
# OUTCOME: in fact python module opencv_python (from project requirements.txt) installs as latest version 3.3.0.10 
# and it installs as /usr/lib64/python3.4/site-packages/cv2/cv2.cpython-34m.so
# But when we install OpenCV from sources 3.3.1, then running application versions/code simply mismatch.
# There is no 3.3.1.x version of opencv_python module, that is why we need to replace so file manually, and then it works.
# But I think it's rather not OK to have such manuipulation
#
#