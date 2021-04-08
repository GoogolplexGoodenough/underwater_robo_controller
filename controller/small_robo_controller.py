import os
import numpy as np

from .base_controller import BaseController

class SmallRoboController(BaseController):
    
    def __init__(self, client = None, prj_scale = None, cam_scale = None, test_mode = False, debug_mode = False, mid_leaf_speed = None):
        super().__init__(client, test_mode, debug_mode)
        self.com_dict = {'left_pwm' : 0, 'right_pwm' : 0 ,'up_left_pwm' : 0 ,'up_right_pwm' : 0 ,'camera' : 0}
        if prj_scale is None:
            self.prj_scale = [81, 115]
        else:
            self.prj_scale = prj_scale
        
        if cam_scale is None:
            self.cam_scale = [120, 180]
        else:
            self.cam_scale = cam_scale

        if mid_leaf_speed is None:
            self.mid_leaf_speed = -0.3
        else:
            self.mid_leaf_speed = mid_leaf_speed

        # print(self.debug_mode)
        # print('hello')



    def update_com(self, left_pwm = None, right_pwm = None, up_left_pwm = None, up_right_pwm = None, camera = None, com_dict = None):
        if com_dict is not None:
            for key in com_dict.keys():
                assert(key in self.com_dict.keys())
                self.com_dict[key] = com_dict[key]
                return

        com_dict = {'left_pwm' : left_pwm, 'right_pwm' : right_pwm, 'up_left_pwm' : up_left_pwm ,'up_right_pwm' : up_right_pwm ,'camera' : camera}
        flag = False
        for key in com_dict.keys():
            if com_dict[key] is not None:
                self.com_dict[key] = com_dict[key]
                flag = True
        
        assert(flag)

    def format_com(self):
        com = self.com_dict
        pwm_list = [com['left_pwm'], com['right_pwm'], com['up_left_pwm'], com['up_right_pwm']]
        pwm_list = [self.project(pwm, [-1, 1], self.prj_scale) for pwm in pwm_list]
        com_list = pwm_list + [self.project(com['camera'], [-1, 1], self.cam_scale)]
        com_list = [str(int(c)).zfill(3) for c in com_list]
        com_str = "{}:{}:{}:{}:{}".format(*com_list)
        return com_str

    def move_forward(self, speed = 0.5, reset_pwm = False):
        speed = np.clip(speed, -1, 1)

        if not reset_pwm:
            self.update_com(left_pwm=speed, right_pwm=-1*speed)
        else:
            self.update_com(left_pwm=speed, right_pwm=-1*speed, up_left_pwm=self.mid_leaf_speed, up_right_pwm=self.mid_leaf_speed)

        com_str = self.format_com()
        if self.debug_mode:
            print('move_forward', speed, com_str)
        if not self.test_mode:
            self.client.send_msg(com_str)


    def turn_left(self, speed = 0.5, reset_pwm = False):
        speed = np.clip(speed, -1, 1)

        if not reset_pwm:
            self.update_com(left_pwm=-1*speed, right_pwm=-1*speed)
        else:
            self.update_com(left_pwm=-1*speed, right_pwm=-1*speed, up_left_pwm=self.mid_leaf_speed, up_right_pwm=self.mid_leaf_speed)

        com_str = self.format_com()
        if self.debug_mode:
            print('turn_left', speed, com_str)
        if not self.test_mode:
            self.client.send_msg(com_str)

    def turn_right(self, speed = 0.5, reset_pwm = False):
        speed = np.clip(speed, -1, 1)

        if not reset_pwm:
            self.update_com(left_pwm=speed, right_pwm=speed)
        else:
            self.update_com(left_pwm=speed, right_pwm=speed, up_left_pwm=self.mid_leaf_speed, up_right_pwm=self.mid_leaf_speed)

        com_str = self.format_com()
        if self.debug_mode:
            print('turn_right', speed, com_str)
        if not self.test_mode:
            self.client.send_msg(com_str)

    def down(self, speed = 0.5, reset_pwm = False):
        speed = np.clip(self.mid_leaf_speed - speed, -1, 1)

        if not reset_pwm:
            self.update_com(up_left_pwm=-1*speed, up_right_pwm=speed)
        else:
            self.update_com(left_pwm=0, right_pwm=0, up_left_pwm=-1*speed, up_right_pwm=speed)

        com_str = self.format_com()
        if self.debug_mode:
            print('down', speed, com_str)
        if not self.test_mode:
            self.client.send_msg(com_str)

    def up(self, speed = 0.5, reset_pwm = False):
        speed = np.clip(self.mid_leaf_speed + speed, -1, 1)

        if not reset_pwm:
            self.update_com(up_left_pwm=-1*speed, up_right_pwm=speed)
        else:
            self.update_com(left_pwm=0, right_pwm=0, up_left_pwm=-1*speed, up_right_pwm=speed)


        com_str = self.format_com()
        if self.debug_mode:
            print('up', speed, com_str)
        if not self.test_mode:
            self.client.send_msg(com_str)

    def leaf_at_speed(self, speed = 0.5, reset_pwm = False):
        speed = np.clip(speed, -1, 1)

        if not reset_pwm:
            self.update_com(up_left_pwm=speed, up_right_pwm=-1*speed)
        else:
            self.update_com(left_pwm=0, right_pwm=0, up_left_pwm=speed, up_right_pwm=-1*speed)

        com_str = self.format_com()
        if self.debug_mode:
            print('up', speed, com_str)
        if not self.test_mode:
            self.client.send_msg(com_str)

    def set_cam(self, angle = -1, reset_pwm = True):
        angle = np.clip(angle, -1, 1)

        if reset_pwm:
            self.update_com(camera=angle)
        else:
            self.update_com(left_pwm=0, right_pwm=0, up_right_pwm=self.mid_leaf_speed, up_left_pwm=self.mid_leaf_speed, camera=angle)
        
        com_str = self.format_com()
        if self.debug_mode:
            print('camera angle', angle, com_str)
        if not self.test_mode:
            self.client.send_msg(com_str)

    def reset(self):
        # self.move_forward(0, True)
        self.set_cam(0, True)
        


if __name__ == "__main__":
    s = SmallRoboController(client = 1,debug_mode=True, test_mode=True)
    print(s.debug_mode)
    s.move_forward()
    s.up()
    s.down()
    s.leaf_at_speed()
    s.leaf_at_speed(reset_pwm=True)
    s.set_cam(0.5)
    s.reset()