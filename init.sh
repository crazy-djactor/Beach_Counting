python3 -m venv venv
./venv/bin/source activate
pip install pafy
pip install --upgrade youtube_dl
pip install opencv-contrib-python==4.2.0.*
pip install lxml
pip install bs4
pip install tensorflow==1.13.1
pip install requirements.txt
sudo apt update && apt install -y libsm6 libxext6 libxrender-dev
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1pIwotoRlgUH09eyQvKXnhquMSx8RDWQS' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1pIwotoRlgUH09eyQvKXnhquMSx8RDWQS" -O ./models/frozen_inference_graph_faster_50.pb && rm -rf /tmp/cookies.txt
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AwqhHwOcxg7jq2iU_FeAMT-F4Z-qq3Va' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1AwqhHwOcxg7jq2iU_FeAMT-F4Z-qq3Va" -O ./models/frozen_inference_graph_faster_101.pb && rm -rf /tmp/cookies.txt
