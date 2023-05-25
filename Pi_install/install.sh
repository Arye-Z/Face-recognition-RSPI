#!/bin/bash

cvVersion="master"

# Create directory for installation
mkdir installation
mkdir installation/OpenCV-"$cvVersion"

# Save current working directory
cwd=$(pwd)


sudo apt -y remove x264 libx264-dev

## Install dependencies

sudo apt -y install build-essential checkinstall cmake pkg-config yasm
sudo apt -y install git gfortran
sudo apt -y install libjpeg8-dev libjasper-dev libpng12-dev
sudo apt -y install libtiff5-dev
sudo apt -y install libtiff-dev
sudo apt -y install libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev
sudo apt -y install libxine2-dev libv4l-dev

cd /usr/include/linux
sudo ln -s -f ../libv4l1-videodev.h videodev.h

cd $cwd


sudo apt -y install libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
sudo apt -y install libgtk2.0-dev libtbb-dev qt5-default
sudo apt -y install libatlas-base-dev
sudo apt -y install libmp3lame-dev libtheora-dev
sudo apt -y install libvorbis-dev libxvidcore-dev libx264-dev
sudo apt -y install libopencore-amrnb-dev libopencore-amrwb-dev
sudo apt -y install libavresample-dev
sudo apt -y install x264 v4l-utils


# Optional dependencies

sudo apt-get -y install libprotobuf-dev protobuf-compiler

sudo apt-get -y install libgoogle-glog-dev libgflags-dev

sudo apt-get -y install libgphoto2-dev libeigen3-dev libhdf5-dev doxygen

# Install python stuff

# get python 3.8.6 for running the environment needed
echo "Retrieving python 3.8.6 for project environment and installing..."
wget https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tar.xz
tar xf Python-3.8.6.tar.xz
cd Python-3.8.6
./configure --prefix=/usr/local/opt/python-3.8.6
make -j 4
sudo make install
echo "Python 3.8.6 environment installed successfully."
#now remove the files not needed
echo "Remove uneccessary installation files..."
cd ..
sudo rm -r Python-3.8.6
rm Python-3.8.6.tar.xz
echo "Finished removing files."

#make python3.8 the default python version
echo "Making python 3.8.6 defualt python..."
. ~/.bashrc
sudo update-alternatives --config python
echo "Python 3.8.6 should now be default python."

#install with pip3.8 venv
echo "Upgrading pip to latest version..."
python3.8 -m pip install --user  pip --upgrade
echo "Finished upgrading pip."

#clone git repository of project
echo "Cloning projects repository to ./Embedded_CV/"
git clone https://github.com/YaakovH/Embedded_CV.git Embedded_CV
git config credential.helper store
echo "Finished cloning repository."

#install all python packages needed for project
echo "Installing all project's python packages..."
python3.8 -m pip install --user -r ./Embedded_CV/requirements.txt
echo "Finished installing python packages"

sudo apt -y install python3-testresources


cd $cwd

# Install virtual environment

python3 -m venv OpenCV-"$cvVersion"-py3
echo "# Virtual Environment Wrapper" >> ~/.bashrc
echo "alias workoncv-$cvVersion=\"source $cwd/OpenCV-$cvVersion-py3/bin/activate\"" >> ~/.bashrc
source "$cwd"/OpenCV-"$cvVersion"-py3/bin/activate

#############

# ########### For Python 3 ############
# now install python libraries within this virtual environment
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
pip install numpy dlib
# quit virtual environment
deactivate


# OPEN CV INSTALL

git clone https://github.com/opencv/opencv.git
cd opencv
git checkout $cvVersion
cd ..

git clone https://github.com/opencv/opencv_contrib.git
cd opencv_contrib
git checkout $cvVersion
cd ..

cd opencv
mkdir build
cd build


cmake -D CMAKE_BUILD_TYPE=RELEASE \
            -D CMAKE_INSTALL_PREFIX=/usr/local \
            -D INSTALL_C_EXAMPLES=ON \
            -D INSTALL_PYTHON_EXAMPLES=ON \
            -D WITH_TBB=ON \
            -D WITH_V4L=ON \
            -D OPENCV_PYTHON3_INSTALL_PATH=$cwd/OpenCV-$cvVersion-py3/lib/python3.5/site-packages \
            -D WITH_QT=ON \
            -D WITH_OPENGL=ON \
            -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
            -D BUILD_EXAMPLES=ON ..

make -j$(nproc)
make install

sudo sed -i 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

echo "sudo modprobe bcm2835-v4l2" &amp;amp;amp;amp;gt;&amp;amp;amp;amp;gt; ~/.profile