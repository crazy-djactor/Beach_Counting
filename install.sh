#sudo apt-get update
#sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
#
#sudo apt-get install python3-pip
#sudo pip3 install -U pip testresources setuptools
#
#sudo pip3 install -U numpy==1.16.1 future==0.17.1 mock==3.0.5 h5py==2.9.0 keras_preprocessing==1.0.5 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11
#
#sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 'tensorflow<2'
#sudo pip3 install --upgrade onvif_zeep
#bash ./download_model.bash

DIR="/etc/onvif/wsdl"
if [ -d "$DIR" ]; then
  echo "Directory Exist for wsl..."
else
  echo "Making directory for wsl..."
  sudo mkdir /etc/onvif
  sudo mkdir /etc/onvif/wsdl
fi
echo "Copy files to wsdl..."
sudo cp ./wsdl/* /etc/onvif/wsdl
echo "Copy beach.service to /etc/systemd/system/beach.service..."
sudo cp ./beach.service /etc/systemd/system/beach.service
