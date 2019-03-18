import cv2
import string
import random
import numpy as np


def genNoiceBG(width, height, snr):
    img = np.zeros((height, width, 3), np.uint8)
    row, col, ch = img.shape
    for i in range(0, int(width * height * snr)):
        cv2.circle(img, (random.randint(0, width-1), random.randint(0, height-1)), random.randint(1,2), np.ones(3)*random.randint(200, 255), cv2.FILLED)
        #img[random.randint(0, height-1), random.randint(0, width-1)] = np.ones(3) * random.randint(150, 255)

    for i in range(0, int(width * height * snr / 5)):
        img = cv2.ellipse(img, \
                          (random.randint(-width, width*2), random.randint(-height, height*2)), \
                          (random.randint(width, width*5), random.randint(height, height * 5)), \
                          random.randint(0,30), \
                          0, \
                          360,\
                          np.ones(3) * random.randint(200, 255), \
                          random.randint(1,2))

    #cv2.imshow('My Image', img)
    #cv2.imwrite('test.bmp', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return img


def genDoubleSizeSingleCodeImage(width, height, fontSize):
    #initialize image
    bW = width * 2
    bH = height * 2
    img = np.zeros((bW, bH, 3), np.uint8)
    text = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    img.fill(0)

    #put random text
    font = cv2.FONT_ITALIC
    font_scale = fontSize + random.random() / 3
    thickness = 3
    size = cv2.getTextSize(text, font, font_scale, thickness)
    text_width = size[0][0]
    text_height = size[0][1]
    color_plus = random.randint(0, 50)
    cv2.putText(img, text, (int(width - text_width / 2), int(height + text_height / 2)), font,
                font_scale, (205 + color_plus, 205 + color_plus, 205 + color_plus), thickness, cv2.LINE_AA)
    randomRange = int(text_width / 3)
    #warpping
    pts1 = np.float32([[width - text_width/2, height - text_height/2], [width + text_width/2, height - text_height/2], [width - text_width/2, height + text_height/2]])
    pts2 = np.float32([[width - text_width/2 + random.randint(-randomRange, randomRange), height - text_height/2 + random.randint(-randomRange, randomRange)], \
                       [width + text_width/2 + random.randint(-randomRange, randomRange), height - text_height/2 + random.randint(-randomRange, randomRange)], \
                       [width - text_width/2 + random.randint(-randomRange, randomRange), height + text_height/2 + random.randint(-randomRange, randomRange)]])

    M = cv2.getAffineTransform(pts1, pts2)
    res = cv2.warpAffine(img, M, (bW, bH))

    #cv2.imshow('My Image', res)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return text, res


def getBoundaryBox(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    r, binaryImg = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    rect = cv2.boundingRect(binaryImg)
    #cv2.rectangle(img, rect, (255,0,0), 1)
    #cv2.imshow('My Image', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return rect

def bitwiseTextOnBK(bk, textImg, rect)  :
    blackBK = np.zeros(bk.shape, np.uint8)
    blackBK[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]] = textImg[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

def genCodeImage(width, height, num, shift, snr):
    textes = []
    rois = []
    stepX = width / (num+1)
    stepY = height / 2
    bk = genNoiceBG(width, height, snr)
    for i in range(0, num):
        text, img = genDoubleSizeSingleCodeImage(height, height, 1.0)
        rect = getBoundaryBox(img)
        startX = int(stepX *(i+1) - rect[2]/2)
        startY  = int(stepY - rect[3]/2)
        bitwise = cv2.bitwise_or(bk[startY:startY+rect[3]-1, startX:startX+rect[2]-1] , img[rect[1]:rect[1]+rect[3] -1, rect[0]:rect[0]+rect[2] - 1])
        bk[startY:startY+rect[3]-1, startX:startX+rect[2]-1] = bitwise
        textes.append(text)
        rois.append((startX, startY, rect[2], rect[3]))
    return textes, rois, bk