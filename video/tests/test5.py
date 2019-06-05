"""
cycles through 4 usb cameras since cant open all at once

nick@nick-xps:~$ v4l2-ctl --list-devices

works cycles through all cameras on bus

"""
import cv2,time

vid_devices = [2,4,6,8]
index = 0
while 1:

    #print("index",index)
    #print("Opening /dev/video"+str(vid_devices[index]))
    capture0 = cv2.VideoCapture(vid_devices[index])
    capture0.set(3,1920)
    capture0.set(4,1080)


    ret0, img0 = capture0.read()
    #ret3, img02 = capture3.read()
    #img1 = cv2.resize(img0, (360, 240))
    #img4 = cv2.resize(img02, (360, 240))
    if (capture0):
        cv2.imshow('img', img0)
        time.sleep(.01)
        #capture0.release()
    if index <= len(vid_devices)-2:

        index+=1
    else:
        index=0

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

capture0.release()

cv2.destroyAllWindows()
