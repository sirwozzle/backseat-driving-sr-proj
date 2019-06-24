
import threading
import cv2
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
