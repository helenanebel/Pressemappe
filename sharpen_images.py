import cv2 as cv
import os
import numpy as np
import statistics
# from scipy.signal import argrelextrema
from tesseract_pressemappe import get_text_files_from_jpgs
from img_methods import save_img, color_to_gray


picture_nr = 0
for picture in os.listdir('jpgs_cut'):
    print(picture)
    if picture_nr > 1000:
        break
    picture_nr += 1
    img = cv.imread('jpgs_cut/' + picture)
    gray = color_to_gray(img)
    gauss_blurred = cv.GaussianBlur(gray, (5, 3), 0, 0)
    filtered = cv.bilateralFilter(gauss_blurred, 13, 75, 75)
    last = cv.adaptiveThreshold(filtered, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 7)

    save_img(last, 'aktuelles_muster_5_3.jpg', 'jpgs_sharpened/') # geht nur mit .JPG am Ende.

    get_text_files_from_jpgs('jpgs_sharpened', ['aktuelles_muster_5_3.jpg'], 'pressemappe_text_files')
    break
