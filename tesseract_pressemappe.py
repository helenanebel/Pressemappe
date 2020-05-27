from PIL import Image
import pytesseract
import language_codes
from langdetect import detect
import os

# Tesseract liegt in: C:\Program Files\Tesseract-OCR
# für moritz die Texte generieren zum Zugriff auf die Beschreibung
# https://pm20.zbw.eu/list/publication/

def get_text_files_from_jpgs():
    if 'pressemappe_text_files' not in os.listdir('C://Users/Helena_Nebel/PycharmProjects/Pressemappe'):
        os.mkdir('pressemappe_text_files')
    jpg_nr = 0
    for jpg_name in os.listdir('jpgs_edited'):
        lang_code=None
        with open('jpgs_edited/' + jpg_name, 'rb') as jpg_file:
            jpg_name = jpg_name.replace('.JPG', '')
            txt=open("pressemappe_text_files/"+jpg_name+".txt", mode='w+', encoding='utf-8')
            txt_name = jpg_name.replace('JPG', 'txt')
            try:
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                text = str(((pytesseract.image_to_string(Image.open(jpg_file)))))
                print(text.replace('\n', ' '))
                print(len(text))
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
                text = str(((pytesseract.image_to_string(Image.open(jpg_file), lang=lang_code))))
                print(text.replace('\n', ' '))
                print(len(text))
                if lang_code == 'deu':
                    text = str(((pytesseract.image_to_string(Image.open(jpg_file), lang='deu_frak'))))
                    print(text.replace('\n', ' '))
                with open('pressemappe_text_files/' + txt_name, 'w') as text_file:
                    text_file.write(text)
            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    get_text_files_from_jpgs()
