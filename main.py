import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import imutils


def mydist(x, y):
    sum = 0
    for i in range(100):
        sum += abs(100 - x[i] - y[i] )
    return sum

if __name__ == "__main__":
    feature = []
    for i in range(20):
        if i in [0, 1, 3, 5, 7, 9, 11, 14, 15, 16, 17, 18, 19]:
            continue
        print i
        img = cv2.imread('data/set1/' + str(i) + '.png', 0)
        # gray = np.float32(gray)
        # dst = cv2.cornerHarris(gray, 2, 3, 0.04)
        # # result is dilated for marking the corners, not important
        # dst = cv2.dilate(dst, None)
        # # Threshold for an optimal value, it may vary depending on the image.
        # img[dst > 0.01 * dst.max()] = [0, 0, 255]
        # cv2.imshow('dst', img)
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[0]
        M = cv2.moments(cnt)

        rect = cv2.minAreaRect(cnt)
        angle = 180 - rect[2] + 90
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # img = cv2.drawContours(img, [box], 0, (125, 0, 255), 2)
        img = imutils.rotate_bound(img, angle=angle)
        crop_img = img[200:400, 100:300]
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[0]
        M = cv2.moments(cnt)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # img = cv2.drawContours(img, [box], 0, (125, 0, 255), 2)
        img = crop_img = img[box[1, 1]:box[3, 1], box[0, 0]:box[2, 0]]
        img = cv2.resize(img, (1000, 1000), 0, 0, interpolation=cv2.INTER_CUBIC)

        img = img[:, ::10]
        points = []
        for x in range(100):
            for y in range(1000):
                if img[y, x] > 0:
                    points.append(y)
                    break

        # print len(points)
        # print points
        # plt.imshow(img, cmap='gray')
        # plt.show()
        feature.append(points)
    nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree', metric=mydist ).fit(feature)
    distances, indices = nbrs.kneighbors(feature)
    print indices
    # if cv2.waitKey(0) & 0xff == 27:
    #     cv2.destroyAllWindows()
    # print("Begin something great")
