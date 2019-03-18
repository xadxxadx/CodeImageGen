import codeImageGen
import cv2
import os


def main_test():
    text, roi, img = codeImageGen.genCodeImage(200, 60, 5, 1, 0.003)
    cv2.imshow('My Image', img)
    cv2.imwrite('test.bmp', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(text)
    print(roi)

def main():
    dirName = 'images'
    if not os.path.exists(dirName):
        os.mkdir(dirName)

    labelName = 'labels'
    if not os.path.exists(labelName):
        os.mkdir(labelName)

    num = 10
    numberCount = 5;
    for i in range(0, num):
        text, roi, img = codeImageGen.genCodeImage(200, 60, numberCount, 1, 0.003)
        fileName = '{:0>8d}.jpg'.format(i)
        cv2.imwrite('{}/{}'.format(dirName, fileName), img)

        text_file = open("{}/{:0>8d}.xml".format(labelName, i), "w")
        text_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
        text_file.write('<annotation>\n')
        text_file.write('\t<folder> {} </folder >\n'.format(dirName))
        text_file.write('\t<filename> {} </filename>\n'.format(fileName))
        text_file.write('\t<size>\n')
        text_file.write('\t\t<width> {} </width>\n'.format(img.shape[1]))
        text_file.write('\t\t<height> {} </height>\n'.format(img.shape[0]))
        text_file.write('\t\t<depth> {} </depth>\n'.format(img.shape[2]))
        text_file.write('\t</size>\n')

        for j in range(0, numberCount):
            text_file.write('\t<object>\n')
            text_file.write('\t\t<name>{}</name>\n'.format(text[j]))
            text_file.write('\t\t<bndbox>\n')
            text_file.write('\t\t\t<xmin>{}</xmin>\n'.format(roi[j][0]))
            text_file.write('\t\t\t<xmax>{}</xmax>\n'.format(roi[j][0] + roi[j][2] - 1))
            text_file.write('\t\t\t<ymin>{}</ymin>\n'.format(roi[j][1]))
            text_file.write('\t\t\t<ymax>{}</ymax>\n'.format(roi[j][1] + roi[j][3] - 1))
            text_file.write('\t\t</bndbox>\n')
            text_file.write('\t\t<truncated>0</truncated>\n')
            text_file.write('\t\t<difficult>0</difficult>\n')
            text_file.write('\t</object>\n')

        text_file.write('\t<segmented>0</segmented>\n')
        text_file.write('</annotation>\n')
        text_file.close()


if __name__ == "__main__":
    main()
