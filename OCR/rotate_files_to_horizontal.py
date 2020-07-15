import cv2 as cv
import statistics
from OCR.img_methods import color_to_gray, rotate_by_degree
# from scipy.signal import argrelextrema


def determine_rotation_degree_and_rotate(img_list: list):
    picture_nr = 0
    for picture in img_list:
        print(picture)
        if picture_nr > 1000:
            break
        picture_nr += 1
        img = cv.imread('jpgs_sharpened/' + picture)
        gray = color_to_gray(img)
        degree_values = {}
        degree_dicts = {}
        for degree in range(-10, 10, 1):
            if degree not in degree_dicts:
                degree_dicts[str(degree)] = {}
            deg = degree/10
            print(deg)
            gray = rotate_by_degree(gray, deg)
            total_rows_to_delete = []
            total_columns_to_delete = []
            cleaned_rows_to_delete = []
            cleaned_columns_to_delete = []

            to_delete_nr = 0
            for dimension in [0, 1]:
                new_shape = gray.shape[dimension]
                number_of_regions = int(new_shape / 50) * 2
                region_length = int(new_shape / number_of_regions)
                for column in range(0, new_shape):
                    if dimension == 1:
                        pixel_list = [row[column] for row in gray]
                    else:
                        pixel_list = gray[column]
                    region_list = [pixel_list[i:i + region_length] for i in range(0, len(pixel_list), region_length)]
                    regions_with_characters = [0 if statistics.mean(region) >= 200 else 1 for region in region_list]
                    if sum(regions_with_characters) <= len(region_list)*0.2:
                        region_nr = 0
                        if region_nr not in [0, 1, len(region_list)-1, len(region_list)-2, len(region_list) - 3]:
                            if sum(regions_with_characters[region_nr-2:region_nr+3]) > 2:
                                regions_with_characters[region_nr] = 1
                            region_nr += 1
                    if sum(regions_with_characters) <= len(region_list) * 0.2:
                        if dimension == 0:
                            total_rows_to_delete.append(column)
                            to_delete_nr += 1
                        else:
                            total_columns_to_delete.append(column)
                            to_delete_nr += 1
            for i in total_rows_to_delete[:-3]:
                cleaned_rows_to_delete.append(i)
                if any(row for row in range(i + 1, i + 3) if row not in total_rows_to_delete):
                    print(i)
                    print(True)
                    break
            # Diese Funktion hier funktioniert.
            # Das hier nicht:
            print(len(total_rows_to_delete), total_rows_to_delete)
            '''
            total_rows_to_delete.reverse()
            print(total_rows_to_delete)
            for i in total_rows_to_delete:
                cleaned_rows_to_delete.append(i)
                if any(column for column in range(i - 1, i - 3) if column not in total_rows_to_delete):
                    break
            print(to_delete_nr)
            print(cleaned_rows_to_delete)
            
                
            print(deg)
            
            # die Daten werden nicht mehr bereinigt!!!
            # funktioniert nicht mehr!!!!!
            '''
        '''
        sorted_values = sorted(degree_values.items(), key=lambda x: x[1], reverse=True)
        print(sorted_values)
        minimals = [int(val[0]) for val in sorted_values[:10]]
        m = stats.trim_mean(minimals, 0.2)
        gray = rotate_by_degree(gray, m)
        print(degree_dicts)
        print(degree_dicts[str(int(m))])
        for key in degree_dicts[str(int(m))]:
            if key == 'columns_to_delete':
                for column in degree_dicts[str(int(m))]['columns_to_delete]:
                    for i in range(gray.shape[1]):
                    gray[column, i] = 255
            else:
            for row in degree_dicts[str(int(m))]['columns_to_delete]:
                for i in range(gray.shape[0]):
                    gray[i, column] = 255
        save_img(gray, picture, 'jpgs_rotated/') # geht nur mit .JPG am Ende.
        '''


if __name__ == '__main__':
    determine_rotation_degree_and_rotate(['aktuelles_muster_5_3.jpg'])

