from VideoCaptureAsync import VideoCaptureAsync
import subprocess
import json

#independant script, just makes json, todo make this called by main rogrm at startup

def make_json():

    live_addresses = []

    print("Searching for cameras on hootoo 10.10.10.1/24 network")
    #somehwere in first 10 hosts is the cameras
    for ping in range(1, 10):
        address = "10.10.10." + str(ping)
        res = subprocess.call(['ping', '-c', '1', address], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        if res == 0:
            live_addresses.append(address)
            #print("ping to", address, "OK")
        elif res == 2:
            pass
            #print("no response from", address)
        else:
            pass
            #print("ping to", address, "failed!")


    print("Found "+str(len(live_addresses))+" hosts")

    cameras = dict()
    camera_count = 1

    #for every address on the network try to open a camera
    for address in live_addresses:
        cam_addr = "rtsp://"+address+":8554/unicast"
        #try to connect to all address as a camera, if it doesnt work, dont add to list
        try:
            cam = VideoCaptureAsync(cam_addr)
            if cam.grabbed:
                cameras[camera_count] = cam_addr
                camera_count+=1
        except:
            pass
    print("Found "+str(len(cameras))+" cameras")

    with open("cameras.json", "w") as o:
        json.dump(cameras, o)
        o.close()
    print("Output to cameras.json")

make_json()