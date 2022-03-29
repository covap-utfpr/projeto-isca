import subprocess
import os
import signal
import cv2
from time import sleep
import sys
import argparse

def yolo(weights,cam):
    bashCommand = "python3 detect.py --source "+cam+" --weights "+weights+" --nosave --imgsz 640 --window 1"
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setpgrp)
    #output, error = process.communicate()
    return process

def kill_p(process):
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

vid_path = "./videos/"
vid = os.listdir(vid_path)
vid_n = len(vid)


#timer for images change
images_timer = 3000

parser = argparse.ArgumentParser()
parser.add_argument('--cam', type=str)
args = parser.parse_args()

f = True
#main loop
while(f):
    
    #video loop
    #read all videos in /videos folder and display
    win = '0'
    for i in range(vid_n):
        cap = cv2.VideoCapture(vid_path + vid[i])
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                cv2.namedWindow(win, cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty(win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow(win, frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()

    #run yolo
    p1 = yolo("best.pt", args.cam)
    sleep(50)
    p2 = yolo("yolov5m.pt",args.cam)
    kill_p(p1)
    sleep(50)
    kill_p(p2)
