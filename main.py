
from process_video import ProcessVideo
from datetime import datetime
import cv2
import sys
import os
import time
import func


thisdir = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.join(thisdir, 'save_image')
SCHEDULE_CSV = os.path.join(thisdir, 'config', 'schedule.csv')
SAVE_CSV = os.path.join(thisdir, 'result.csv')


def process_single_stream(url, country='', threshold=0.6):
    print("Processing: " + url)
    if url.startswith('https://') or url.startswith('http://'):
        img, cnt = class_process.process_link(url)
        video_id = url.split('=')[-1]
    else:
        img, cnt = class_process.process_image(url, threshold=threshold)
        video_id = os.path.basename(url)

    if not os.path.isdir(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)

    timestamp = str(datetime.fromtimestamp(time.time()))

    if img is None:
        func.append_csv(SAVE_CSV, [[timestamp, country, video_id, 'None']])
    else:
        filename = timestamp.replace(':', '_').replace(' ', '_') + '_' + country + '_' + video_id + '.jpg'
        cv2.imwrite(SAVE_FOLDER + '/' + filename, img)
        func.append_csv(SAVE_CSV, [[timestamp, country, video_id, cnt]])


def process(video_list):
    if video_list == 'schedule':
        schedule = func.load_csv(SCHEDULE_CSV)
        schedule_time = []
        schedule_country = []
        schedule_file = []
        schedule_threshold = []

        for i in range(len(schedule)):
            if i == 0:
                schedule_time.append(int(schedule[i][0]))
            else:
                schedule_time.append(schedule_time[-1] + int(schedule[i][0]))
            schedule_country.append(schedule[i][1])
            schedule_file.append(schedule[i][2])
            schedule_threshold.append(schedule[i][3])

        time_start = time.time()
        while True:
            if datetime.now().minute in [58, 59]:
                sys.exit(0)

            ts = (time.time() - time_start) % schedule_time[-1]
            for i in range(len(schedule_time)):
                if ts < schedule_time[i]:
                    process_single_stream(schedule_file[i], schedule_country[i], schedule_threshold[i])
                    break

            time.sleep(30)

    else:
        process_single_stream(video_list)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        video = sys.argv[1]
    else:
        # video = '../1.avi'
        video = "https://www.youtube.com/watch?v=JqUREqYduHw"
        # video = 'schedule'
    video = "https://www.youtube.com/watch?v=JqUREqYduHw"

    class_process = ProcessVideo()
    process(video)
