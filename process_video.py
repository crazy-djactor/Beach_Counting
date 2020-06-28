from config.setting import *
from json_send import *
import func
import time
import cv2
import sys


class ProcessVideo:

    def __init__(self, model='yolo_v3'):
        print('Loading {} model ...'.format(model))
        if model == 'yolo_v3':
            from yolo import YOLO
            self.class_model = YOLO()
        else:
            from tf_detector import TfDetector
            self.class_model = TfDetector(model)

    @staticmethod
    def check_valid_detection(img, rect_list, score_list, class_list, threshold=0.6):
        img_h, img_w = img.shape[:2]
        check_rect_list = []
        check_score_list = []

        for i in range(len(score_list)):
            if int(class_list[i]) == 1 and score_list[i] > threshold:
                if rect_list[i][2] - rect_list[i][0] < img_w / 3 and rect_list[i][3] - rect_list[i][1] < img_h / 3:
                    check_rect_list.append(rect_list[i])
                    check_score_list.append(score_list[i])

        return check_rect_list, check_score_list

    @staticmethod
    def draw_img(img, rect_list):
        for rect in rect_list:
            img = cv2.rectangle(img, (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3])), (255, 0, 0), 2)

        return img

    @staticmethod
    def draw_count(img, count):
        cv2.rectangle(img, (0, 0), (170, 40), (255, 255, 255), -1)
        cv2.putText(img, "Count: " + str(count), (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        return img

    def process_video(self, video_source, f_save):
        cap = cv2.VideoCapture(video_source)
        video_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MPEG'), fps, (video_w, video_h))

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            img_draw, valid_rects = self.process_image(frame, DETECT_THRESHOLD)

            if f_save:
                out.write(img_draw)

            cv2.imshow('frame', cv2.resize(img_draw, None, fx=0.5, fy=0.5))

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_video_split(self, video_source, f_send_server=True, f_show=True, f_save=False):
        print('Video Source => ' + video_source)
        cap = cv2.VideoCapture(video_source)

        video_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        start_h = int(video_h * 0.4)
        end_h = int(video_h * 0.6)
        start_w = int(video_w * 0.45)
        end_w = int(video_w * 0.55)
        fps = cap.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MPEG'), fps, (video_w, video_h))

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # --------------------- split frame and detect individually --------------------
            frame1 = frame[:end_h, :end_w].copy()
            frame2 = frame[:end_h, start_w:].copy()
            frame3 = frame[start_h:, :end_w].copy()
            frame4 = frame[start_h:, start_w:].copy()

            _, valid_rects1 = self.process_image(frame1, DETECT_THRESHOLD)
            _, valid_rects2 = self.process_image(frame2, DETECT_THRESHOLD)
            _, valid_rects3 = self.process_image(frame3, DETECT_THRESHOLD)
            _, valid_rects4 = self.process_image(frame4, DETECT_THRESHOLD)

            # -------------------------- combine the detection result ----------------------
            valid_rects = []
            for i in range(len(valid_rects1)):
                rect = valid_rects1[i]
                if rect[2] < end_w - 10 and rect[3] < end_h - 10:
                    valid_rects.append(rect)

            new_rect_list = []
            for i in range(len(valid_rects2)):
                rect = valid_rects2[i]
                if rect[0] > 10 and rect[3] < end_h - 10:
                    new_rect = [rect[0] + start_w, rect[1], rect[2] + start_w, rect[3]]
                    if not func.check_contain(valid_rects, new_rect):
                        new_rect_list.append(new_rect)

            valid_rects += new_rect_list
            new_rect_list = []
            for i in range(len(valid_rects3)):
                rect = valid_rects3[i]
                if rect[2] < end_w - 10 and rect[1] > 10:
                    new_rect = [rect[0], rect[1] + start_h, rect[2], rect[3] + start_h]
                    if not func.check_contain(valid_rects, new_rect):
                        new_rect_list.append(new_rect)

            valid_rects += new_rect_list
            new_rect_list = []
            for i in range(len(valid_rects4)):
                rect = valid_rects4[i]
                if rect[0] > 10 and rect[1] > 10:
                    new_rect = [rect[0] + start_w, rect[1] + start_h, rect[2] + start_w, rect[3] + start_h]
                    if not func.check_contain(valid_rects, new_rect):
                        new_rect_list.append(new_rect)
            valid_rects += new_rect_list

            # ----------------------- Send the result to server --------------------------
            if f_send_server:
                temp_name = str(time.time()) + '.jpg'
                cv2.imwrite(temp_name, frame)
                json_req = make_request_json(ip_addr=video_source, img_file=temp_name, count=len(valid_rects))
                send_request(SERVER_URL, json_req)
                func.rm_file(temp_name)

            # ---------------------------- draw the result -------------------------------
            print('The are {} peoples.'.format(len(valid_rects)))

            img_draw = self.draw_img(frame, valid_rects)
            img_draw = self.draw_count(img_draw, len(valid_rects))

            if f_save:
                out.write(img_draw)

            if f_show:
                cv2.imshow('frame', cv2.resize(img_draw, None, fx=0.5, fy=0.5))

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_image(self, frame, threshold=0.2):
        # ------------------------ detect person ---------------------------
        det_rect_list, det_score_list, det_class_list = self.class_model.detect_from_images(frame)
        valid_rects, valid_scores = self.check_valid_detection(frame,
                                                               det_rect_list,
                                                               det_score_list,
                                                               det_class_list,
                                                               threshold)

        # ------------------------ drawing result --------------------------
        img_draw = self.draw_img(frame, valid_rects)
        img_draw = self.draw_count(img_draw, len(valid_rects))

        return img_draw, valid_rects


if __name__ == '__main__':
    if len(sys.argv) > 1:
        video_src = sys.argv[1]
    else:
        video_src = 'rtsp://{}:{}@{}:554/cam/realmonitor?channel=1&subtype=0'.\
            format(CAMERA_USER_NAME, CAMERA_PASSWORD, CAMERA_IP)

    class_obj = ProcessVideo(MODEL_NAME)
    # video_src = './3.mov'
    # class_obj.process_video(filename, f_save=False)
    class_obj.process_video_split(video_src, f_send_server=F_SEND_SERVER, f_save=F_WRITE_VIDEO, f_show=F_SHOW_RESULT)
