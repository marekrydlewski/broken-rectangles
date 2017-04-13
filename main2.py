import cv2
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt
import imutils
import os
import sys


def mydist(x, y):
    sum = []
    for i in range(100):
        sum.append(x[i] + y[100 - i - 1])
    return np.var(sum)


if __name__ == "__main__":
    folder = sys.argv[1]
    N = int(sys.argv[2])
    files = os.listdir(folder)
    files = [image_number for image_number in files if image_number.endswith('.png')]
    # print files
    feature = []
    for image_number in range(N):

        img = cv2.imread(folder + '/'+ str(image_number) + '.png', 0)
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        contour_nr = 0
        while contour_nr < len(contours) and len(contours[contour_nr]) < 10:
            contour_nr += 1

        cnt = contours[contour_nr]

        rect = cv2.minAreaRect(cnt)

        # rotacja
        angle = 270 - rect[2]
        img = imutils.rotate_bound(img, angle=angle)

        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        contour_nr = 0
        while contour_nr < len(contours) and len(contours[contour_nr]) < 20:
            contour_nr += 1

        cnt = contours[contour_nr]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        A = np.array(box)
        minA = np.min(A, axis=0)
        maxA = np.max(A, axis=0)

        shift = 5
        left_side = []
        good_night_right_side = []
        for i in range(minA[1], maxA[1]):
            left_side.append(img[i, minA[0] + shift])
            good_night_right_side.append(img[i, maxA[0] - shift])
        upper_side = []
        bottom_side = []

        for i in range(minA[0], maxA[0]):
            upper_side.append(img[minA[1] + shift, i])
            bottom_side.append(img[maxA[1] - shift, i])

        side_with_lowest_sum = np.argmin(
            [sum(upper_side) / len(upper_side), sum(bottom_side) / len(bottom_side), sum(left_side) / len(left_side),
             sum(good_night_right_side) / len(good_night_right_side)])

        if side_with_lowest_sum == 1:
            img = imutils.rotate_bound(img, angle=180)
            img = img[minA[1]:maxA[1], minA[0]:maxA[0]]
        elif side_with_lowest_sum == 2:
            img = imutils.rotate_bound(img, angle=90)
            img = img[minA[0]:maxA[0], minA[1]:maxA[1]]
        elif side_with_lowest_sum == 3:
            img = imutils.rotate_bound(img, angle=270)
            img = img[minA[0]:maxA[0], minA[1]:maxA[1]]
        else:
            img = img[minA[1]:maxA[1], minA[0]:maxA[0]]

        img = cv2.resize(img, (1000, 1000), 0, 0, interpolation=cv2.INTER_CUBIC)

        img = img[:, ::10]
        points = []
        for x in range(100):
            added = False
            for y in range(1000):
                if img[y, x] > 0:
                    points.append(y)
                    added = True
                    break
            if not added:
                points.append(1000)

        feature.append(points)
    nbrs = NearestNeighbors(n_neighbors=N, algorithm='ball_tree', metric=mydist).fit(feature)
    distances, indices = nbrs.kneighbors(feature)

    for row in indices:
        for element in row:
            print element,
        print
