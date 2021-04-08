#!/usr/bin/env python
from importlib import import_module
import os
from detect import inference_image
import cv2 as cv
# from enhance import toy_inference_numpy
import numpy as np
import _thread
# import camera driver
# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from camera import Camera


# camera.set_video_source('http://192.168.137.2:8081/')

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

if __name__ == '__main__':
    camera = import_module('camera.camera_opencv').Camera
    camera.set_video_source('http://192.168.137.2:8081/')

    camera = camera()
    frame = camera.get_frame()
    while True:
        try:
            frame = camera.get_frame()
            frame, result = inference_image(frame)
            cv.imshow('', frame)
            key = cv.waitKey(1)
            if key == 27:
                cv.destroyAllWindows()
                break
        except:
            cv.destroyAllWindows()
            break

