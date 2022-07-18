import os
from math import *

import cv2

from doimg import *
import cv2 as cv
import numpy as np
from PIL import Image
import pandas as pd
import xlwt
import openpyxl

framepath = "frame\\frame.png"
imglist=[
    'imgfile\\1.png'
    'imgfile\\2.png'
    'imgfile\\3.png'
    'imgfile\\4.png'
    'imgfile\\5.png'
]
appledatapath = pd.ExcelWriter("imgfile\\appledata.xlsx")
# imgf=open("..imgf",'w+')
if not os.path.exists('imgfile\\appledata.xlsx'):
    appledata = pd.DataFrame()
    appledata1 = appledata.to_excel("imgfile\\appledata.xlsx",'1')


weights = np.array([0, 1]) # w1 = 0, w2 = 1
bias = 4




def edge(img):
    # 灰度图像
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 高斯模糊,降低噪声
    blurred = cv.GaussianBlur(gray, (3, 3), 0)
    # 图像梯度
    xgrad = cv.Sobel(blurred, cv.CV_16SC1, 1, 0)
    ygrad = cv.Sobel(blurred, cv.CV_16SC1, 0, 1)
    # 计算边缘
    # 50和150参数必须符合1：3或者1：2
    edge_output = cv.Canny(xgrad, ygrad, 50, 150)

    contours, heriachy = cv.findContours(edge_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # max = 0
    # maxA = 0
    num = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv.boundingRect(contour)
        # if (w * h > maxA):
        #     max = i
        #     maxA = w * h

        if w < 50 or h < 50:
            continue
        num.append(i)

    for i in num:
        # cv.drawContours(img, contours, i, (0, 0, 255), 2)
        # x, y, w, h = cv.boundingRect(contours[i])
        # img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if i == 0:
            continue
        contours=list(contours)
        contours[0] = np.concatenate((contours[i], contours[0]))

    cv.imshow('img', img)
    x, y, w, h = cv.boundingRect(contours[0])

    cut_img = Applecut(img, x, y, w, h)
    cut_blurred = Applecut(blurred, x, y, w, h)
    cv.imshow('cut', cut_blurred)

    ret, binary = cv.threshold(cut_blurred, 150, 255, cv.THRESH_BINARY)
    cv.imshow("bi", binary)  # 求面积

    edge = cv.Canny(binary, 40, 100)
    cv.imshow("edge", edge)  # 求周长

    longth = 0
    width = 0
    if w > h:
        longth = w
        width = h
    else:
        longth = h
        width = w
    area, point_width, point_height = Getarea(binary)
    circumference = Getcircum(edge)
    color = Getcolor(cut_img, point_height, point_width)
    relist=[area,circumference,longth,width,color]
    print('area:', area, 'circumference:', circumference, 'longth:', longth, 'width:', width, 'color:', color)
    return relist


def do():
    for j in range(1, 16, 1):
        path = "imgfile\\" + str(j) + '.png'
        src2 = cv.imread(path)
        size = src2.shape
        src3 = cv.resize(src2, ((int)(size[1] / 5), (int)(size[0] / 5)), cv.INTER_LINEAR)
        datalist = edge(src3)
        dataframe = pd.DataFrame({'index':[j],'面积':[datalist[0]],'颜色':[datalist[4]]})
        print(dataframe)
        dataframe.to_excel(appledatapath,'1')
        appledatapath.save()
    appledatapath.close()


    for i in range(1, 20, 1):
        print(i, ':')
        #         path = file + str(i) + '.jpg'

        #         src1 = cv.imread(path)

        get_photo(framepath)
        src1 = cv.imread(framepath)
        img=Image.open(framepath)
        # 图三（原图）
        size = src1.shape
        src = cv.resize(src1, ((int)(size[1] / 5), (int)(size[0] / 5)), cv.INTER_LINEAR)
        edge(src)
        cv.waitKey(0)
    #     cv.destroyAllWindows()
    #     del_files(framepath)

    # imgf.closed()

do()

