#sudo apt-get update
#sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
#
#sudo apt-get install python3-pip
#sudo pip3 install -U pip testresources setuptools
#
#sudo pip3 install -U numpy==1.16.1 future==0.17.1 mock==3.0.5 h5py==2.9.0 keras_preprocessing==1.0.5 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11
#
#sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 'tensorflow<2'

#bash ./download_model.bash

sudo mkdir /etc/onvif/wsdl
sudo cp ./wsdl/* /etc/onvif/wsdl
sudo cp ./BeachCounting.sh /usr/local/bin/BeachCounting.sh
sudo chmod +x /usr/local/bin/BeachCounting.sh
sudo cp ./beach.service /etc/systemd/system/beach.service
