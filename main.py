import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
import os

if __name__ == "__main__":
    folder = 'data/set0/'
    files = os.listdir(folder)
    files = [image_file for image_file in files if image_file.endswith('.png')]
    # print files
    for image_file in files:
        # if image_file not in ['49.png']:
        #     continue
        print image_file

        img = cv2.imread(folder + image_file, 0)
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        contour_nr = 0
        while contour_nr < len(contours) and len(contours[contour_nr]) < 10:
            contour_nr += 1

        cnt = contours[contour_nr]
        # cnt = contours[0]

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
        contour_nr = 0
        while contour_nr < len(contours) and len(contours[contour_nr]) < 20:
            contour_nr += 1

        cnt = contours[contour_nr]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # print len(contours)
        # print len(contours[contour_nr])
        # print contours[contour_nr]
        # img = cv2.drawContours(img, [box], 0, (125, 0, 255), 2)
        # cv2.circle(img, (164, 27), 5, (100, 100, 0), -1)
        A = np.array(box)
        minA = np.min(A, axis=0)
        maxA = np.max(A, axis=0)

        shift = 5
        left_side = []
        good_night_right_side = []
        for i in range(minA[1], maxA[1]):
            left_side.append(img[i, minA[0]+shift])
            good_night_right_side.append(img[i, maxA[0]-shift])
        upper_side = []
        bottom_side = []

        for i in range(minA[0], maxA[0]):
            upper_side.append(img[minA[1]+shift, i])
            bottom_side.append(img[maxA[1]-shift, i])

        # print upper_side
        # print bottom_side
        # print good_night_right_side
        # print left_side

        side_with_lowest_sum = np.argmin(
            [sum(upper_side)/len(upper_side), sum(bottom_side)/len(bottom_side), sum(left_side)/len(left_side), sum(good_night_right_side)/len(good_night_right_side)])

        # print side_with_lowest_sum
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

        plt.imshow(img, cmap='gray')
        # plt.show()
        plt.savefig('result' + folder + image_file)
