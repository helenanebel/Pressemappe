import cv2 as cv
import os
import numpy as np
import statistics
# from scipy.signal import argrelextrema


# Bilder jeweils von 1 bis 10 Grad drehen und schauen, ob man dann mehr wegschneiden kann.
def saveimg(img, picture, output_path):
    try:
        cv.imwrite(output_path + picture, img)
    except:
        print('writing file failed', img)


def color_to_gray(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def rotate_by_degree(img, angle):
    return cv.warpAffine(img, cv.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), angle, 1.0), (img.shape[1], img.shape[0]), borderValue=255)


picture_nr = 0
for picture in ['pressemappe_results/test_5.JPG']:
    print(picture)
    if picture_nr > 1000:
        break
    picture_nr += 1
    img = cv.imread('pressemappe_results/test_5.JPG')
    # print(img)
    gray = color_to_gray(img)
    characters_in_line = False
    column = 0
    number_of_regions = int(gray.shape[0]/100)*2
    columns_to_delete = []
    for dimension in [gray.shape[0], gray.shape[1]]:
        for column in range(0, dimension):
            if dimension == gray.shape[1]:
                pixel_list = [row[column] for row in gray]
            else:
                pixel_list = gray[column]
            region_length = int(len(pixel_list)/number_of_regions)
            region_list = [pixel_list[i:i + region_length] for i in range(0, len(pixel_list), region_length)]
            regions_with_characters = [0 if statistics.mean(region)>=200 else 1 for region in region_list ]
            if sum(regions_with_characters) <= len(region_list)*0.2:
                region_nr = 0
                for region in regions_with_characters:
                    if region_nr not in [0, 1, len(region_list)-1, len(region_list)-2]:
                        if sum(regions_with_characters[region_nr-2:region_nr+3]) > 2:
                            regions_with_characters[region_nr] = 1
                    region_nr += 1
            if sum(regions_with_characters) <= len(region_list) * 0.2:
                columns_to_delete.append(column)

    # alle Spalten in dieser Liste mit 255 auffüllen!
    # shape[0] ist width, shape[1] ist heigth

    gray = rotate_by_degree(gray, -0.75)
    # herausfinden, was der perfekte Winkel ist (berechnen aus der Anzahl der schwarzen Pixel
    # wenn man die Regionen auswertet. (besser sind wenige Regionen
    # mit einem hohen Gesamtwert als viele Regionen mit einem niedrigen Gesamtwert!
    # noch versuchen, die Kante zu finden!!!
    # vorher noch blurren!
    saveimg(gray, 'lala.JPG', 'jpgs_sharpened/') # geht nur mit .JPG am Ende.

    break

