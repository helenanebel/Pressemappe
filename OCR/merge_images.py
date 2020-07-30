import cv2 as cv
from OCR.img_methods import save_img
from OCR.get_contours import get_contours
import numpy as np
import os


def merge_pictures(picture: str, do_save_img: bool = True):
    img_2 = get_contours(picture, source_dir_path='OCR/jpgs_cut')
    img_1 = cv.imread('OCR/jpgs_sharpened/' + picture)
    gray_1 = cv.cvtColor(img_1, cv.COLOR_BGR2GRAY)
    if gray_1.shape[1] < img_2.shape[1]:
        new_column = np.zeros((1, gray_1.shape[1]), np.uint8)
        new_column.fill(255)
        gray_1 = np.r_[gray_1, new_column]
        # Falls das Konturenbild angepasst wurde, müssen die Shapes wieder angepasst werden.
    dst = cv.bitwise_and(gray_1, img_2)
    if do_save_img:
        save_img(dst, picture, 'OCR/jpgs_added/')
    return dst


if __name__ == '__main__':
    merge_pictures('0000xx_000010_000xx_00001_PIC_P000010000000000000000010000_0000_00000000HP_A.JPG')