import os
import numpy as np

class BaseController:
    def __init__(self, client = None, test_mode = False, debug_mode = False):
        if client is None:
            from importlib import import_module
            client = import_module('../server.server').client()
        self.client = client

        self.test_mode = test_mode
        self.debug_mode = debug_mode
        pass

    def project(self, value, ori_scale = None, prj_scale = None):
        if ori_scale is None:
            ori_scale = self.ori_scale
            prj_scale = self.prj_scale
        return (value - min(ori_scale))*(max(prj_scale) - min(prj_scale))/(max(ori_scale) - min(ori_scale)) + min(prj_scale)

    def move_forward(self, speed):
        raise NotImplementedError

    def turn_left(self, speed):
        raise NotImplementedError

    def turn_right(self, speed):
        raise NotImplementedError


    def up(self, speed):
        raise NotImplementedError

    def down(self, speed):
        raise NotImplementedError

    def leaf_at_speed(self, speed):
        raise NotImplementedError

