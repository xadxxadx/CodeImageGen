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

def genDoubleSizeSingleCodeImage(width, height):
    #initialize image
    bW = width * 2
    bH = height * 2
    img = np.zeros((bW, bH, 3), np.uint8)
    text = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    img.fill(0)

    #put random text
    font = cv2.FONT_ITALIC
    font_scale = 1.0 + random.random()
    thickness = 3
    size = cv2.getTextSize(text, font, font_scale, thickness)
    text_width = size[0][0]
    text_height = size[0][1]
    cv2.putText(img, text, (int(width - text_width / 2), int(height + text_height / 2)), font,
                font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
    randomRange = int(text_width / 3)
    #warpping
    pts1 = np.float32([[width - text_width/2, height - text_height/2], [width + text_width/2, height - text_height/2], [width - text_width/2, height + text_height/2]])
    pts2 = np.float32([[width - text_width/2 + random.randint(-randomRange, randomRange), height - text_height/2 + random.randint(-randomRange, randomRange)], \
                       [width + text_width/2 + random.randint(-randomRange, randomRange), height - text_height/2 + random.randint(-randomRange, randomRange)], \
                       [width - text_width/2 + random.randint(-randomRange, randomRange), height + text_height/2 + random.randint(-randomRange, randomRange)]])

    M = cv2.getAffineTransform(pts1, pts2)
    res = cv2.warpAffine(img, M, (bW, bH))

    cv2.imshow('My Image', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return res

def genCodeImage(width, height, num, shift, snr):
    random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    img = np.zeros((400, 400, 3), np.uint8)
    img.fill(90)
    text = 'Hello, OpenCV!'
    cv2.putText(img, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 255), 1, cv2.LINE_AA)