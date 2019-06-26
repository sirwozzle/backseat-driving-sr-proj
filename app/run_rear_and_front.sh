#!/usr/bin/env bash
pwd
cd ..
source venv/bin/activate
which python3
cd app
python3 get_cam_ips.py #gets the camera ips
# run the rear code
python3 rear_cameras.py
#python3 splice_video_streams_with_processing.py &
#TODO make a python to do front camera only code