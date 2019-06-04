#reads the 3 wifi cameras and trys to display
#doesnt work cause of


import numpy as np
import cv2
import copy

#cap = cv2.VideoCapture('192.168.1.131:8081')
#cap2 = cv2.VideoCapture('http://192.168.1.131:8081')
one = cv2.VideoCapture('rtsp://user:password@192.168.1.135/live')
two = cv2.VideoCapture('rtsp://user:password@192.168.1.136/live')
three = cv2.VideoCapture('rtsp://user:password@192.168.1.137/live')
#cap1 = cv2.VideoCapture('http://192.168.1.134:8081')
#cap2 = cv2.VideoCapture('http://192.168.1.134:8081')
#cap3 = cv2.VideoCapture('http://192.168.1.134:8081')
#cap1 = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    #ret, frame = cap.read()
    try:
        ret, frame1 = one.read()
    except:
        print("cant read 1")
    try:
        ret, frame2 = two.read()
    except:
        print("cant read 2")
    try:
        ret, frame3 = three.read()
    except:
        print("cant read 3")
    #frame1 = cv2.resize(frame1, (1280, 720))
    #frame2 = cv2.resize(frame2, (1280, 720))
    #frame3 = cv2.resize(frame3, (1280, 720))

    #ret, frame1 = cap1.read()
    #ret, frame2 = cap2.read()
    #ret, frame3 = cap3.read()
    #ret, frame1 = cap1.read()

    # Our operations on the frame come here

    # Display the resulting frame
    #cv2.imshow('gray',gray)
    try:
        cv2.imshow('one',frame1)
    except:
        print("cant show 1")
    try:
        pass
        #cv2.imshow('two',frame2)
    except:
        print("cant show 2")
    try:
        pass
        #cv2.imshow('three',frame3)
    except:
        print("cant show 3")

    #cv2.imshow('built in',frame1)
    #cv2.imshow('steam again2',frame2)
    #cv2.imshow('steam again1',frame1)
    #cv2.imshow('steam again3',frame3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
one.release()
two.release()
three.release()
cv2.destroyAllWindows()


#TODO depth test
#addd to github repo