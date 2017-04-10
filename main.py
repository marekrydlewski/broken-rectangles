import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils

if __name__ == "__main__":
    for i in range(20):
        # if i != 1:
        #     continue

        img = cv2.imread('data/set1/' + str(i) + '.png', 0)
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[0]

        rect = cv2.minAreaRect(cnt)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # img = cv2.drawContours(img, [box], 0, (125, 0, 255), 2)

        # rotacja
        angle = 270 - rect[2]  # trzeba dobrac odpowiedni kat
        img = imutils.rotate_bound(img, angle=angle)

        # crop
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[0]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # img = cv2.drawContours(img, [box], 0, (125, 0, 255), 2)
        A = np.array(box)
        minA = np.min(A, axis=0)
        maxA = np.max(A, axis=0)

        left_side = []
        good_night_right_side = []
        for i in range(minA[1], maxA[1]):
            left_side.append(img[i, minA[0]])
            good_night_right_side.append(img[i, maxA[0]])
        upper_side = []
        bottom_side = []

        for i in range(minA[0], maxA[0]):
            upper_side.append(img[minA[1], i])
            bottom_side.append(img[maxA[1], i])

        side_with_lowest_sum = np.argmin(
            [sum(upper_side), sum(bottom_side), sum(left_side), sum(good_night_right_side)])

        if side_with_lowest_sum == 1:
            img = imutils.rotate_bound(img, angle=180)
        elif side_with_lowest_sum == 2:
            img = imutils.rotate_bound(img, angle=90)
        elif side_with_lowest_sum == 3:
            img = imutils.rotate_bound(img, angle=270)

        # img = img[minA[1]:maxA[1], minA[0]:maxA[0]]

        plt.imshow(img, cmap='gray')
        plt.show()
