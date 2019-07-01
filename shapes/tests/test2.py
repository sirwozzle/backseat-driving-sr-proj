import cv2
import numpy as np
from AsyncImageProcessJobs import Jobs
from multiprocessing.pool import ThreadPool

def nothing(x):
    # any operation
    pass


#does a image processing job on a frame in its own thread
def do_job_on_frame(job, frame):
    return_frame = pool.apply_async(job, (frame, frame)).get()
    return return_frame


pool = ThreadPool(processes=2)
edge = Jobs.edges
blur = Jobs.smoothing_tests
gamma = Jobs.adjust_gamma
matrix = Jobs.matrix

cap = cv2.VideoCapture(0)


font = cv2.FONT_HERSHEY_COMPLEX

while True:
    _, frame = cap.read()
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    #l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    #l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    #u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    #u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    #u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    #lower_red = np.array([l_h, l_s, l_v])
    #upper_red = np.array([u_h, u_s, u_v])

    #mask = cv2.inRange(hsv, lower_red, upper_red)
    #mask = cv2.erode(mask, kernel)
    mask = do_job_on_frame(gamma,frame)

    mask = do_job_on_frame(edge,frame)
    kernel = np.ones((8, 8), np.uint8)

    kernel = np.ones((10, 10), np.float32) / 25
    #mask = cv2.filter2D(mask, -1, kernel)

    #mask = do_job_on_frame(gamma,mask)

    #mask = cv2.dilate(mask,kernel)
    #mask = do_job_on_frame(blur,mask)
    # Contours detection
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 100:
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

            if len(approx) == 3:
                cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
            elif len(approx) == 4:
                cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
            elif 10 < len(approx) < 20:
                cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))


    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()