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
    # print(img)
    gray = color_to_gray(img)
    pixel_list = [int(pixel) for row in gray for pixel in row]
    print(statistics.mean(pixel_list))
    print(statistics.stdev(pixel_list)) # die Warnings werden selbständig gelöst und stellen kein Problem dar.
    print(statistics.median_grouped(pixel_list))
    print(statistics.quantiles(pixel_list, n=10)) # returns a list of n - 1 cut points separating the intervals.
    values = statistics.quantiles(pixel_list, n=20)

    # ab hier Code schreiben & gleich DOKU!!!
    # kernel = np.ones((5, 5), np.float32) / 25
    # last = cv.filter2D(gray, -1, kernel)

    # last = cv.GaussianBlur(gray, (5, 5), 50, 50)

    last =  cv.medianBlur(cv.medianBlur(gray, 3), 3)
    fil = cv.bilateralFilter(gray, 9, 75, 75) # höhere kernel_size besser (13), sigma ist auf 75 oder 100 am Besten, sonst zu verschwommen
    last = cv.adaptiveThreshold(fil, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 7) # Kernel unter 5 und über 15 nicht sinnvoll
    # C sollte zwischen 7 und 9 liegen.
    # blur = cv.GaussianBlur(gray, (5, 5), 50, 50)
    # ret3, last = cv.threshold(fil,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU) # scheint nicht sinnvoll zu sein, obwohl viel Rauschen entfernt
    imagem = cv.bitwise_not(last)
    kernel = np.ones((3, 3), np.uint8)
    # last = cv.erode(imagem, kernel, iterations=2) # mit drei ZU großer Effekt, weniger wäre toll!
    # dilation = cv.dilate(imagem, kernel, iterations=1)
    # opening = cv.morphologyEx(imagem, cv.MORPH_OPEN, kernel)
    # closing = cv.morphologyEx(imagem, cv.MORPH_CLOSE, kernel)
    # alle drei zu groß für die angestrebten Zwecke.
    # yx = cv.bitwise_not(closing)
    last = cv.Laplacian(imagem, cv.CV_64F) # funktioniert sehr gut!
    ops = 'Laplacian'
    #
    # th2 = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,3,2)
    # ret3, th3 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # imagem = cv.bitwise_not(th2) # Invertierung
    # dilation = cv.dilate(th2, (9, 9), iterations=2) # vor dilation muss der Vordergrund in weiß sein!
    # closing = cv.morphologyEx(imagem, cv.MORPH_CLOSE, (3,3))

    # Unterschiede durch kernel_size etc. untersuchen!!!
    # andere noise-removal Vorgehensweisen verwenden!
    # herausfinden, wie die Farbe der Schrift-Pixel durchschnittlich aussieht!
    # "Schattenwurf" entfernen!
    # Gaussian blur kernel höher als breit?


    picture = picture.split('_PIC')[0].split('_', 1)[1] + '_' + ops + '.JPG'
    saveimg(last, picture, 'jpgs_sharpened/') # geht nur mit .JPG am Ende.
    # img = cv.imread('jpgs_sharpened/' + picture)

    # saveimg(last, picture, 'jpgs_sharpened/')
    break

# for index in range(1, 19):
        # print(values[index]-values[index-1])
    # x = np.array(pixel_list)
    # for index in list(argrelextrema(x, np.greater)[0]):
        # print(pixel_list[index]) # das sind alle Pixel, die größer sind als ihre Nachbarn (lokale Maxima)

# Tresholding und Smoothing erledigt!