import cv2
from modules import webcam
import time 
from openrdk import CommsRuntime
import subprocess
import threading
import os


capture = cv2.VideoCapture("/dev/video0",cv2.CAP_V4L2)
capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def camera():
    while True:
        frame = webcam.get_frame(capture)

        cv2.imwrite("Frame.jpg", frame)
        time.sleep(.3)

def test_ordk():
    time.sleep(5)
    openrdk = CommsRuntime(auto_start=False, enable_webview=False, enable_webview_updates=False)

def monitor():
    while True:
        print(os.path.exists("/dev/video0"))
        time.sleep(0.1)

thread_monitor = threading.Thread(target=monitor)
thread = threading.Thread(target= camera)
thread_ordk = threading.Thread(target = test_ordk)


thread_monitor.start()
thread.start()
time.sleep(5)
thread_ordk.start()
