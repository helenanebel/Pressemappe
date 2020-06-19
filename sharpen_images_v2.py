import cv2 as cv
import os
import numpy as np
import statistics
# from scipy.signal import argrelextrema
from tesseract_pressemappe import get_text_files_from_jpgs

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

    # ab hier Code schreiben & gleich DOKU!!!

    last = cv.GaussianBlur(gray, (3, 3), 0, 0)

    # last =  cv.medianBlur(cv.medianBlur(last, 3), 3) # entfernt Rauschen und behälgt Kanten bei.
    fil = cv.bilateralFilter(last, 13, 75, 75) # höhere kernel_size besser (13), sigma ist auf 75 oder 100 am Besten, sonst zu verschwommen
    last = cv.adaptiveThreshold(fil, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 7) # Kernel unter 5 und über 15 nicht sinnvoll
    # C sollte zwischen 7 und 9 liegen.
    # ret3, last = cv.threshold(fil,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU) # scheint nicht sinnvoll zu sein, obwohl viel Rauschen entfernt


    # Gaussian blur kernel höher als breit?


    saveimg(last, 'test_11.JPG', 'jpgs_sharpened/') # geht nur mit .JPG am Ende.

    # saveimg(last, picture, 'jpgs_sharpened/')
    get_text_files_from_jpgs(['test_11.jpg'], 'jpgs_sharpened/')
    break

# for index in range(1, 19):
        # print(values[index]-values[index-1])
    # x = np.array(pixel_list)
    # for index in list(argrelextrema(x, np.greater)[0]):
        # print(pixel_list[index]) # das sind alle Pixel, die größer sind als ihre Nachbarn (lokale Maxima)

'''
    pixel_list = [int(pixel) for row in gray for pixel in row]
    print(statistics.mean(pixel_list))
    print(statistics.stdev(pixel_list)) # die Warnings werden selbständig gelöst und stellen kein Problem dar.
    print(statistics.median_grouped(pixel_list))
    print(statistics.quantiles(pixel_list, n=10)) # returns a list of n - 1 cut points separating the intervals.
    values = statistics.quantiles(pixel_list, n=20)
    '''