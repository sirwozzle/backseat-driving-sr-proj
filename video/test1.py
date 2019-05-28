import numpy as np
import cv2
import copy

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('gray',gray)
    cv2.imshow('normal1',frame)

    frame_copy = copy.copy(frame)

    cv2.imshow('normal copy',frame_copy)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


#TODO depth test
#addd to github repo