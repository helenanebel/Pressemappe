import pytesseract
import language_codes
from langdetect import detect
import os
import cv2 as cv

# Tesseract liegt in: C:\Program Files\Tesseract-OCR
# für moritz die Texte generieren zum Zugriff auf die Beschreibung
# https://pm20.zbw.eu/list/publication/

def get_text_files_from_jpgs(jpg_names_list, dir_path):
    if 'pressemappe_text_files' not in os.listdir('C://Users/Helena_Nebel/PycharmProjects/Pressemappe'):
        os.mkdir('pressemappe_text_files')
    jpg_nr = 0
    for jpg_name in jpg_names_list:
        lang_code=None
        print(jpg_name)
        txt_name = jpg_name.replace('.jpg', '').replace('.JPG', '')
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            print(dir_path + jpg_name)
            text = str(pytesseract.image_to_string(cv.imread(dir_path + jpg_name)))
            # print(text.replace('\n', ' '))
            # print(len(text))
            language=language_codes.resolve(detect(text))
            print(language)
            if language!='ger':
                if language=='fre':
                    lang_code='fra'
                if language=='ita':
                    lang_code='ita'
                if language=='dut':
                    lang_code='nld'
                if language=='spa':
                    lang_code='spa'
            else:
                lang_code = 'deu'
            text = str(pytesseract.image_to_string(cv.imread(dir_path + jpg_name), lang=lang_code))

            if lang_code == 'deu':
                text = str(pytesseract.image_to_string(cv.imread(dir_path + jpg_name), lang='deu_frak'))
                # print(text.replace('\n', ' '))
            text.encode('utf8')
            # print(text.replace('\n', ' '))
            # print(len(text))
            with open('pressemappe_text_files/' + txt_name, 'w') as text_file:
                text_file.write(text)
        except Exception as e:
            print(e)
            continue



if __name__ == '__main__':
    jpg_names_list = os.listdir('jpgs_sharpened')
    get_text_files_from_jpgs(jpg_names_list, 'jpgs_sharpened/')
