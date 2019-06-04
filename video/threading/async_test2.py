""""
copy fo test1 but using rtsp camera
"""

import cv2
import time
from VideoCaptureAsync import VideoCaptureAsync

def test(n_frames=500, width=1280, height=720, async=False,captureDevice = 0):
    if async:
        cap = VideoCaptureAsync(captureDevice)
    else:
        cap = cv2.VideoCapture(captureDevice)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if async:
        cap.start()
    t0 = time.time()
    i = 0
    while i < n_frames:
        _, frame = cap.read()
        cv2.imshow('Frame', frame)
        cv2.waitKey(1) & 0xFF
        i += 1
    print('[i] Frames per second: {:.2f}, async={}'.format(n_frames / (time.time() - t0), async))
    if async:
        cap.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    cameras = ['rtsp://user:password@192.168.1.135/live', 'rtsp://user:password@192.168.1.136/live',
               'rtsp://user:password@192.168.1.137/live']

    test(n_frames=60, width=1280, height=720, async=False, captureDevice=cameras[0])
    test(n_frames=60, width=1280, height=720, async=True, captureDevice=cameras[0])

