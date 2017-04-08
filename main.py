import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils


def get_formatted_image(img):
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
    cnt = contours[0]
    rect = cv2.minAreaRect(cnt)
    # img = cv2.drawContours(img, [box], 0, (125, 0, 255), 2)
    # plt.imshow(img)
    # plt.show()

    # rotacja
    angle = 180 - rect[2] + 90  # trzeba dobrac odpowiedni kat
    img = imutils.rotate_bound(img, angle=angle)

    # edges = cv2.Canny(img, 50, 150, apertureSize=3)

    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    # for rho, theta in lines[0]:
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000 * (-b))
    #     y1 = int(y0 + 1000 * (a))
    #     x2 = int(x0 - 1000 * (-b))
    #     y2 = int(y0 - 1000 * (a))
    #
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # crop
    # ret, thresh = cv2.threshold(img, 127, 255, 0)
    # im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
    # cnt = contours[0]
    # rect = cv2.minAreaRect(cnt)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # img = img[box[1, 1]:box[3, 1], box[0, 0]:box[2, 0]]

    # black and white
    # (thresh, im_bw) = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)

    return img


if __name__ == "__main__":
   # for i in range(20):
    img = cv2.imread('data/set1/' + str(3) + '.png', 0)
    img_rotated = get_formatted_image(img)

    plt.imshow(img_rotated)
    plt.show()

    # cv2.imshow("obraz", img)
    # cv2.waitKey(0)

