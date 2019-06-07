""""
copy fo test2
combine multiple streams into 1 frame
works but freezes stream1???
"""

import cv2
import time
import threading
import numpy as np
from VideoCaptureAsync import VideoCaptureAsync

def splice(left,right):

    combined = np.concatenate((left, right), axis=1)

    return combined
    """
    if left.shape != right.shape:
        print("Mismatched sized frames")
        print("I aint dealing with those yet")
        print("left shape"+str(left.shape))
        print("right shape"+str(right.shape))




    print("l shape",left.shape)
    print("r shape",right.shape)
    print("r shape",type(right.shape))
    print("l dtype",left.dtype)
    print("r dtype",right.dtype)

    #assume right and left frames are the same and double width of the left to add in the right
    new_shape = (left.shape[0],left.shape[1]*2,left.shape[2])

    print("New shape",new_shape)

    combined = np.ndarray(shape=new_shape,dtype=left.dtype)
    print("combined shape",combined.shape)

    #print(combined)

    #copy all of left into combined
    row_counter = 0
    col_counter = 0
    for row in left:
        for col in left:

            #print("l",row_counter,col_counter)
            #print(row_counter,left[row_counter][col_counter])
            combined[row_counter][col_counter] = left[row_counter][col_counter]

            col_counter+=1
        col_counter = 0
        row_counter+=1
    #copy all of right into the image
    row_counter = 0
    col_counter = 0
    for row in right:
        for col in right:
            #print("r", row_counter, col_counter)

            combined[row_counter][col_counter+new_shape[0]-1] = right[row_counter][col_counter]

            col_counter += 1
        col_counter = 0
        row_counter += 1

    #np.ndarray(shape=(2, 2), dtype=float, order='F')

    return combined
    """



if __name__ == '__main__':
    #cameras = ['rtsp://user:password@192.168.1.135/live', 'rtsp://user:password@192.168.1.136/live',
    #           'rtsp://user:password@192.168.1.137/live']
    cameras = ['rtsp://user:password@10.10.10.3/live', 'rtsp://user:password@10.10.10.4/live',
               'rtsp://user:password@10.10.10.5/live']

    #cameras = [0,0,0]
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

        frame23 = splice(left=frame2,right=frame3);

        cv2.imshow("cam1",frame1)
        cv2.imshow("cam23",frame23)

        cv2.waitKey(1) & 0xFF
        #TODO make wait for input per frame, have display all cams msec
        #print(cam1.get(cv2.CAP_PROP_POS_MSEC))
        #print(type(frame1))

    cam1.stop()
    cam2.stop()
    cam3.stop()

