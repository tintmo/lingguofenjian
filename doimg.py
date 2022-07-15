from math import *
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




