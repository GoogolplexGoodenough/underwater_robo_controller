#!/usr/bin/env python
from importlib import import_module
import os
from detect import inference_image
import cv2 as cv
import numpy as np
import _thread
from server import comunicator
from controller import SmallRoboController


if __name__ == '__main__':
    client = comunicator(sleep_time=0.01)
    commandor = SmallRoboController(client=client, debug_mode=True)
    camera = import_module('camera.camera_opencv').Camera
    camera.set_video_source('http://192.168.137.2:8081/')
    camera = camera()
    frame = camera.get_frame()
    cam = 0
    while True:
        try:
            frame = camera.get_frame()
            frame, result = inference_image(frame)
            cv.imshow('', frame)
            key = cv.waitKey(1)
            # if key != -1:
                # print(key)
            if key == 27:
                cv.destroyAllWindows()
                break
            if key == 119: # w
                commandor.move_forward(0.5, True)
                pass
            
            if key == 115: # s
                commandor.move_forward(-0.5, True)
                pass
            if key == 97: # a
                commandor.turn_left(0.5, True)
                pass
            if key == 100: # d
                commandor.turn_right(0.5, True)
                pass
            if key == 105: # i
                commandor.up(0.5, True)
                pass
            if key == 107: # k
                commandor.down(0.5, True)
                pass
            if key == 56: # 8
                cam = np.clip(cam + 0.05, -1, 1)
                commandor.set_cam(cam)
            if key == 50: # 2
                cam = np.clip(cam - 0.05, -1, 1)
                commandor.set_cam(cam)
            
        except:
            cv.destroyAllWindows()
            break

