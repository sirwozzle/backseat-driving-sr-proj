""""
copy of rear but just diaplays camera 1
"""

import cv2
import time
import json
import numpy as np
from VideoCaptureAsync import VideoCaptureAsync
from AsyncImageProcessJobs import Jobs
from multiprocessing.pool import ThreadPool
import copy


#load camera json to dict
def get_cameras():
    with open("cameras.json", "r") as read_file:
        cameras = json.load(read_file)
    return cameras

#does a image processing job on a frame in its own thread
def do_job_on_frame(job, frame):
    return_frame = pool.apply_async(job, (frame, frame)).get()
    return return_frame


if __name__ == '__main__':

    #get cameras
    cameras = get_cameras()

    #only uses cameras 2,3 asa they aret the rear

    cam1 = VideoCaptureAsync(cameras['3'])
    cam1.start()
    print("started")
    # multithreading bits
    pool = ThreadPool(processes=1)

    # TODO add output option
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 20.0, (2560, 720))

    # define jobs
    ticker = Jobs.add_scale_to_top_of_image
    smoother = Jobs.smoothing_tests
    edge = Jobs.edges
    matrix = Jobs.matrix
    gamma = Jobs.adjust_gamma

    #number of pixels along the center line to remove (half from each image)
    pixels_to_cut = 10

    while 1:
        # i = input("q to quit, enter for frame")
        # if i == 'q':
        #    break

        _,frame1,ts1 = cam1.read()

        #TODO un fisheye cameras

        # adds scale at top fo img
        # frame2 = pool.apply_async(ticker, (frame2, frame2, 10)).get()
        # frame3 = pool.apply_async(ticker, (frame3, frame3, 10)).get()

        #frame2 = do_job_on_frame(ticker, frame2)
        #frame3 = do_job_on_frame(ticker, frame3)

        cv2.imshow("cam1",frame1)

        frame1edge = do_job_on_frame(edge,frame1)
        cv2.imshow("cam1edge", frame1edge)

        # orgin splice

        # out.write(frame23sharp)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cam1.stop()
    # out.release()
