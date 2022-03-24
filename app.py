import subprocess
import os
import signal
import cv2
from time import sleep

def yolo():
    bashCommand = "python3 detect.py --source 0 --weights best.pt --nosave --imgsz 640 --window 1"
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setpgrp)
    #output, error = process.communicate()
    return process

def kill_p(process):
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

imgs_path = "./images/"
imgs = os.listdir(imgs_path)
imgs_n = len(imgs)

vid_path = "./videos/"
vid = os.listdir(vid_path)
vid_n = len(vid)


#timer for images change
images_timer = 3000

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
    p = yolo()
    sleep(10)
    kill_p(p)

    #image loop
    #read all images in /images folder and display
    win = '3'
    for i in range(imgs_n):
        img = cv2.imread(imgs_path + imgs[i])
        cv2.namedWindow(win, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(win, img)
        cv2.waitKey(images_timer) 