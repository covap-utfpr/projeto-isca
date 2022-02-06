#!/bin/bash

cd yolov5/
python3 detect.py --source 0 --weights best.pt --nosave
