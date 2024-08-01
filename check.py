import cv2
import numpy as np


def get_pixel_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        colorsBGR = img[y, x]
        colorsHSV = cv2.cvtColor(
            np.uint8([[colorsBGR]]), cv2.COLOR_BGR2HSV)[0][0]
        print(f"Coordinates: ({x}, {y}) BGR: {colorsBGR}, HSV: {colorsHSV}")


# Загрузите ваше изображение
img = cv2.imread("t.png")

cv2.imshow('Image', img)
cv2.setMouseCallback('Image', get_pixel_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
