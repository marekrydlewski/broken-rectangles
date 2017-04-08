import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils


if __name__ == "__main__":
    for i in range(20):

        img = cv2.imread('data/set1/' + str(i) + '.png', 0)
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[0]

        rect = cv2.minAreaRect(cnt)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # img = cv2.drawContours(img, [box], 0, (125, 0, 255), 2)

        #rotacja
        angle = 180 - rect[2] + 90 # trzeba dobrac odpowiedni kat
        img = imutils.rotate_bound(img, angle=angle)

        # crop
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[0]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # img = img[box[1, 1]:box[3, 1], box[0, 0]:box[2, 0]]

        plt.imshow(img, cmap='gray')
        plt.show()

