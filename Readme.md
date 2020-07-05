## Pacakges

    
- Tensorflow install on jetson nano
``` sudo apt-get update
    sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
    
    sudo apt-get install python3-pip
    sudo pip3 install -U pip testresources setuptools
    
    sudo pip3 install -U numpy==1.16.1 future==0.17.1 mock==3.0.5 h5py==2.9.0 keras_preprocessing==1.0.5 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11
    
    sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 'tensorflow<2'
```

- Install OnVif
```
    sudo pip3 install --upgrade onvif_zeep
``` 
- Download models
```
    bash ./init.sh
```    
- Download project
```
git clone https://github.com/crazy-djactor/Beach_Counting.git
```


- Configure project
update the camera ID and credentials(username/password) in the setting.py



After install packages, should copy models and config folder manually because these folders are not included in the repository.


## Run script for person detection

        python process_video.py [source]
        

## Donwload models
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1pIwotoRlgUH09eyQvKXnhquMSx8RDWQS' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1pIwotoRlgUH09eyQvKXnhquMSx8RDWQS" -O frozen_inference_graph_faster_50.pb && rm -rf /tmp/cookies.txt
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AwqhHwOcxg7jq2iU_FeAMT-F4Z-qq3Va' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AwqhHwOcxg7jq2iU_FeAMT-F4Z-qq3Va" -O frozen_inference_graph_faster_101.pb && rm -rf /tmp/cookies.txt