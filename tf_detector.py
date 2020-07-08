import os
import cv2
import numpy as np
import tensorflow as tf


class TfDetector:

    def __init__(self, model_type='faster_rcnn_resnet50'):
        if model_type == 'faster_rcnn_resnet50':
            model_name = 'frozen_inference_graph_faster_50.pb'
        elif model_type == 'faster_rcnn_resnet101':

            model_name = 'frozen_inference_graph_faster_101.pb'
        elif model_type == 'ssd_mobile_v2':
            model_name = 'frozen_inference_graph_faster_50.pb'
        else:
            model_name = 'frozen_inference_graph.pb'

        path_pb = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', model_name)
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(path_pb, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            self.sess = tf.Session(graph=detection_graph)

        self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        self.boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        self.scores = detection_graph.get_tensor_by_name('detection_scores:0')
        self.classes = detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    def detect_objects(self, image_np):
        # Expand dimensions since the models expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)

        # Actual detection.
        return self.sess.run([self.boxes, self.scores, self.classes, self.num_detections],
                             feed_dict={self.image_tensor: image_np_expanded})

    def detect_from_images(self, frame):
        [frm_height, frm_width] = frame.shape[:2]
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        (boxes, scores, classes, _) = self.detect_objects(frame_rgb)
        detect_rect_list = []
        detect_score_list = []
        detect_class_list = []

        for i in range(len(scores[0])):
            x1, y1 = int(boxes[0][i][1] * frm_width), int(boxes[0][i][0] * frm_height)
            x2, y2 = int(boxes[0][i][3] * frm_width), int(boxes[0][i][2] * frm_height)
            detect_rect_list.append([x1, y1, x2, y2])
            detect_score_list.append(scores[0][i])
            detect_class_list.append(classes[0][i])

        return detect_rect_list, detect_score_list, detect_class_list
