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
import datetime


#splices left and right together with pixel columns from overlap removed
def splice(left, right,pixels_to_rm=0,height_offset=0):

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


    if height_offset >= 0:
        row_to_delete = right.shape[0] -1
        #do heigth change
        for i in range(0,height_offset):
            left = np.delete(left,0,0)
            right = np.delete(right,row_to_delete,0)
            row_to_delete-=1
    else:
        row_to_delete = left.shape[0] - 1
        # do heigth change
        for i in range(0, (-1*height_offset)):
            right = np.delete(right, 0, 0)
            left = np.delete(left, row_to_delete, 0)
            row_to_delete -= 1

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

#placeholder for trackbar
def nothing(x):
    # any operation
    pass

#adds padding to a frame to make it a desired resolution, if it is less
def add_padding_to_meet_res(frame,res_to_meet):
    #get the size that the padding has to be
    width_to_meet = res_to_meet[0]
    height_to_meet = res_to_meet[1]

    width = frame.shape[1]
    height = frame.shape[0]

    padding_height = height_to_meet-height
    padding_width = width_to_meet-width


    #add padding to bottom
    #make white rectangle of needed height and exisiting width
    img = np.zeros([padding_height, width, 3], dtype=np.uint8)
    img.fill(255)  # or img[:] = 255
    #add to frame
    frame = np.concatenate((frame, img), axis=0)

    # add padding to side
    # make rectangle of needed width and to_meet height
    img = np.zeros([height_to_meet, padding_width, 3], dtype=np.uint8)
    img.fill(255)  # or img[:] = 255
    # add to side
    frame = np.concatenate((frame, img), axis=1)

    #print(frame)
    #print(frame.shape)

    return frame


