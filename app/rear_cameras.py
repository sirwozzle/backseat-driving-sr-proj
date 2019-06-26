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
import copy


#splices left and right together with pixel columns from overlap removed
def splice(left, right,pixels_to_rm=0):

    #get width of left image
    left_width = left.shape[1]
    #split pixles to remove between the 2 halfs
    cols_to_rm_from_left = int(pixels_to_rm/2)
    cols_to_rm_from_right = pixels_to_rm-cols_to_rm_from_left

    #remove from left
    for i in range(0,cols_to_rm_from_left):
        col_to_delete=left_width-1
        left = np.delete(left, col_to_delete, 1)  # delete last col of left
        left_width-=1

    # remove from right
    for i in range(0, cols_to_rm_from_right):
        right = np.delete(right, 0, 1)  # delete first col of right

    #combine
    combined = np.concatenate((left, right), axis=1)

    return combined

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

    # cam1 = VideoCaptureAsync(cameras[0])
    cam2 = VideoCaptureAsync(cameras['2'])
    cam3 = VideoCaptureAsync(cameras['3'])
    # cam1.start()
    cam2.start()
    cam3.start()
    print("started")
    # multithreading bits
    pool = ThreadPool(processes=2)

    # TODO add output option
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 20.0, (2560, 720))

    # define jobs
    ticker = Jobs.add_scale_to_top_of_image
    smoother = Jobs.smoothing_tests
    edge = Jobs.edges
    matrix = Jobs.matrix

    #number of pixels along the center line to remove (half from each image)
    pixels_to_cut = 10

    while 1:
        # i = input("q to quit, enter for frame")
        # if i == 'q':
        #    break

        # _,frame1,ts1 = cam1.read()
        _, frame2, ts2 = cam2.read()
        _, frame3, ts3 = cam3.read()

        # adds scale at top fo img
        # frame2 = pool.apply_async(ticker, (frame2, frame2, 10)).get()
        # frame3 = pool.apply_async(ticker, (frame3, frame3, 10)).get()

        frame2 = do_job_on_frame(ticker, frame2)
        frame3 = do_job_on_frame(ticker, frame3)
        frame23 = splice(left=frame2, right=frame3,pixels_to_rm=pixels_to_cut);

        # cv2.imshow("cam1",frame1)
        # orgin splice

        cv2.imshow("cam23", frame23)

        # frame23blur = pool.apply_async(smoother, (frame23, frame23)).get()

        # cv2.imshow("cam23blur",frame23blur)

        # frame23edges = pool.apply_async(edge, (frame23, frame23)).get()
        #frame23edges = do_job_on_frame(edge,frame23)

        #cv2.imshow("cam23sharp", frame23edges)

        # out.write(frame23sharp)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # qcam1.stop()
    cam2.stop()
    cam3.stop()
    # out.release()
