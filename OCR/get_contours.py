import cv2 as cv
import os
import numpy as np
import statistics


# from scipy.signal import argrelextrema


def saveimg(img, picture, output_path):
    try:
        cv.imwrite(output_path + picture, img)
    except:
        print('writing file failed', img)


def color_to_gray(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


picture_nr = 0
for picture in os.listdir('jpgs_cut'):
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
    last = cv.GaussianBlur(gray, (5, 3), 0, 0)
    fil = cv.bilateralFilter(last, 5, 75, 75)  # höhere kernel_size besser (13), sigma ist auf 75 oder 100 am Besten, sonst zu verschwommen
    last = cv.adaptiveThreshold(fil, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 7)  # Kernel unter 5 und über 15 nicht sinnvoll

    cons, hierarchy = cv.findContours(last, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    print(len(hierarchy[0]))

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
    print(top_level_contour_indices)
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


    # Auslese der Konturen:
    # eventuell weniger sinnvoll als angenommen?
    mean_second_level = statistics.median([cv.contourArea(cons[con_nr]) for con_nr in second_level_contour_indices])
    mean_third_level = statistics.median([cv.contourArea(cons[con_nr]) for con_nr in third_level_contour_indices])
    for con_nr in top_level_contour_indices:
        cv.drawContours(mask, [cons[con_nr]], 0, (255, 255, 255), -1, lineType=8)
    for con_nr in second_level_contour_indices:
        if cv.contourArea(cons[con_nr]) > mean_third_level:
            cv.drawContours(mask, [cons[con_nr]], 0, 0, -1, lineType=8)  # Draw contours on the colour image
            # Parameter definieren
            cv.drawContours(mask, [cons[con_nr]], 0, (255, 255, 255), 1, lineType=8)
    for con_nr in third_level_contour_indices:
        #if cv.contourArea(cons[con_nr]) > mean_third_level*0.5:
            cv.drawContours(mask, [cons[con_nr]], 0, (255, 255, 255), -1, lineType=8)  # Draw contours on the colour image

    # new_gray = color_to_gray(mask)

    opening = mask
    # opening = cv.morphologyEx(mask, cv.MORPH_OPEN, (3, 3))
    erosion = cv.dilate(opening, (2, 2), iterations=1)
    erosion = cv.dilate(erosion, (2, 2), iterations=1)
    # a_del = np.delete(erosion, 1, 0)
    # print(a_del.shape)
    # a_del = np.delete(a_del, 1, 0)
    # print(a_del.shape)


    saveimg(erosion, 'aktuelle_konturen_erosion_2_2_closing_2_2_double.jpg', 'jpgs_sharpened/')
    # saveimg(negative, 'contours_white_border_linetype_8_hierarchy_respected_fil_5_neg.jpg', 'jpgs_sharpened/')
    # get_text_files_from_jpgs('jpgs_sharpened', ['contours_white_border_linetype_8_hierarchy_respected_fil_5.jpg'])

    # Berechnung der Durchschnittsfarbe!!!!
    # avg_color_per_row = np.average(roi, axis=0)
    # avg_color = np.average(roi, axis=1)
    # print(avg_color)
    break
