from PIL import Image
import pytesseract
import language_codes
from langdetect import detect
import urllib.request
from bs4 import BeautifulSoup
import os


def get_text_files():
    if 'pressemappe_text_files' not in os.listdir('/home/hnebel/IdeaProjects/Pressemappe'):
        os.mkdir('pressemappe_text_files')
    url = 'https://zbw.eu/beta/pm20mets/pe/'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        dir_page = response.read()
    dir_page = dir_page.decode('utf-8')
    dir_soup = BeautifulSoup(dir_page, 'html.parser')

    for per_folder in [tr for tr in [tr.find('a')['href'] for tr in dir_soup.find_all('tr') if tr.find('a')] if 'xx' in tr]:
        per_folder_url = 'https://zbw.eu/beta/pm20mets/pe/' + per_folder
        req = urllib.request.Request(per_folder_url)
        with urllib.request.urlopen(req) as response:
            per_folder_page = response.read()
        per_folder_page = per_folder_page.decode('utf-8')
        per_folder_soup = BeautifulSoup(per_folder_page, 'html.parser')
        for per_xml_url in [per_folder_url + tr for tr in [tr.find('a')['href'] for tr in per_folder_soup.find_all('tr') if tr.find('a')] if '.xml' in tr]:
            req = urllib.request.Request(per_xml_url)
            with urllib.request.urlopen(req) as response:
                per_xml_page = response.read()
            per_xml_page = per_xml_page.decode('utf-8')
            per_xml_soup = BeautifulSoup(per_xml_page, 'xml')
            jpg_urls = [img_tag['xlink:href'] for img_tag in per_xml_soup.find('mets:fileGrp', USE="DEFAULT").find_all('mets:FLocat', LOCTYPE="URL")]

            lang_code=None
            # txt=open("pressemappe_text_files/"+dirname+".txt", mode='w+', encoding='utf-8')
            jpg_nr=0
            for url in jpg_urls:
                print(url)
                jpg_nr+=1
                webfile = urllib.request.urlopen(url)
                jpg_name = url.replace('http://webopac.hwwa.de/DigiPerson/P/', '')
                jpg_name = jpg_name.replace('/', '_')
                txt_name = jpg_name.replace('JPG', 'txt')
                print('file is open')
                try:
                    text = str(((pytesseract.image_to_string(Image.open(webfile),lang="deu"))))
                    print(text)
                    print('text is read')
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
                    #text = str(((pytesseract.image_to_string(Image.open(webfile),lang=lang_code))))
                    with open(txt_name, 'w') as text_file:
                        text_file.write(text)
                except Exception as e:
                    print(e)
                    continue

if __name__ == '__main__':
    get_text_files()

