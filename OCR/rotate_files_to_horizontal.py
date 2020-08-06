import cv2 as cv
import statistics
from OCR.img_methods import color_to_gray, rotate_by_degree, save_img
from scipy import stats


def determine_rotation_degree_and_rotate(picture, do_save_img: bool = True,
                                         do_remove_borders: bool = True,
                                         img_obj=None, img_obj_given: bool = False):
    if img_obj_given:
        img = img_obj
    else:
        img = cv.imread('jpgs_sharpened/' + picture)
    degree_values = {}
    degree_dicts = {}
    for degree in range(-10, 10, 1):
        if degree not in degree_dicts:
            degree_dicts[str(degree)] = {}
        deg = degree/10
        if len(img.shape) > 2:
            gray = color_to_gray(img)
        else:
            gray = img
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
                if sum(regions_with_characters) <= len(region_list)*0.35:
                    region_nr = 0
                    if region_nr not in [0, 1, len(region_list)-1, len(region_list)-2, len(region_list) - 3]:
                        if sum(regions_with_characters[region_nr-2:region_nr+3]) > 2:
                            regions_with_characters[region_nr] = 1
                        region_nr += 1
                if sum(regions_with_characters) <= len(region_list) * 0.35:
                    if dimension == 0:
                        total_rows_to_delete.append(column)
                        to_delete_nr += 1
                    else:
                        total_columns_to_delete.append(column)
                        to_delete_nr += 1
        for i in total_rows_to_delete[:-3]:
            cleaned_rows_to_delete.append(i)
            if any(row for row in range(i + 1, i + 3) if row not in total_rows_to_delete):
                break
        total_rows_to_delete.reverse()
        for i in total_rows_to_delete:
            cleaned_rows_to_delete.append(i)
            if any(column for column in range(i - 1, i - 3, -1) if column not in total_rows_to_delete):
                break
        for i in total_columns_to_delete[:-3]:
            cleaned_columns_to_delete.append(i)
            if any(row for row in range(i + 1, i + 3) if row not in total_columns_to_delete):
                break
        total_columns_to_delete.reverse()
        for i in total_columns_to_delete:
            cleaned_columns_to_delete.append(i)
            if any(column for column in range(i - 1, i - 3, -1) if column not in total_columns_to_delete):
                break
        degree_values[str(degree)] = to_delete_nr
        degree_dicts[str(degree)]['columns'] = cleaned_columns_to_delete
        degree_dicts[str(degree)]['rows'] = cleaned_rows_to_delete
    sorted_values = sorted(degree_values.items(), key=lambda x: x[1], reverse=True)
    minimals = [int(val[0]) for val in sorted_values[:10]]
    m = stats.trim_mean(minimals, 0.2)
    if len(img.shape) > 2:
        gray = color_to_gray(img)
    else:
        gray = img
    gray = rotate_by_degree(gray, int(m)/10)
    if do_remove_borders:
        for key in degree_dicts[str(int(m))]:
            if key == 'columns':
                for column in degree_dicts[str(int(m))]['columns']:
                    for i in range(gray.shape[0]):
                        gray[i, column] = 255
            else:
                for row in degree_dicts[str(int(m))]['rows']:
                    for i in range(gray.shape[1]):
                        gray[row, i] = 255
    if do_save_img:
        save_img(gray, picture, 'jpgs_rotated/')  # geht nur mit .JPG am Ende.
    return gray


if __name__ == '__main__':
    determine_rotation_degree_and_rotate(
        ['0000xx_000012_000xx_00008_PIC_P000012000000000000000080001_0000_00000000HP_A.JPG'])

# evtl. weiterentwickeln, dass Überschriften abgeschnitten werden.
