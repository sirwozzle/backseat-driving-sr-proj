import numpy as np
import cv2
import copy


import threading

import time


def get_size(frame):
    height = frame.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = frame.get(cv2.CAP_PROP_FRAME_WIDTH)
    size = str(height)+"x"+str(width)
    return size


def thread_cam(video_input,video_name):
    cap = cv2.VideoCapture(video_input)
    print("cap",type(cap))
    while(True):
        ret, frame = cap.read()
        #print(type(frame))
        #print(get_size(cap))
        if video_name == "1":
            global frame1
            frame1 = frame
            cv2.imshow(video_name, frame)


#cap = cv2.VideoCapture('192.168.1.131:8081')
#cap2 = cv2.VideoCapture('http://192.168.1.131:8081')
#cap = cv2.VideoCapture('http://192.168.1.134:8081')
#cap1 = cv2.VideoCapture('http://192.168.1.134:8081')
#cap2 = cv2.VideoCapture('http://192.168.1.134:8081')
#cap3 = cv2.VideoCapture('http://192.168.1.134:8081')

global frame1
frame1 = None


camera_inputs = ['http://192.168.1.134:8081','http://192.168.1.134:8081','http://192.168.1.134:8081','http://192.168.1.134:8081']
camera_names = ["1","2","3","4"]

a = threading.Thread(target=thread_cam,args=(camera_inputs[0],camera_names[0],))
print("made a")
b = threading.Thread(target=thread_cam,args=(camera_inputs[1],camera_names[1],))
print("made b")
c = threading.Thread(target=thread_cam,args=(camera_inputs[2],camera_names[2],))
print("made c")
d = threading.Thread(target=thread_cam,args=(camera_inputs[3],camera_names[3],))
print("made d")

a.start()
print("started a")
b.start()
print("started b")
c.start()
print("started c")
d.start()
print("started d")


while(True):
    try:
        cv2.imshow("name",frame1)
    except:
        pass