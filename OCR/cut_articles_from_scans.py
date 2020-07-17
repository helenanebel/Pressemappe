import cv2 as cv
import os
import numpy as np
from OCR.img_methods import color_to_gray, save_img
import math


def cut_articles(jpgs_list: list):
    picture_nr = 0
    for picture in os.listdir('jpgs'):
        if picture_nr > 1000:
            break
        picture_nr += 1
        img = cv.imread('jpgs/' + picture)
        img = cv.copyMakeBorder(img, 100, 100, 100, 100, cv.BORDER_CONSTANT, value=(255, 255, 255))
        gray = color_to_gray(img)

        ret, new = cv.threshold(gray, 85, 255, cv.THRESH_BINARY)
        blur = cv.GaussianBlur(new, (225,151), 0)
        ret2, th2 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        blur = cv.GaussianBlur(th2, (225,151), 0)
        ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        blur = cv.GaussianBlur(th3, (225,151), 0)
        ret4, th4 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        blur = cv.GaussianBlur(th4, (225,151), 0)
        ret5, th5 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        contours, hierarchy = cv.findContours(th5, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        inner_contours = [con for con in contours if cv.contourArea(con) not in [9931053, 9943198]]
        contours_sorted = sorted(inner_contours, key=cv.contourArea)
        max_log = max([int(math.log10(cv.contourArea(con))) for con in contours_sorted[-10:]])
        largest_area = contours_sorted[-1]
        contours_sorted = [con for con in contours_sorted if int(math.log10(cv.contourArea(con))) >= max_log - 1]
        mask = np.zeros(img.shape, np.uint8)
        mask.fill(255)
        cv.drawContours(mask, contours, -1, 0)
        dst = cv.bitwise_and(img, mask)
        max_x = 0
        max_y = 0
        min_x = img.shape[1]
        min_y = img.shape[0]

        for c in [largest_area]:
            x, y, w, h = cv.boundingRect(c)
            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x + w, max_x)
            max_y = max(y + h, max_y)
        roi = gray[min_y:max_y, min_x:max_x]
        avg_color_per_row = np.average(roi, axis=0)
        avg_color = np.average(roi, axis=1)
        save_img(roi, picture, 'jpgs_cut/')


if __name__ == '__main__':
    jpgs_list = os.listdir('jpgs')
    cut_articles(jpgs_list)