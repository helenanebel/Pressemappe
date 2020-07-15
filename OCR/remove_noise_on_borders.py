import cv2 as cv
import statistics
# from scipy.signal import argrelextrema
from OCR.img_methods import color_to_gray, save_img, rotate_by_degree

# Bilder jeweils von 1 bis 10 Grad drehen und schauen, ob man dann mehr wegschneiden kann.

picture_nr = 0
for picture in ['pressemappe_results/median_blur_gaussian_kernel_3_bil_fil_17.JPG']:
    print(picture)
    if picture_nr > 1000:
        break
    picture_nr += 1
    img = cv.imread('jpgs_for_doku/median_blur_gaussian_kernel_3_bil_fil_17.JPG')
    # print(img)
    gray = color_to_gray(img)

    pixel_list = [int(pixel) for row in gray for pixel in row]
    print(statistics.mean(pixel_list))
    print(statistics.stdev(pixel_list))  # die Warnings werden selbständig gelöst und stellen kein Problem dar.
    print(statistics.median_grouped(pixel_list))
    print(statistics.quantiles(pixel_list, n=10))  # returns a list of n - 1 cut points separating the intervals.
    values = statistics.quantiles(pixel_list, n=20)
    gray = rotate_by_degree(gray, -0.7)
    characters_in_line = False
    column = 0
    number_of_regions = int(gray.shape[0]/200)*2
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
            if sum(regions_with_characters) <= len(region_list)*0.266:
                region_nr = 0
                for region in regions_with_characters:
                    if region_nr not in [0, 1, len(region_list)-1, len(region_list)-2]:
                        if sum(regions_with_characters[region_nr-2:region_nr+3]) > 2:
                            regions_with_characters[region_nr] = 1
                    region_nr += 1
            if sum(regions_with_characters) <= len(region_list) * 0.266:
                columns_to_delete.append(column)
        starting = []
        for col in range(1, len(columns_to_delete) - 1):
            if columns_to_delete[col] -1 != columns_to_delete[col -1]:
                break
            starting.append(columns_to_delete[col])
        starting = max(starting)
        ending = []
        for col in range(len(columns_to_delete) - 1, 1, -1):
            if columns_to_delete[col] - 1 != columns_to_delete[col -1]:
                break
            ending.append(columns_to_delete[col])
        ending = min(ending)
        if dimension == gray.shape[0]:
            print(starting, ending)
            gray[0:starting, 0:gray.shape[1]] = 0
            gray[ending:gray.shape[0], 0:gray.shape[1]] = 0
        else:
            print(starting, ending)
            gray[0:gray.shape[0], 0:starting] = 0
            gray[0:gray.shape[0], ending:gray.shape[1]] = 0
    # alle Spalten in dieser Liste mit 255 auffüllen!
    # shape[0] ist width, shape[1] ist heigth

    #
    # herausfinden, was der perfekte Winkel ist (berechnen aus der Anzahl der schwarzen Pixel
    # wenn man die Regionen auswertet. (besser sind wenige Regionen
    # mit einem hohen Gesamtwert als viele Regionen mit einem niedrigen Gesamtwert!
    # noch versuchen, die Kante zu finden!!!
    # closing vor dem Abschneiden ist sinnvoll!
    save_img(gray, 'lala.JPG', 'jpgs_sharpened/') # geht nur mit .JPG am Ende.

    break

