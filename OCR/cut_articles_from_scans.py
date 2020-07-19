import cv2 as cv
import os
import numpy as np
from OCR.img_methods import color_to_gray, save_img
import math

jpgs_for_evaluation = [ "0000xx_000010_000xx_00002_PIC_P000010000000000000000020000_0000_00000000HP_A.JPG",
                        "0000xx_000010_000xx_00001_PIC_P000010000000000000000010000_0000_00000000HP_A.JPG",
                        "0000xx_000012_000xx_00001_PIC_P000012000000191479000010000_0000_00000000HP_A.JPG",
                        "0000xx_000034_001xx_00168_PIC_P000034000000000000001680000_0000_00000P34HP_A.JPG",
                        "0077xx_007779_000xx_00001_PIC_P007779000000191478000010000_0000_00000000HP_A.JPG",
                        "0112xx_011242_000xx_00011_PIC_P011242000000191477000110000_0000_00000000HP_A.JPG",
                        "0074xx_007478_000xx_00004_PIC_P007478000000000000000040000_0000_00000000HP_A.JPG",
                        "0425xx_042518_000xx_00052_PIC_P042518000000000000000520000_0000_00000000KP_A.JPG",
                        "0109xx_010995_000xx_00004_PIC_P010995000000000000000040000_0000_00000M48HP_A.JPG",
                        "0423xx_042397_000xx_00002_PIC_P042397000000191477000020000_0000_00000000HP_A.JPG",
                        "0000xx_000010_000xx_00002_PIC_P000010000000000000000020001_0000_00000000HP_A.JPG",
                        "0036xx_003644_000xx_00004_PIC_P003644000000000000000040000_0000_00000000HP_A.JPG",
                        "0000xx_000010_000xx_00005_PIC_P000010000000000000000050000_0000_00000000HP_A.JPG",
                        "0000xx_000012_000xx_00005_PIC_P000012000000191477000050001_0000_00000000HP_A.JPG",
                        "0036xx_003644_000xx_00003_PIC_P003644000000000000000030000_0000_00000000HP_A.JPG",
                        "0044xx_004455_000xx_00001_PIC_P004455000000191478000010000_0000_00000000HP_A.JPG",
                        "0000xx_000022_000xx_00040_PIC_P000022000000000000000400000_0000_00000X49HP_A.JPG",
                        "0000xx_000022_000xx_00015_PIC_P000022000000000000000150000_0000_00000000HP_A.JPG",
                        "0032xx_003281_000xx_00008_PIC_P003281000000000000000080000_0000_00000000HP_A.JPG",
                        "0032xx_003281_000xx_00005_PIC_P003281000000000000000050000_0000_00000000HP_A.JPG",
                        "0000xx_000010_000xx_00006_PIC_P000010000000191477000060001_0000_00000000HP_A.JPG",
                        "0000xx_000012_000xx_00002_PIC_P000012000000191479000020000_0000_00000000HP_A.JPG",
                        "0000xx_000034_001xx_00162_PIC_P000034000000000000001620001_0000_00000P34HP_A.JPG",
                        "0099xx_009942_000xx_00003_PIC_P009942000000000000000030000_0000_00000000HP_A.JPG",
                        "0032xx_003274_000xx_00052_PIC_P003274000000000000000520000_0000_00000000HP_A.JPG",
                        "0090xx_009021_000xx_00004_PIC_P009021000000000000000040000_0000_00000X48HP_A.JPG",
                        "0001xx_000135_000xx_00067_PIC_P000135000000000000000670000_0000_00000X48HP_A.JPG",
                        "0046xx_004600_000xx_00003_PIC_P004600000000191477000030000_0000_00000000HP_A.JPG",
                        "0110xx_011060_000xx_00010_PIC_P011060000000191477000100000_0000_00000000HP_A.JPG",
                        "0110xx_011060_000xx_00040_PIC_P011060000000000000000400000_0000_00000000HP_A.JPG"]


def cut_articles(jpgs_list: list):
    picture_nr = 0
    for picture in jpgs_list:
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
    jpgs_list = jpgs_for_evaluation
    cut_articles(jpgs_list)