import os
from math import *

import cv2
import cv2 as cv
import numpy as np
from PIL import Image

def Applecut(img,x,y,w,h):
    # 计算长宽
    cut = img[y:y+h , x:x+w];
    cv.imshow("cut",cut);
    return cut;

def Getcolor (img ,height ,width):
    # 计算颜色均值
    R = 0;
    G = 0;
    B = 0;
    count = 1;
    color = [];
    for i in range(0, len(height), 1):
        count += 1;
        R += img[height[i], width[i]][0];
        G += img[height[i], width[i]][1];
        B += img[height[i], width[i]][2];
    R = int(R / count);
    G = int(G / count);
    B = int(B / count);
    color.append(R);
    color.append(G);
    color.append(B);
    return color;

def Getarea(img):
    count = 0
    point_height = []
    point_width = []
    height, width = img.shape
    for h in range(0, height, 1):
        for w in range(0, width, 1):
            if (img[h, w] == 0):
                count += 1
                point_height.append(h)
                point_width.append(w)
    return count, point_width, point_height

def Getcircum(img):
    count = 0
    height, width = img.shape
    for h in range(0, height, 1):
        for w in range(0, width, 1):
            if (img[h, w] == 255):
                count += 1
    return count

def del_files(dir_path):
    if os.path.isfile(dir_path):
        try:
            os.remove(dir_path) # 这个可以删除单个文件，不能删除文件夹
        except BaseException as e:
            print(e)
    elif os.path.isdir(dir_path):
        file_lis = os.listdir(dir_path)
        for file_name in file_lis:
            # if file_name != 'wibot.log':
            tf = os.path.join(dir_path, file_name)
            del_files(tf)
# 调用摄像头拍摄照片
def get_photo(framepath):
    cap = cv2.VideoCapture(0)           # 开启摄像头，0为本机，1或2为外设
    f, frame = cap.read()               # 将摄像头中的一帧图片数据保存
    cv2.imwrite(framepath, frame)     # 将图片保存为本地文件
    cap.release()                       # 关闭摄像头



