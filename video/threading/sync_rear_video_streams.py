""""
work on sycning cameras 2,3
"""

import cv2
import time
import threading
import json

from VideoCaptureAsync import VideoCaptureAsync


class buffer:

    def __init__(self,max_length=5):
        #self.buffer = None
        self.length = 0;
        self.frames = []
        self.times = []
        self.time_to_frame = dict()
        #defautl max len to 5
        self.max_length = max_length

    def add(self,frame,timestamp):
        self.frames.append(frame)
        self.times.append(timestamp)
        self.time_to_frame[timestamp] = frame
        self.length+=1

        self.prune()
        return

    def prune(self):
        if self.length >= self.max_length:
            self.frames.pop(0)
            self.times.pop(0)
            self.length-=1
        return

    #returns frame by timestamp, if timestamp doesnt exist, uses index
    def get_frame(self,index):
        if index in self.time_to_frame.keys():
            return self.time_to_frame[index]
        #print("getting frame ",index)
        return self.frames[index]


    def get_time(self,index):
        return self.times[index]

    def get_length(self):
        return self.length

def clear_currents(cam2_current,cam3_current):
    print("PLACEHOLDER TO DISPLAY A FRAME")
    print("cam2",cam2_current,"cam3",cam3_current)
    cam2_current = None
    cam3_current = None
    #print("")
    return cam2_current,cam3_current

def get_frames_to_display(cam2_current,cam3_current,cam2_buffer,cam3_buffer):
    return cam2_buffer.get_frame(cam2_current), cam3_buffer.get_frame(cam3_current)


#return if a and b are withing a range of eachother
def within_range(a,b,range):
    if a > b:
        if a-range <= b:
            return True
        if b + range >= a:
            return True
    if a < b:
        if a + range >= b:
            return True
        if b - range <= a:
            return True
    return False


if __name__ == '__main__':
    #cameras = ['rtsp://user:password@192.168.1.135/live', 'rtsp://user:password@192.168.1.136/live',
    #           'rtsp://user:password@192.168.1.137/live']
    cameras = ["rtsp://10.10.10.2:8554/unicast","rtsp://10.10.10.4:8554/unicast"]

    # test(n_frames=60, width=1280, height=720, async=False,captureDevice=cameras[0])
    # test(n_frames=60, width=1280, height=720, async=True,captureDevice=cameras[0])

    # TODO time creation fo each cmaera and buffer the  length it takes, then playfrom buffer
    t0 = time.time()
    print("t0", t0)

    cam2 = VideoCaptureAsync(cameras[1])
    t0c2 = time.time()
    print("t0c2", t0c2)
    print("time to create cam2 " + str(t0c2 - t0) + "s\n")

    cam3 = VideoCaptureAsync(cameras[0])
    t0c3 = time.time()

    t1 = time.time()
    cam2.start()
    t1c2 = time.time()
    cam3.start()
    t1c3 = time.time()


    #counter of how many frames in buffer
    buffer_counter = 0
    #delay of how many to store before showing
    frames_to_buffer = 100
    #create buffers that hold last 100 frames
    buffer_length = 400
    cam2_buffer = buffer(buffer_length)
    cam3_buffer = buffer(buffer_length)

    #frame_to_grab_from_buffer = int((buffer_length/3)*2)
    frame_to_grab_from_buffer = 70

    #number of ms that is allowed difference between frames to display them
    allowed_time_ahead = 75


    cam2_current = None
    cam3_current = None
    showing_frames_this_run = False

    while 1:
        # i = input("q to quit, enter for frame")
        # if i == 'q':
        #    break


        #read from cameras, getting frame and timestamp
        r2, frame2,ts2 = cam2.read()
        r3, frame3,ts3 = cam3.read()
        #if frames are returned, add to buffer
        if r2:
            cam2_buffer.add(frame2,ts2)
        if r3:
            cam3_buffer.add(frame3,ts3)



        #once there is enough in the buffer
        if buffer_counter > frames_to_buffer:

            #todo get the times at the buffers and use that to ask what index to get
            # if frames are returned

            #TODO always get 0th frame in the buffer (or maybe always the middle frame?)
            # and then compare the times, try to scrub fwd or back to find match
            cam2_ts = cam2_buffer.get_time(frame_to_grab_from_buffer)
            cam3_ts = cam3_buffer.get_time(frame_to_grab_from_buffer)
            #print("cam2 time",cam2_ts,"cam2 current",cam2_current)
            #print("cam3 time",cam3_ts,"cam3 current",cam3_current)

            #TODO first check who is ahead from live grab
            # then check if its ahead of the current set frames

            #the camera ahead is saved and other one allowed to continue
            if cam2_ts > cam3_ts + allowed_time_ahead:
                #print("cam2 ahead")
                if cam2_current == None:
                    cam2_current = cam2_ts
            elif cam3_ts > cam2_ts + allowed_time_ahead:
                #print("cam3 ahead")
                if cam3_current == None:
                    cam3_current = cam3_ts
            else:
                #print("sync")
                #fn to display the current selected frames
                cam2_current = cam2_ts
                cam3_current = cam3_ts
                #TODO display first
                showing_frames_this_run = True
                frame2 ,frame3 = get_frames_to_display(cam2_current,cam3_current,cam2_buffer,cam3_buffer)
                cam2_current,cam3_current = clear_currents(cam2_current,cam3_current)

            #if they both been set, then go
            if cam2_current != None and cam3_current != None:
                #TODO display first
                showing_frames_this_run = True
                frame2 ,frame3 = get_frames_to_display(cam2_current,cam3_current,cam2_buffer,cam3_buffer)
                cam2_current,cam3_current = clear_currents(cam2_current,cam3_current)
            else:
                #check that the new ts is close enough to the set current
                if cam2_current != None:
                    if within_range(cam2_current,cam3_ts,allowed_time_ahead):
                        cam3_current = cam3_ts
                if cam3_current != None:
                    if within_range(cam3_current,cam2_ts,allowed_time_ahead):
                        cam2_current = cam2_ts


            # if they both been set, then go
            if cam2_current != None and cam3_current != None:
                #TODO display first
                showing_frames_this_run = True
                frame2 ,frame3 = get_frames_to_display(cam2_current,cam3_current,cam2_buffer,cam3_buffer)
                cam2_current, cam3_current = clear_currents(cam2_current, cam3_current)

            #TODO rm the and False
            if showing_frames_this_run:
                cv2.imshow("cam2", frame2)
                cv2.imshow("cam2", frame2)
                cv2.imshow("cam3", frame3)
                cv2.imshow("cam3", frame3)
                showing_frames_this_run = False



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

    print(cam2_buffer.length)
    print(cam2_buffer.counts)
    print(cam2_buffer.times)