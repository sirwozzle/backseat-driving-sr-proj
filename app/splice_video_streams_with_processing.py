""""
copy fo test2
combine multiple streams into 1 frame
works but freezes stream1???
"""

import cv2
import time
import json
import numpy as np
from VideoCaptureAsync import VideoCaptureAsync
from AsyncImageProcessJobs import Jobs
from multiprocessing.pool import ThreadPool


def splice(left,right):

    combined = np.concatenate((left, right), axis=1)

    return combined

def get_cameras():

    with open("cameras.json", "r") as read_file:
        cameras = json.load(read_file)
    return cameras



if __name__ == '__main__':
    #cameras = ['rtsp://user:password@192.168.1.135/live', 'rtsp://user:password@192.168.1.136/live',
    #           'rtsp://user:password@192.168.1.137/live']
    #cameras = ['rtsp://user:password@10.10.10.3/live', 'rtsp://user:password@10.10.10.4/live',
    #           'rtsp://user:password@10.10.10.5/live']

    #cameras = ["rtsp://10.10.10.2:8554/unicast","rtsp://10.10.10.3:8554/unicast","rtsp://10.10.10.4:8554/unicast"]

    cameras = get_cameras()


    #cameras = [0,0,0]
    # test(n_frames=60, width=1280, height=720, async=False,captureDevice=cameras[0])
    # test(n_frames=60, width=1280, height=720, async=True,captureDevice=cameras[0])

    #cam1 = VideoCaptureAsync(cameras[0])
    cam2 = VideoCaptureAsync(cameras['1'])
    cam3 = VideoCaptureAsync(cameras['2'])
    #cam1.start()
    cam2.start()
    cam3.start()

    #multithreading bits
    pool = ThreadPool(processes=2)

    ticker = Jobs.add_scale_to_top_of_image

    while 1:
        #i = input("q to quit, enter for frame")
        #if i == 'q':
        #    break

        #_,frame1,ts1 = cam1.read()
        _,frame2,ts2 = cam2.read()
        _,frame3,ts3 = cam3.read()

        frame2 = pool.apply_async(ticker, (frame2, frame2, 10)).get()
        frame3 = pool.apply_async(ticker, (frame3, frame3, 10)).get()

        frame23 = splice(left=frame2,right=frame3);

        #cv2.imshow("cam1",frame1)
        cv2.imshow("cam23",frame23)

        cv2.waitKey(1) & 0xFF
        #TODO make wait for input per frame, have display all cams msec
        #print(cam1.get(cv2.CAP_PROP_POS_MSEC))
        #print(type(frame1))

    cam1.stop()
    cam2.stop()
    cam3.stop()

