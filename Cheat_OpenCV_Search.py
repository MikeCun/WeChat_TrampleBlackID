# -*- coding: utf-8 -*
import numpy as np
import os, cv2, wda, imutils

# Screen Size for the Phone
screen_w, screen_h = 1242, 2208
black_w, black_h = 310, 540

# IOS WDA Client
SeverURL = "http://localhost:8100"
client = wda.Client(SeverURL)
s = client.session()

while True:
    # IOS SreenShot
    client.screenshot('block.png')
    if not os.path.exists('block.png'):
        raise NameError('Cannot obtain screenshot from the phone!')

    img = cv2.imread('block.png', 0)
    # 二值化图像，将图像黑白分明
    ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # 自适应二值化图像，将图像黑白更加分明
    thresh = cv2.adaptiveThreshold(thresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 53, 2)
    # 模糊化图像，将边框去除
    ChQImg = cv2.blur(thresh, (23, 23))
    # 二值化图像，并取黑色部分
    ChQImg = cv2.threshold(ChQImg, 100, 225, cv2.THRESH_BINARY)[1]
    # 找图像边框
    cnts = cv2.findContours(ChQImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 返回轮廓列表
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        M = cv2.moments(c)
        if M["m00"] == 0:
            cX, cY = 0, 0
        else:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        if cY / black_h:
            cY = screen_h - black_h + black_h / 2
        if cY > (screen_h - black_h):
            # 模拟点击
            s.tap(cX / 3, cY / 3)
    break
