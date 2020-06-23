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
    second_img = cv.imread('jpgs_sharpened/lala.JPG')
    second_img = color_to_gray(second_img)
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

    last = cv.medianBlur(cv.medianBlur(gray, 3), 3)
    fil = cv.bilateralFilter(last, 7, 75, 75)  # höhere kernel_size besser (13), sigma ist auf 75 oder 100 am Besten, sonst zu verschwommen
    last = cv.adaptiveThreshold(fil, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 7)  # Kernel unter 5 und über 15 nicht sinnvoll

    cons, hierarchy = cv.findContours(last, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
    # cv.List nimmt alle Konturen, cv.retr_external nur die äußeren
    # letzter Parameter gibt an, dass die Konturen nicht angenähert werden sollen.
    # bei cv.RETR_EXTERNAL kommt nur eine einzige Kontur zurück (der äußere Rand)
    mask = np.zeros(img.shape, np.uint8)
    mask.fill(255)

    contours_sorted = sorted(cons, key=cv.contourArea)[:-1]
    print(cons)
    lower_limit = statistics.median([cv.contourArea(con) for con in contours_sorted[:-1]]) # returns a list of n - 1 cut points separating the intervals.
    print(lower_limit)
    print([cv.contourArea(con) for con in contours_sorted])
    print(len(cons))
    cons = [con for con in contours_sorted if cv.contourArea(con) > lower_limit*0.25]
    for contour in cons:

        cv.drawContours(mask, [contour], 1, 0, -1, lineType=4)  # Draw contours on the colour image
        # Parameter definieren
        cv.drawContours(mask, [contour], 1, (255, 255, 255), 1, lineType=4)  # Draw contours on the colour image
        # Parameter: mask, Kontur als Array von Array, Index der zu zeichnenden Kontur
        # Farbe der Kontur, Füllungszustand (-1 = gefüllt, 1 = ungefüllt), linetype=8 & 15 schlecht,
        # linetype 4 normal gefüllt.
        # hier Lösung für unfilled Characters
        # https://stackoverflow.com/questions/48259724/cv2-drawcontours-unfill-circles-inside-characters-python-opencv
    # Konturenauswahl anpassen!
    # Konturen zweiter Ordnung nicht ausfüllen!!!!
    saveimg(mask, 'lap_edited_with_white_contours.jpg', 'jpgs_sharpened/')
    # Berechnung der Durchschnittsfarbe!!!!
    # avg_color_per_row = np.average(roi, axis=0)
    # avg_color = np.average(roi, axis=1)
    # print(avg_color)
    break

# eventuell kleine Konturen am Rand wegschneiden.

# for index in range(1, 19):
        # print(values[index]-values[index-1])
    # x = np.array(pixel_list)
    # for index in list(argrelextrema(x, np.greater)[0]):
        # print(pixel_list[index]) # das sind alle Pixel, die größer sind als ihre Nachbarn (lokale Maxima)

# Tresholding und Smoothing erledigt!