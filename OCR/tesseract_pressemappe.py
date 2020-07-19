import pytesseract
import language_codes
from langdetect import detect
import os
import cv2 as cv
import sys

# Tesseract liegt in: C:\Program Files\Tesseract-OCR


def get_jpg_names_list(source_dir_path: str):
    return os.listdir(source_dir_path)


def get_text_files_from_jpgs(jpg_names_list: list,
                             source_dir_path: str = 'jpgs_added',
                             target_dir_path: str = 'test_added',
                             tesseract_dir_path: str = r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                             path_name: str = 'C://Users/Helena_Nebel/PycharmProjects/Pressemappe/OCR',
                             save_file: bool = True,
                             img_obj = None, img_obj_given: bool = False):
    if target_dir_path not in os.listdir(path_name):
        os.mkdir(target_dir_path)
    last_file = ''
    jpg_names_list.sort()
    for jpg_name in jpg_names_list:
        lang_code = None
        print(jpg_name)
        txt_name = jpg_name.replace('.jpg', '').replace('.JPG', '')
        if not img_obj_given:
            img = cv.imread(source_dir_path + '/' + jpg_name)
        else:
            img = img_obj
        try:
            pytesseract.pytesseract.tesseract_cmd = tesseract_dir_path
            text = str(pytesseract.image_to_string(img))
            language=language_codes.resolve(detect(text))
            print(language)
            if language != 'ger':
                if language == 'fre':
                    lang_code = 'fra'
                if language == 'ita':
                    lang_code = 'ita'
                if language == 'dut':
                    lang_code = 'nld'
                if language == 'spa':
                    lang_code = 'spa'
            else:
                lang_code = 'deu'
            text = str(pytesseract.image_to_string(img, lang=lang_code))
            if lang_code == 'deu':
                text_frak = str(pytesseract.image_to_string(img, lang='deu_frak'))
            else:
                text_frak = ''
            text = text + '\n' + text_frak
            text = text.encode('utf-8')
            text = text.decode('utf-8')
            if save_file:
                if jpg_name[:26] == last_file[:26]:
                    with open(target_dir_path + '/' + txt_name, 'a', encoding='utf-8') as text_file:
                        text_file.write(' \n' + text)
                else:
                    with open(target_dir_path + '/' + txt_name, 'w', encoding='utf-8') as text_file:
                        text_file.write(text)
            last_file = jpg_name
            return text
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('Error! Code: {c}, Message, {m}, Type, {t}, File, {f}, Line {line}'.format(
                c=type(e).__name__, m=str(e), t=exc_type, f=fname, line=exc_tb.tb_lineno))


if __name__ == '__main__':
    # main_jpg_names_list = get_jpg_names_list('jpgs/')
    print(get_text_files_from_jpgs(jpg_names_list=['0000xx_000010_000xx_00001_PIC_P000010000000000000000010000_0000_00000000HP_A.JPG'],
                             source_dir_path='jpgs_sharpened'))
