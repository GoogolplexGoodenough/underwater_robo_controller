#!/usr/bin/env python
from importlib import import_module
import os
from detect import inference_image
from server import comunicator
from controller import SmallRoboController
from planner import TradPlanner

if __name__ == '__main__':
    client = comunicator(sleep_time=0.01)
    commandor = SmallRoboController(client=client, debug_mode=True, test_mode=False)
    camera = import_module('camera.camera_opencv').Camera
    camera.set_video_source('http://192.168.137.2:8081/')
    camera = camera()
    planner = TradPlanner(config_file=None, camera=camera, comunicator=commandor, inference_image=inference_image)
    planner.run()