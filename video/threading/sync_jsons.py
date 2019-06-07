
import json

with open("cam2.json", "r") as read_file:
    cam2_buffer = json.load(read_file)

with open("cam3.json", "r") as read_file:
    cam3_buffer = json.load(read_file)

print(cam2_buffer)
print(cam3_buffer)

cam2_current = None
cam3_current = None

#TODO read a few ahead maybe
buffer_counter = 0
for i,j in zip(cam2_buffer.keys(),cam3_buffer.keys()):
    #convert to int for easy mode
    k, l = int(float(i)),int(float(j))

    print(k,l)

    cam2_set = False
    cam3_set = False

    if cam2_current == None:
        cam2_current = k
        cam2_set = True
    if cam3_current == None:
        cam3_current = l
        cam3_set = True

    #if first run, then done
    if cam2_set and cam3_set:
        #TODO make this run once buffer has been filled, not actual first
        continue


    #if 2 > 3
    #TODO if greater than other+-100
    if k > l:
        print("2 ahead",k,l)
        cam2_set = True
    elif k < l:
        print("3 ahead",k,l)
        cam3_set = True
    elif k == l:
        print("same", k, l)

    #dont set the ahead one
    if not cam2_set:
        cam2_current = k

    if not cam3_set:
        cam3_current = l

    print("current values",cam2_current,cam3_current)

    buffer_counter+=1