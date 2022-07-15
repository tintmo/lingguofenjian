from math import *
from doimg import *
import cv2 as cv
import numpy as np
from PIL import Image

imgfile='D:\\Pycharmfile\\lingguofenjian\\imgfile\\7.png'
imgf=open("..imgf",'w+')

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
    edge_output = cv.Canny(xgrad, ygrad, 100, 300)

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

    print('area:', area, 'circumference:', circumference, 'longth:', longth, 'width:', width, 'color:', color)


def do():
    for i in range(1, 8, 1):
        print(i, ':')
        #         path = file + str(i) + '.jpg'

        #         src1 = cv.imread(path)
        src1 = cv.imread(imgfile)
        img=Image.open(imgfile)
        # 图三（原图）
        size = src1.shape
        src = cv.resize(src1, ((int)(size[1] / 5), (int)(size[0] / 5)), cv.INTER_LINEAR)
        edge(src)
        cv.waitKey(0)
    #     cv.destroyAllWindows()
    imgf.closed()


do()

