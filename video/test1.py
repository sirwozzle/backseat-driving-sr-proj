import numpy as np
import cv2
import copy

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(4)
cap3 = cv2.VideoCapture(6)
cap4 = cv2.VideoCapture(8)
cap5 = cv2.VideoCapture(10)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret1, frame1 = cap.read()
    ret2, frame2 = cap.read()
    ret3, frame3 = cap.read()
    ret4, frame4 = cap.read()
    ret5, frame5 = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imshow('gray',gray)
    cv2.imshow('built in',frame)
    cv2.imshow('1',frame1)
    cv2.imshow('2',frame2)
    cv2.imshow('3',frame3)
    cv2.imshow('4',frame4)
    cv2.imshow('5',frame5)

    frame_copy = copy.copy(frame)

    #cv2.imshow('normal copy',frame_copy)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


#TODO depth test
#addd to github repo