#test multiple usb cameras

import numpy as np
import cv2
import copy
from VideoCaptureAsync import VideoCaptureAsync
#from AsyncImageProcessWorker import AsyncImageProcessWorker,Jobs
from AsyncImageProcessJobs import Jobs

from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)


cap = VideoCaptureAsync(0)

#cap = cv2.VideoCapture(0)
cap.start()



ticks = Jobs.add_scale_to_top_of_image

def foo(bar, baz):
  print( 'hello '+bar)
  return 'foo' + baz



#starts the process
async_result = pool.apply_async(foo, ('world', 'foo')) # tuple of args for foo


# do some other stuff in the main process

return_val = async_result.get()  # get
print(return_val)

while(True):
    # Capture frame-by-frame
    ret, frame,ts = cap.read()
    # Display the resulting frame
    #cv2.imshow('gray',gray)



    cv2.imshow('built in',frame)
    ticked_frame = pool.apply_async(ticks,(frame,frame,10)).get()

    cv2.imshow('worked on',ticked_frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.stop()
cv2.destroyAllWindows()



#TODO depth test
#addd to github repo