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
    cameras = ['rtsp://user:password@10.10.10.3/live', 'rtsp://user:password@10.10.10.4/live',
               'rtsp://user:password@10.10.10.5/live']
    cameras = ["rtsp://10.10.10.2:8554/unicast",1,1]
    # test(n_frames=60, width=1280, height=720, async=False,captureDevice=cameras[0])
    # test(n_frames=60, width=1280, height=720, async=True,captureDevice=cameras[0])

    cam1 = VideoCaptureAsync(cameras[0])
    #cam2 = VideoCaptureAsync(cameras[1])
    #cam3 = VideoCaptureAsync(cameras[2])
    cam1.start()
    #cam2.start()
    #cam3.start()
    while 1:
        #i = input("q to quit, enter for frame")
        #if i == 'q':
        #    break
        _,frame1,ts = cam1.read()
        #_,frame2 = cam2.read()
        #_,frame3 = cam3.read()
        #print(ts)
        cv2.imshow("cam1",frame1)
        #cv2.imshow("cam2",frame2)
        #cv2.imshow("cam3",frame3)

        cv2.waitKey(1) & 0xFF

        #print(type(frame1))

    cam1.stop()
    cam2.stop()

