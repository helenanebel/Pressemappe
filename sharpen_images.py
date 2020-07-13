import cv2 as cv
import os
import numpy as np
import statistics
# from scipy.signal import argrelextrema
from tesseract_pressemappe import get_text_files_from_jpgs
from img_methods import save_img, color_to_gray


def sharpen_images_and_get_text_files(jpg_list:list):
    picture_nr = 0
    for picture in jpg_list:
        print(picture)
        if picture_nr > 1000:
            break
        picture_nr += 1
        img = cv.imread('jpgs_cut/' + picture)
        gray = color_to_gray(img)
        if gray.shape[1]%2 == 0:
            print(gray.shape)
            new_column = np.zeros((1, img.shape[1]), np.uint8)
            print(new_column.shape)
            new_column.fill(255)
            gray = np.r_[gray, new_column]
        print(gray.shape)
        gauss_blurred = cv.GaussianBlur(gray, (5, 3), 0, 0)
        filtered = cv.bilateralFilter(gauss_blurred, 13, 75, 75)
        last = cv.adaptiveThreshold(filtered, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 7)
        # hier noch eroden oder closen?
        save_img(last, picture, 'jpgs_sharpened/') # geht nur mit .JPG am Ende.
        print(gray.shape)
        get_text_files_from_jpgs('jpgs_sharpened', [picture], 'pressemappe_text_files')


if __name__ == '__main__':
    sharpen_images_and_get_text_files(os.listdir('jpgs_cut'))