if __name__ == '__main__':


    #TODO make the trackbars and configs need an interactive flag, otherwise save values
    # to a json and load later
    #make trackbar window

    cv2.namedWindow("PX-to-cut")
    cv2.createTrackbar("PX-to-cut", "PX-to-cut", 0, 180, nothing)

    #TODO make toggle like above

    # contour trackbars
    cv2.namedWindow("Contour_Mask_controls")
    cv2.createTrackbar("L-H", "Contour_Mask_controls", 0, 180, nothing)
    cv2.createTrackbar("L-S", "Contour_Mask_controls", 66, 255, nothing)
    cv2.createTrackbar("L-V", "Contour_Mask_controls", 134, 255, nothing)
    cv2.createTrackbar("U-H", "Contour_Mask_controls", 180, 180, nothing)
    cv2.createTrackbar("U-S", "Contour_Mask_controls", 255, 255, nothing)
    cv2.createTrackbar("U-V", "Contour_Mask_controls", 243, 255, nothing)


    cv2.namedWindow("Height_offset")
    cv2.createTrackbar("Height_offset", "Height_offset", 0, 200, nothing)

    combined_res = (1920,540)

    output = True
    #TODO toggle output
    if output:
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #set resolution
        stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        name = "output_"+str(stamp)+".avi"
        out = cv2.VideoWriter(name, fourcc, 35.0, combined_res)

    #get cameras
    cameras = get_cameras()

    #only uses cameras 2,3 asa they aret the rear

    # cam1 = VideoCaptureAsync(cameras[0])
    cam2 = VideoCaptureAsync(cameras['2'])
    cam3 = VideoCaptureAsync(cameras['1'])

    #toggle comment if using webcams instead
    #cam2 = VideoCaptureAsync(0)

    # cam1.start()
    cam2.start()
    cam3.start()
    print("started")
    # multithreading bits
    pool = ThreadPool(processes=2)


    # define jobs
    ticker = Jobs.add_scale_to_top_of_image
    smoother = Jobs.smoothing_tests
    edge = Jobs.edges
    matrix = Jobs.matrix
    gamma = Jobs.adjust_gamma
    contours = Jobs.contours

    #number of pixels along the center line to remove (half from each image)
    pixels_to_cut = 0

    #height change for spliced frames
    height_offset = 100
    cv2.setTrackbarPos("Height_offset", "Height_offset", 100)



    #todo json load
    cv2.setTrackbarPos("Height_offset", "Height_offset", 73)
    cv2.setTrackbarPos("PX-to-cut", "PX-to-cut", 41)



    framerate = 0
    frames_captured = 0
    start_time = time.time()

    while 1:
        # i = input("q to quit, enter for frame")
        # if i == 'q':
        #    break

        # _,frame1,ts1 = cam1.read()
        _, frame2, ts2 = cam2.read()

        #print("_",_)
        #TODO lower res and ignore becasue time
        if not _:
            print("frame 2 not grabbed")
        #frame3 = copy.copy(frame2)
        _, frame3, ts3 = cam3.read()
        #print("_",_)
        if not _:
            print("frame 3 not grabbed")
        frames_captured+=1


        # adds scale at top fo img
        # frame2 = pool.apply_async(ticker, (frame2, frame2, 10)).get()
        # frame3 = pool.apply_async(ticker, (frame3, frame3, 10)).get()

        #frame2 = do_job_on_frame(ticker, frame2)
        #frame3 = do_job_on_frame(ticker, frame3)

        #TODO see rackbars init
        pixels_to_cut = cv2.getTrackbarPos("PX-to-cut", "PX-to-cut")

        #make height offset on scale -100 - 100
        height_offset = cv2.getTrackbarPos("Height_offset", "Height_offset")-100

        frame23 = splice(left=frame2, right=frame3,pixels_to_rm=pixels_to_cut,height_offset=height_offset);


        #TODO rm
        #outframe23 = add_padding_to_meet_res(frame23, (2560, 720))
        #cv2.imshow("outframe",outframe23)
        if output:
            outframe23 = add_padding_to_meet_res(frame23,combined_res)
            out.write(outframe23)

        # cv2.imshow("cam1",frame1)
        # orgin splice

        cv2.imshow("cam23", frame23)

        # frame23blur = pool.apply_async(smoother, (frame23, frame23)).get()

        # cv2.imshow("cam23blur",frame23blur)

        #frame23gamma = do_job_on_frame(gamma,frame23)
        #cv2.imshow("23 gamma",frame23gamma)


        # frame23edges = pool.apply_async(edge, (frame23, frame23)).get()
        frame23edges = do_job_on_frame(edge,frame23)

        cv2.imshow("cam23sharp", frame23edges)



        #TODO contours toggle again
        l_h = cv2.getTrackbarPos("L-H", "Contour_Mask_controls")
        l_s = cv2.getTrackbarPos("L-S", "Contour_Mask_controls")
        l_v = cv2.getTrackbarPos("L-V", "Contour_Mask_controls")
        u_h = cv2.getTrackbarPos("U-H", "Contour_Mask_controls")
        u_s = cv2.getTrackbarPos("U-S", "Contour_Mask_controls")
        u_v = cv2.getTrackbarPos("U-V", "Contour_Mask_controls")

        #TODO renable
        #frame23contours = do_job_on_frame(contours,[frame23,l_h,l_s,l_v,u_h,u_s,u_v])

        #cv2.imshow("frame23contours",frame23contours)


        #frame23edgecontours = do_job_on_frame(contours,[frame23edges,l_h,l_s,l_v,u_h,u_s,u_v])

        #cv2.imshow("frame23contours",frame23edgecontours)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    end_time = time.time()
    framerate = frames_captured/(end_time-start_time)
    print("framerate was ",framerate)
    print("elapsted time was "+str(end_time-start_time)+" seconds")
    # qcam1.stop()
    cam2.stop()
    cam3.stop()
    if output:
        out.release()

    print("px_to_cut",pixels_to_cut)
    print("height offset",height_offset)
