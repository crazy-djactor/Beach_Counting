
import os
from PIL import Image
import numpy as np
from keras import backend as keras_backend
from keras.models import load_model

from yolo3.model import yolo_eval
from yolo3.utils import letterbox_image


class YOLO(object):
    def __init__(self):
        self.score = 0.5
        self.iou = 0.5
        self.model_image_size = (416, 416)  # fixed size or (None, None)

        model_path = os.path.expanduser('models/yolo.h5')
        self.yolo_model = load_model(model_path, compile=False)
        self.class_names = self._get_class('models/coco_classes.txt')
        self.anchors = self._get_anchors('models/yolo_anchors.txt')

        self.sess = keras_backend.get_session()
        self.is_fixed_size = self.model_image_size != (None, None)
        self.input_image_shape = keras_backend.placeholder(shape=(2,))

        self.boxes, self.scores, self.classes = self.generate()

    @staticmethod
    def _get_class(classes_path):
        classes_path = os.path.expanduser(classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    @staticmethod
    def _get_anchors(anchors_path):
        anchors_path = os.path.expanduser(anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
            anchors = [float(x) for x in anchors.split(',')]
            anchors = np.array(anchors).reshape(-1, 2)
        return anchors

    def generate(self):
        # Generate output tensor targets for filtered bounding boxes.
        boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                                           len(self.class_names), self.input_image_shape,
                                           score_threshold=self.score, iou_threshold=self.iou)
        return boxes, scores, classes

    def detect_from_images(self, frame):
        image = Image.fromarray(frame[..., ::-1])  # bgr to rgb
        if self.is_fixed_size:
            assert self.model_image_size[0] % 32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1] % 32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (image.width - (image.width % 32),
                              image.height - (image.height % 32))
            boxed_image = letterbox_image(image, new_image_size)

        image_data = np.array(boxed_image, dtype='float32')

        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                keras_backend.learning_phase(): 0
            })

        detect_rect_list = []
        detect_score_list = []
        detect_class_list = []
        for i in range(len(out_classes)):
            [y1, x1, y2, x2] = out_boxes[i]
            detect_rect_list.append([x1, y1, x2, y2])
            detect_score_list.append(out_scores[i])
            detect_class_list.append(out_classes[i] + 1)

        return detect_rect_list, detect_score_list, detect_class_list

    def close_session(self):
        self.sess.close()
