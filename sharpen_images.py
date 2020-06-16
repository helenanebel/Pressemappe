import cv2 as cv
import os
import numpy as np
import statistics
from scipy.signal import argrelextrema


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
    # print(img)
    gray = color_to_gray(img)
    pixel_list = [int(pixel) for row in gray for pixel in row]
    print(statistics.mean(pixel_list))
    print(statistics.stdev(pixel_list)) # die Warnings werden selbständig gelöst und stellen kein Problem dar.
    print(statistics.median_grouped(pixel_list))
    print(statistics.quantiles(pixel_list, n=10)) # returns a list of n - 1 cut points separating the intervals.
    values = statistics.quantiles(pixel_list, n=20)
    # for index in range(1, 19):
        # print(values[index]-values[index-1])
    # x = np.array(pixel_list)
    # for index in list(argrelextrema(x, np.greater)[0]):
        # print(pixel_list[index]) # das sind alle Pixel, die größer sind als ihre Nachbarn (lokale Maxima)

    # blur = cv.GaussianBlur(gray, (5, 5), 0) # kernel sizes sind ungerade!
    # th2 = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,3,2)
    ret3, th3 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # Unterschiede durch kernel_size etc. untersuchen!!!
    # andere nois-removal Vorgehensweisen verwenden!
    # herausfinden, wie die Farbe der Schrift-Pixel durchschnittlich aussieht!
    # "Schattenwurf" entfernen!
    saveimg(th3, picture, 'jpgs_sharpened/')
    break

# max - und min- und average-values ermitteln und diese verwenden, um das weitere Vorgehen zu bestimmen.
