from .base_planner import BasePlanner
import cv2 as cv
import _thread
import time
import numpy as np

class TradPlanner(BasePlanner):
    def __init__(self, config_file, camera, comunicator, inference_image, human_interupt = True):
        super().__init__(config_file)
        self.det = inference_image
        self.det_result = []
        self.cam = camera
        self.com = comunicator
        self.human_interupt = human_interupt
        self.auto = True
        self.det_result = []
        self.raw_det_result = []

        self.com.set_cam(-1)
        self.check_config()
        self.frame_shape = None
        _thread.start_new_thread(self.visual_sensor, ())
        # _thread.start_new_thread(self.proc_result, ())

    def check_config(self):
        if self.config is None:
            self.config = {
                'look_around_time' : 5,
                'turn_speed_ratio': 0.5,
                'route_time': 6,
                'route_choice_change_time': 2,
                'route_change_ratio': [6, 2, 2],
                'route_change_action': ['move_forward', 'turn_left', 'turn_right'],
                'route_change_speed': [0.5, 0.5, 0.5],
                'forward_speed_ratio': 0.5,
                'up_down_speed_ratio': 0.5,
            }
        else:
            if not hasattr(self.config, 'turn_speed_ratio'):
                self.config['turn_speed_ratio'] = 0.5
            if not hasattr(self.config, 'route_time'):
                self.config['route_time'] = 6
            if not hasattr(self.config, 'route_choice_change_time'):
                self.config['route_choice_change_time'] = 2
            if not hasattr(self.config, 'route_change_ratio'):
                self.config['route_change_ratio'] = [6, 2, 2]
                self.config['route_change_action'] = ['move_forward', 'turn_left', 'turn_right']
                self.config['route_change_speed'] = [0.5, 0.5, 0.5]
            if not hasattr(self.config, 'look_around_time'):
                self.config['look_around_time'] = 5
            if not hasattr(self.config, 'forward_speed_ratio'):
                self.config['forward_speed_ratio'] = 0.5
            if not hasattr(self.config, 'up_down_speed_ratio'):
                self.config['up_down_speed_ratio'] = 0.5

    def run(self):
        flag = False
        while True:
            if not self.auto:
                continue
            if not flag:
                flag = self.look_around()
            if flag:
                flag = self.navigate()
            else:
                flag = self.route()
            

    def route(self):           # random route
        self.call_hook('before_route')

        choice = self.rand_chose(self.config['route_change_ratio'])
        chose_func = self.config['route_change_action'][choice]
        speed = self.config['route_change_speed'][choice]
        start_time = time.time()
        chose_time = time.time()

        while time.time() - start_time < self.config['route_time']:

            if time.time() - chose_time < self.config['route_choice_change_time']:
                getattr(self.com, chose_func)(speed, reset_pwm=True)

            else:
                choice = self.rand_chose(self.config['route_change_ratio'])
                chose_func = self.config['route_change_action'][choice]
                speed = self.config['route_change_speed'][choice]
                chose_time = time.time()

            if len(self.det_result) > 0:
                return True

        self.call_hook('after_route')
        return False

    def navigate(self):
        self.call_hook('before_navigation')

        import time
        start_time = time.time()
        while True:
            if not self.auto:
                break

            det_result = self.det_result
            if len(det_result) == 0:
                # print('hahahahaha')
                time.sleep(0.05)
                return False
            # print(len(det_result))
            # print(center)
            obj_center = self.nearest_obj_center(det_result)
            print(obj_center)
            self.towards_center(obj_center)
            time.sleep(0.02)
            if time.time() - start_time > 10:
                break
            
        self.call_hook('after_navigation')
        return True

    def look_around(self):
        self.call_hook('before_look_around')
        start_time = time.time()
        while time.time() - start_time < self.config['look_around_time']:
            if not self.auto:
                break

            self.com.turn_left(self.config['turn_speed_ratio'])
            if len(self.det_result) > 0:
                return True
        self.call_hook('after_look_around')
        return False

    def visual_sensor(self, show = True):
        frame = self.cam.get_frame()
        if self.frame_shape is None:
            self.frame_shape = frame.shape

        while True:
            frame = self.cam.get_frame()
            det_frame, det_result = self.det(frame, post_proc=self.det_result_filter)
            if len(det_result) == 0:
                # self.det_result = []
                self.det_result.clear()
                pass
            else:
                self.det_result = det_result
            # self.raw_det_result = det_result
            # self.det_result = self.det_result_filter(det_result, det_frame.shape)
            # _thread.start_new_thread(self.proc_result, (det_frame.shape, ))
            if show:
                cv.imshow('det_frame', det_frame)
                key = cv.waitKey(1)

                if key == -1 or not self.human_interupt: # nothing
                    continue
                
                elif key == 27:  # esc
                    cv.destroyAllWindows()
                    self.auto = False
                    break
                
                elif key == 119: # w
                    self.com.move_forward(0.5, True)
                    pass
                elif key == 115: # s
                    self.com.move_forward(-0.5, True)
                    pass
                elif key == 97: # a
                    self.com.turn_left(0.5, True)
                    pass
                elif key == 100: # d
                    self.com.turn_right(0.5, True)
                    pass
                elif key == 105: # i
                    self.com.up(0.5, True)
                    pass
                elif key == 107: # k
                    self.com.down(0.5, True)
                    pass
                elif key == 56: # 8
                    cam = np.clip(cam + 0.05, -1, 1)
                    self.com.set_cam(cam)
                elif key == 50: # 2
                    cam = np.clip(cam - 0.05, -1, 1)
                    self.com.set_cam(cam)
                else:
                    continue

                self.auto = False

    
    def det_result_filter(self, det_result, frame_shape):
        det = []
        h, w, c = frame_shape
        
        for box in det_result:
            cat, cnf, bbox = box
            # tmp = (bbox[0]/w, bbox[1]/h, bbox[2], bbox[3])
            tmp = ((bbox[0] + bbox[2])/2/w, (bbox[1] + bbox[3])/2/h)  ######### center, w, h
            # tmp = ((bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2)
            tmp = (cat, float(cnf), tmp)
            try:
                if tmp[0] == 'starfish' or tmp[0] == 'waterweeds':
                    continue
                if tmp[1] < 0.3:
                    continue
            except:
                pass

            det.append(tmp)
        
        print(len(det_result), len(det))
        return det

    def nearest_obj_center(self, det_result):
        # print(len(det_result))
        bboxes = [det[2] for det in det_result]
        y_list = [obj[1] for obj in bboxes]
        idx = np.argmax(y_list)
        # print(det_result[idx])
        return bboxes[idx]

    def towards_center(self, center):
        w, h = center
        if w < 0.3:
            self.com.turn_left(self.config['turn_speed_ratio']/(max(1, 2*h)), reset_pwm=True)
        elif w > 0.7:
            self.com.turn_right(self.config['turn_speed_ratio']/(max(1, 2*h)), reset_pwm=True)
        elif h < 0.5:
            self.com.move_forward(self.config['forward_speed_ratio']/(max(1, 2*h)), reset_pwm=True)
            self.com.down(self.config['up_down_speed_ratio'])
        elif h > 0.7:
            self.com.down(self.config['up_down_speed_ratio'])
        
    def rand_chose(self, chose_list):
        rand_idx = np.random.randint(0, sum(chose_list))
        total_w = 0
        for idx, w in enumerate(chose_list):
            total_w += w
            if total_w >= rand_idx:
                return idx

    def proc_result(self):
        while self.frame_shape is None:
            time.sleep(0.1)
        
        while True:
            raw_result = self.raw_det_result
            det_result = self.det_result_filter(raw_result, self.frame_shape)
            self.det_result = det_result
            time.sleep(0.05)