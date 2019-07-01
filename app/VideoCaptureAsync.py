"""

class from
http://blog.blitzblit.com/2017/12/24/asynchronous-video-capture-in-python-with-opencv/

"""

import threading
import cv2
import time
import datetime
import os

global error_dir
error_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),"error_logs")


class VideoCaptureAsync:
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.is_ok = True
        #try to read video source
        self.cap = cv2.VideoCapture(self.src)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()


    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def get(self, propId):
        return self.cap.get(propId)

    # returns the cameras internal time
    def get_time(self):
        return self.cap.get(cv2.CAP_PROP_POS_MSEC)

    def start(self):
        if self.started:
            print('[!] Asynchroneous video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            # TODO make better warning
            if not grabbed:
                stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
                filename = str(stamp)+".txt"
                with open(os.path.join(error_dir,filename),"w") as error_file:
                    error_file.write("frame not grabbed, maybe frozen")
                    error_file.close()
                print("Frame from "+str(self.src)+" not grabbed")
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    #returns if frame is grabbed, the frame and the timestamp
    def read(self):
        with self.read_lock:
            grabbed = self.grabbed
            if not self.grabbed:
                #print("Failed to grab frame, trying again in .1s")
                return self.read()
            frame = self.frame.copy()
            ts = self.get_time()
        return grabbed, frame, ts

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
