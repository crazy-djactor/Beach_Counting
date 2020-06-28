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

        python main.py [source]
        
The input parameter "source" can be one of the "schedule", video_name or youtube link.

For example:

        python main.py
        python main.py schedule
        python main.py 1.mp4


## Run script for car detection

        python main_car.py [country]
        
The parameter 'country' can be 'schedule' or ISO2 code such as 'ID', 'DE' and so on.
If 'country'='schedule' then the engine will be run infinitely with schedule by config/schedule_car.csv.

        python main_car.py schedule
        
or

        python main_car.py

if 'country' is a specific country code, then capture all images once and process it, and then end.

        python main_car.py IT
        

### Crontab

    sudo crontab -e

run script 07h 00m ~ 15h 00m every hour

    00 07-15   *   *   * python3 ~/count_things/main.py
    00 07-15   *   *   * python3 ~/count_things/main_car.py
