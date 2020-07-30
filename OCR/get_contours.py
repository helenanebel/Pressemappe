import cv2 as cv
import os
import numpy as np
import statistics
from OCR.img_methods import color_to_gray, save_img


def get_contours(picture, do_save_img: bool = True,
                 source_dir_path: str = 'OCR/jpgs_cut', target_dir_path: str = 'OCR/jpgs_contours'):
    img = cv.imread(source_dir_path + '/' + picture)
    gray = color_to_gray(img)
    # sollte man das auch für das zweite Bild machen?
    if gray.shape[1]%2 == 0:
        new_column = np.zeros((1, img.shape[1]), np.uint8)
        new_column.fill(255)
        gray = np.r_[gray, new_column]
        # verhindert, dass sich die Reihen nach unten verschieben; gibt beim merge Probleme.
    last = cv.GaussianBlur(gray, (5, 3), 0, 0)
    fil = cv.bilateralFilter(last, 5, 75, 75)
    last = cv.adaptiveThreshold(fil, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 7)  # Kernel unter 5 und über 15 nicht sinnvoll

    cons, hierarchy = cv.findContours(last, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    mask = np.zeros(gray.shape, np.uint8)
    mask.fill(255)
    top_level_contour_indices = []
    second_level_contour_indices = []
    third_level_contour_indices = []
    con_nr = 0
    for con_hierarchy in hierarchy[0]:
        if con_hierarchy[3] == -1:
            top_level_contour_indices.append(con_nr)
        con_nr += 1
    con_nr = 0
    for con_hierarchy in hierarchy[0]:
        if con_hierarchy[3] in top_level_contour_indices:
            second_level_contour_indices.append(con_nr)
        con_nr += 1
    con_nr = 0
    for con_hierarchy in hierarchy[0]:
        if con_hierarchy[3] in second_level_contour_indices:
            third_level_contour_indices.append(con_nr)
            cv.drawContours(mask, [cons[con_nr]], 0, (255, 255, 255), -1, lineType=8)  # Draw contours on the colour image
        con_nr += 1

    mean_third_level = statistics.median([cv.contourArea(cons[con_nr]) for con_nr in third_level_contour_indices])
    for con_nr in second_level_contour_indices:
        if cv.contourArea(cons[con_nr]) > mean_third_level:
            cv.drawContours(mask, [cons[con_nr]], 0, 0, -1, lineType=8)
            cv.drawContours(mask, [cons[con_nr]], 0, (255, 255, 255), 1, lineType=8)
    for con_nr in third_level_contour_indices:
        cv.drawContours(mask, [cons[con_nr]], 0, (255, 255, 255), -1, lineType=8)

    opening = cv.dilate(mask, (3, 3), iterations=2)
    erosion = cv.dilate(opening, (3, 3), iterations=2)
    if do_save_img:
        save_img(erosion, target_dir_path + '/' + picture, 'OCR/jpgs_contours/')
    return erosion


if __name__ == '__main__':
    jpgs_list = os.listdir('OCR/jpgs_cut')
    get_contours(jpgs_list)
