from mmdet.apis import init_detector, inference_detector
import mmcv
import cv2 as cv
import numpy as np

# Specify the path to model config and checkpoint file
config_file = 'detect/configs/faster_rcnn_double_no_skip_no_lr_flops.py'
checkpoint_file = 'detect/checkpoint/epoch_24.pth'

# build the model from a config file and a checkpoint file
model = init_detector(config_file, checkpoint_file, device='cuda:0')
classes = ('echinus', 'holothurian', 'scallop', 'starfish', 'waterweeds')
colors = {'echinus':(255, 0, 0), 'holothurian':(0, 255, 0), 'scallop':(0, 0, 255), 'starfish':(255, 255, 0), 'waterweeds':(0, 0, 255)}

def inference_image(frame, thre = 0.5, post_proc = None):
    result = inference_detector(model, frame)
    bboxes = []
    for res in result:
        for r in res:
            bboxes.append(r[:-1])

    labels = []
    for idx, res in enumerate(result):
        for i in range(len(res)):
            labels.append(classes[idx])

    confidences = []
    for res in result:
        for r in res:
            confidences.append(r[-1])

    result = []
    for label, confi, bbox in zip(labels, confidences, bboxes):
        result.append((label, confi, bbox))
        if confi < thre:
            continue
        
        left, top, right, bottom = bbox
        cv.rectangle(frame, (left, top), (right, bottom), colors[label], 1)
        cv.putText(frame, "{} [{:.2f}]".format(label, float(confi)),
                    (int(left), int(top) - 5), fontFace = cv.FONT_HERSHEY_SIMPLEX, fontScale = 0.5,
                    color = colors[label], thickness = 1)

    if post_proc is None:
        return frame, result
    else:
        return frame, post_proc(result, frame.shape)
    

if __name__ == '__main__':
    cap = cv.VideoCapture('./var0.mp4')
    ret, frame = cap.read()
    while ret:
        ret, frame = cap.read()
        if not ret:
            break

        frame, result = inference_image(frame)
        cv.imshow('', frame)
        key = cv.waitKey(1)
        if key == 27:
            break
