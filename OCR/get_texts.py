from OCR.sharpen_images import sharpen_images_and_get_text_files
from OCR.merge_images import merge_pictures
from OCR.tesseract_pressemappe import get_text_files_from_jpgs
import os
from OCR.cut_articles_from_scans import cut_articles
from OCR.rotate_files_to_horizontal import determine_rotation_degree_and_rotate
from OCR.get_jpgs import get_jpgs

jpgs_for_evaluation = [ "0000xx_000010_000xx_00002_PIC_P000010000000000000000020000_0000_00000000HP_A.JPG",
                        "0000xx_000010_000xx_00002_PIC_P000010000000000000000020001_0000_00000000HP_A.JPG",
                        "0000xx_000010_000xx_00001_PIC_P000010000000000000000010000_0000_00000000HP_A.JPG",
                        "0000xx_000012_000xx_00001_PIC_P000012000000191479000010000_0000_00000000HP_A.JPG",
                        "0000xx_000034_001xx_00168_PIC_P000034000000000000001680000_0000_00000P34HP_A.JPG",
                        "0077xx_007779_000xx_00001_PIC_P007779000000191478000010000_0000_00000000HP_A.JPG",
                        "0112xx_011242_000xx_00011_PIC_P011242000000191477000110000_0000_00000000HP_A.JPG",
                        "0074xx_007478_000xx_00004_PIC_P007478000000000000000040000_0000_00000000HP_A.JPG",
                        "0425xx_042518_000xx_00052_PIC_P042518000000000000000520000_0000_00000000KP_A.JPG",
                        "0425xx_042518_000xx_00052_PIC_P042518000000000000000520001_0000_00000000KP_A.JPG",
                        "0109xx_010995_000xx_00004_PIC_P010995000000000000000040000_0000_00000M48HP_A.JPG",
                        "0423xx_042397_000xx_00002_PIC_P042397000000191477000020000_0000_00000000HP_A.JPG",
                        "0423xx_042397_000xx_00002_PIC_P042397000000191477000020001_0000_00000000HP_A.JPG",
                        "0423xx_042397_000xx_00002_PIC_P042397000000191477000020002_0000_00000000HP_A.JPG",
                        "0423xx_042397_000xx_00002_PIC_P042397000000191477000020003_0000_00000000HP_A.JPG",
                        "0036xx_003644_000xx_00004_PIC_P003644000000000000000040000_0000_00000000HP_A.JPG",
                        "0000xx_000010_000xx_00005_PIC_P000010000000000000000050000_0000_00000000HP_A.JPG",
                        "0000xx_000012_000xx_00005_PIC_P000012000000191477000050000_0000_00000000HP_A.JPG",
                        "0000xx_000012_000xx_00005_PIC_P000012000000191477000050001_0000_00000000HP_A.JPG",
                        "0036xx_003644_000xx_00003_PIC_P003644000000000000000030000_0000_00000000HP_A.JPG",
                        "0044xx_004455_000xx_00001_PIC_P004455000000191478000010000_0000_00000000HP_A.JPG",
                        "0000xx_000022_000xx_00040_PIC_P000022000000000000000400000_0000_00000X49HP_A.JPG",
                        "0000xx_000022_000xx_00015_PIC_P000022000000000000000150000_0000_00000000HP_A.JPG",
                        "0032xx_003281_000xx_00008_PIC_P003281000000000000000080000_0000_00000000HP_A.JPG",
                        "0032xx_003281_000xx_00005_PIC_P003281000000000000000050000_0000_00000000HP_A.JPG",
                        "0000xx_000010_000xx_00006_PIC_P000010000000191477000060000_0000_00000000HP_A.JPG",
                        "0000xx_000010_000xx_00006_PIC_P000010000000191477000060001_0000_00000000HP_A.JPG",
                        "0000xx_000012_000xx_00002_PIC_P000012000000191479000020000_0000_00000000HP_A.JPG",
                        "0000xx_000034_001xx_00162_PIC_P000034000000000000001620000_0000_00000P34HP_A.JPG",
                        "0099xx_009942_000xx_00003_PIC_P009942000000000000000030000_0000_00000000HP_A.JPG",
                        "0099xx_009942_000xx_00003_PIC_P009942000000000000000030001_0000_00000000HP_A.JPG",
                        "0032xx_003274_000xx_00052_PIC_P003274000000000000000520000_0000_00000000HP_A.JPG",
                        "0090xx_009021_000xx_00004_PIC_P009021000000000000000040000_0000_00000X48HP_A.JPG",
                        "0001xx_000135_000xx_00067_PIC_P000135000000000000000670000_0000_00000X48HP_A.JPG",
                        "0046xx_004600_000xx_00003_PIC_P004600000000191477000030000_0000_00000000HP_A.JPG",
                        "0110xx_011060_000xx_00010_PIC_P011060000000191477000100000_0000_00000000HP_A.JPG",
                        "0110xx_011060_000xx_00040_PIC_P011060000000000000000400000_0000_00000000HP_A.JPG"]


def get_texts(jpgs_list: list, source_dir_path: str = 'jpgs_cut', target_dir_path: str = 'pressemappe_text_files'):
    last = ''
    jpgs_list.sort()
    for picture in jpgs_list:
        name = picture.replace('.JPG', '')
        print('start', picture)
        if picture not in os.listdir(source_dir_path):
            cut_articles([picture])
        sharpened = sharpen_images_and_get_text_files([picture], source_directory=source_dir_path,
                                          do_save_img=True)[0]
        # sharpened_rotated = determine_rotation_degree_and_rotate(picture, do_save_img=False, do_remove_borders=False,
                                                         # img_obj_given=True, img_obj=sharpened)
        merged = merge_pictures(picture, do_save_img=False)
        # merged_rotated = determine_rotation_degree_and_rotate(picture, do_save_img=False, do_remove_borders=False,
                                                         # img_obj_given=True, img_obj=merged)
        text_sharpened = get_text_files_from_jpgs([picture], img_obj=sharpened, save_file=False, img_obj_given=True)
        print('sharpened')
        text_merged = get_text_files_from_jpgs([picture], img_obj=merged, save_file=False, img_obj_given=True)
        print('merged')
        txt_name = picture.replace('.JPG', '')
        text = text_sharpened + '\n' + text_merged
        text = text.encode('utf-8')
        text = text.decode('utf-8')
        if picture[:26] == last[:26]:
            with open(target_dir_path + '/' + last, 'a', encoding='utf-8') as text_file:
                text_file.write(text)
        else:
            with open(target_dir_path + '/' + txt_name, 'w', encoding='utf-8') as text_file:
                print(picture)
                text_file.write(text)
        last = txt_name


if __name__ == '__main__':
    get_texts(jpgs_for_evaluation)
