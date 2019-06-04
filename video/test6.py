#i think same as 4?

import cv2,time




def list_supported_capture_properties(cap: cv2.VideoCapture):
    """ List the properties supported by the capture device.
    """
    supported = list()
    for attr in dir(cv2):
        if attr.startswith('CAP_PROP'):
            if cap.get(getattr(cv2, attr)) != -1:
                supported.append(attr)
    return supported

def get_size(frame):
    height = frame.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = frame.get(cv2.CAP_PROP_FRAME_WIDTH)
    size = str(height)+"x"+str(width)
    return size

#capture0 = cv2.VideoCapture(0)
#capture0.set(3,160)
#capture0.set(4,120)
capture1 = cv2.VideoCapture(2)
#capture1.set(3,1920)
#capture1.set(4,1080)
capture2 = cv2.VideoCapture(2)
#capture2.set(3,1920)
#capture2.set(4,1080)
#capture2.set(3,160)
#capture2.set(4,120)

#print(list_supported_capture_properties(capture1))

#print(capture1.get(9))
#capture1.set(9,1)
#capture2.set(9,1)
#print(capture1.get(9))

#exit(0)

print(get_size(capture1),get_size(capture2))
#capture3 = cv2.VideoCapture(6)
while 1:

    #ret0, img0 = capture0.read()
    ret1, img1 = capture1.read()

    ret2, img2 = capture2.read()
    print(type(img1),type(img2))


    #ret3, img02 = capture3.read()


    #img1 = cv2.resize(img0, (360, 240))
    #img2 = cv2.resize(img00, (360, 240))
    #img3 = cv2.resize(img01, (360, 240))
    #img4 = cv2.resize(img02, (360, 240))
    """
    if (capture0):
        cv2.imshow('img1', img1)
    if (capture1):
        cv2.imshow('img2', img2)
    if (capture2):
        cv2.imshow('img3', img3)
    """
    #if (capture0):
    #    cv2.imshow('img1', capture0.read()[0])
    if (capture1):
        #cv2.imshow('img2', capture1.read()[1])
        cv2.imshow('img2', img1)
    if (capture2):
        #cv2.imshow('img3', capture2.read()[1])
        cv2.imshow('img3', img2)
    #if (capture3):
    #    cv2.imshow('img4', img4)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


capture0.release()
capture1.release()
cv2.destroyAllWindows()
