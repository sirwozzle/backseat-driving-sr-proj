""""
copy fo test2
to display 3 cams at once
works
"""

import cv2
import time
import threading

from VideoCaptureAsync import VideoCaptureAsync


if __name__ == '__main__':
    cameras = ['rtsp://user:password@192.168.1.135/live', 'rtsp://user:password@192.168.1.136/live',
               'rtsp://user:password@192.168.1.137/live']

    # test(n_frames=60, width=1280, height=720, async=False,captureDevice=cameras[0])
    # test(n_frames=60, width=1280, height=720, async=True,captureDevice=cameras[0])

    cam1 = VideoCaptureAsync(cameras[0])
    cam2 = VideoCaptureAsync(cameras[1])
    cam3 = VideoCaptureAsync(cameras[2])
    cam1.start()
    cam2.start()
    cam3.start()
    while 1:
        #i = input("q to quit, enter for frame")
        #if i == 'q':
        #    break
        _,frame1 = cam1.read()
        _,frame2 = cam2.read()
        _,frame3 = cam3.read()
        cv2.imshow("cam1",frame1)
        cv2.imshow("cam2",frame2)
        cv2.imshow("cam3",frame3)

        cv2.waitKey(1) & 0xFF
        #TODO make wait for input per frame, have display all cams msec
        print(cam1.get(cv2.CAP_PROP_POS_MSEC))
        #print(type(frame1))

    cam1.stop()
    cam2.stop()

