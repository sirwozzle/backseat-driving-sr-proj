
import threading
import cv2
import numpy as np
import time

#image processing jobs to be done
class Jobs:

    #adds a dash along top of the image
    def add_scale_to_top_of_image(self,src,every_n_pixels=10):
        #fixes the type for src, which is the input frame
        fix_type = type(src)

        depth_of_dashes = 20#pxs deep dashes

        #get the size of the image, then calculate which ones become dashes
        width = src.shape[1]

        #what x cords should it dash
        counter = 0
        dash_xs = []
        for p in range(0,width):
            if counter == every_n_pixels:
                dash_xs.append(p)
                counter=0
            counter+=1
        #print(dash_ys)

        for y in range(0,depth_of_dashes):
            for x in dash_xs:
                #print(x,y)
                src[y][x][0] = 255
                src[y][x][1] = 255
                src[y][x][2] = 255

        #print("src",src.shape)
        #print("n px",every_n_pixels)
        #return the final worked on image
        return src

    def smoothing_tests(self,src):
        kernel = np.ones((20, 20), np.float32) / 400
        dst = cv2.filter2D(src, -1, kernel)

        return dst

    def adjust_gamma(self,image):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        gamma = 2.0
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)


    def edges(self,src):#TODO steamline and make better
        #grayscale it
        im = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        # edges
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        # kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(im, -1, kernel)

        """
        #sharpen it
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(gray_image, -1, kernel)

        #edges
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        #kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(gray_image, -1, kernel)

        #dialte
        kernel = np.ones((5, 5), np.uint8)
        im = cv2.dilate(im, kernel, iterations=1)

        #sharpen again
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(im, -1, kernel)

        #sharpen again
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(im, -1, kernel)

        #here is good, just resdue noise

        kernel = np.ones((7, 7), np.float32) / 49
        im = cv2.filter2D(im, -1, kernel)
        kernel = np.ones((5, 5), np.float32) / 25
        im = cv2.filter2D(im, -1, kernel)

        # sharpen again
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(im, -1, kernel)
        """

        return im

    #uh, i did something..
    def matrix(self,src):
        #grayscale it
        gray_image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        #sharpen it
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(gray_image, -1, kernel)

        #edges
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        #kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(gray_image, -1, kernel)

        #dialte
        kernel = np.ones((5, 5), np.uint8)
        im = cv2.dilate(im, kernel, iterations=1)

        #sharpen again
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(im, -1, kernel)

        #sharpen again
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(im, -1, kernel)
        #sharpen again
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # kernel = np.array([[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1] [-1,-1, 8, -1,-1],[-1, -1, -1,-1,-1],[-1, -1, -1,-1,-1]])
        im = cv2.filter2D(im, -1, kernel)


        return im

    #takes a list of params as list
    def contours(self,input_list):

        font = cv2.FONT_HERSHEY_COMPLEX

        frame = input_list[0]
        hsv = cv2.cvtColor(input_list[0], cv2.COLOR_BGR2HSV)

        l_h = input_list[1]
        l_s = input_list[2]
        l_v = input_list[3]
        u_h = input_list[4]
        u_s = input_list[5]
        u_v = input_list[6]


        lower_red = np.array([l_h, l_s, l_v])
        upper_red = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower_red, upper_red)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel)

        # Contours detection
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if area > 400:
                cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

                if len(approx) == 3:
                    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
                elif len(approx) == 4:
                    cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
                elif 10 < len(approx) < 20:
                    cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))

        #cv2.imshow("Frame", frame)
        return frame



    #TODO fix freezing
    """
    [h264 @ 0x2027a00]
    error
    while decoding MB 8 24, bytestream -5
    [h264 @ 0x1bf1a80]
    error
    while decoding MB 57 26, bytestream -5
    """