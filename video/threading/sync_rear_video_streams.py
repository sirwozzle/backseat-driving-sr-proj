""""
work on sycning cameras 2,3
"""

import cv2
import time
import threading
import json

from VideoCaptureAsync import VideoCaptureAsync


class buffer:

    #TODO make buffer class, or intgreate class into asycn file
    # this way cam2_buffer = new buffer() and it holds the dicts, as well as lengths and optiosn to pop and push
    # first sync jsons, then make buffer that can be synced same way
    # buffers
    #actual buffers with timestamp:frame
    #cam2_buffer = dict()
    #cam3_buffer = dict()
    #buffer counter:timestamp per buffer
    #cam2_buffer_counter = dict()
    #cam3_buffer_counter = dict()
    #counter of how many frames in buffer
    #buffer_counter = 0
    #delay of how many to store before showing
    #frames_to_buffer = 90

    def __init__(self):
        #self.buffer = None
        self.buffer = []

    def add(self,to_add):
        #TODO make it take the actual tuple of time:frame and add to 2 dicts
        return



if __name__ == '__main__':
    cameras = ['rtsp://user:password@192.168.1.135/live', 'rtsp://user:password@192.168.1.136/live',
               'rtsp://user:password@192.168.1.137/live']

    # test(n_frames=60, width=1280, height=720, async=False,captureDevice=cameras[0])
    # test(n_frames=60, width=1280, height=720, async=True,captureDevice=cameras[0])

    # TODO time creation fo each cmaera and buffer the  length it takes, then playfrom buffer
    t0 = time.time()
    print("t0", t0)

    cam2 = VideoCaptureAsync(cameras[1])
    t0c2 = time.time()
    print("t0c2", t0c2)
    print("time to create cam2 " + str(t0c2 - t0) + "s\n")

    cam3 = VideoCaptureAsync(cameras[2])
    t0c3 = time.time()

    t1 = time.time()
    cam2.start()
    t1c2 = time.time()
    cam3.start()
    t1c3 = time.time()

    #TODO make buffer class, or intgreate class into asycn file
    # this way cam2_buffer = new buffer() and it holds the dicts, as well as lengths and optiosn to pop and push
    # first sync jsons, then make buffer that can be synced same way
    # buffers
    #actual buffers with timestamp:frame
    cam2_buffer = dict()
    cam3_buffer = dict()
    #buffer counter:timestamp per buffer
    cam2_buffer_counter = dict()
    cam3_buffer_counter = dict()
    #counter of how many frames in buffer
    buffer_counter = 0
    #delay of how many to store before showing
    frames_to_buffer = 90

    """
    with open("log.txt", "a") as l:
        l.write("time to create cam2 " + str(t0c2 - t0) + "\n")
        l.write("time to create cam3 " + str(t0c3 - t0c2) + "\n")
        l.write("time to start cam3 " + str(t1c2 - t1) + "\n")
        l.write("time to start cam3 " + str(t1c3 - t1c2) + "\n")

        l.close()

    print("t0 for cam2",cam2.get_time())
    print("t0 for cam3",cam3.get_time())
    """

    while 1:
        # i = input("q to quit, enter for frame")
        # if i == 'q':
        #    break

        #get the frames and print times
        #TODO rm times printing
        print("pr time for cam2", cam2.get_time())
        print("pr time for cam3", cam3.get_time())

        r2, frame2 = cam2.read()
        r3, frame3 = cam3.read()
        print("ar time for cam2", cam2.get_time())
        print("ar time for cam3", cam3.get_time())
        print("")

        #get the camera times
        cam2_time = cam2.get_time()
        cam3_time = cam3.get_time()
        # actual buffer
        #add the frame to the buffer marked via time
        cam2_buffer[cam2_time] = frame2
        cam3_buffer[cam3_time] = frame3
        #mark the time to the buffer counter so frames can be pulled later
        cam2_buffer_counter[buffer_counter] = cam2_time
        cam3_buffer_counter[buffer_counter] = cam3_time
        #cam2_buffer[cam2.get_time()] = "a"
        #cam3_buffer[cam3.get_time()] = "b"

        #once there is enough in the buffer
        if buffer_counter > frames_to_buffer:
            # if frames are returned
            #the display the ones from buffer
            if r2:
                #cv2.imshow("cam2", frame2)
                cv2.imshow("cam2", cam2_buffer[cam2_buffer_counter[buffer_counter]])
            if r3:
                #cv2.imshow("cam3", frame3)
                cv2.imshow("cam3", cam3_buffer[cam3_buffer_counter[buffer_counter]])

        # cv2.waitKey(1) & 0xFF
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        # TODO make wait for input per frame, have display all cams msec
        # print("1",cam1.get(cv2.CAP_PROP_POS_MSEC))
        # print("2",cam2.get(cv2.CAP_PROP_POS_MSEC))
        # print("3",cam3.get(cv2.CAP_PROP_POS_MSEC))

        buffer_counter+=1
    """
    with open("cam2.json","w") as o:
        json.dump(cam2_buffer,o)
        o.close()

    with open("cam3.json","w") as o:
        json.dump(cam3_buffer, o)
        o.close()
    """


    # cam1.stop()
    cam2.stop()
    cam3.stop()
