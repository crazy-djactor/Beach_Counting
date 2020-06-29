## Pacakges

        pip install pafy
        pip install --upgrade youtube_dl
        pip install opencv-contrib-python==4.2.0.*
        pip install lxml
        pip install bs4
        pip install tensorflow==1.13.1
        apt update && apt install -y libsm6 libxext6 libxrender-dev


After install packages, should copy models and config folder manually because these folders are not included in the repository.


## Run script for person detection

        python process_video.py [source]
        

## Donwload models
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1pIwotoRlgUH09eyQvKXnhquMSx8RDWQS' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1pIwotoRlgUH09eyQvKXnhquMSx8RDWQS" -O frozen_inference_graph_faster_50.pb && rm -rf /tmp/cookies.txt
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AwqhHwOcxg7jq2iU_FeAMT-F4Z-qq3Va' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AwqhHwOcxg7jq2iU_FeAMT-F4Z-qq3Va" -O frozen_inference_graph_faster_101.pb && rm -rf /tmp/cookies.txt