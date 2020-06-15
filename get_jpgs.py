import urllib.request
from bs4 import BeautifulSoup
import os

# Tesseract liegt in: C:\Program Files\Tesseract-OCR
# für moritz die Texte generieren zum Zugriff auf die Beschreibung
# https://pm20.zbw.eu/list/publication/


def get_jpgs():
    try:
        if 'jpgs' not in os.listdir('C://Users/Helena_Nebel/PycharmProjects/Pressemappe'):
            os.mkdir('jpgs')
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
                jpg_urls = [img_tag['xlink:href'].replace('B.JPG', 'A.JPG') for img_tag in per_xml_soup.find('mets:fileGrp', USE="DEFAULT").find_all('mets:FLocat', LOCTYPE="URL")]
                jpg_nr=0
                for url in jpg_urls:
                    print(url)
                    jpg_nr+=1
                    jpg_name = url.replace('http://webopac.hwwa.de/DigiPerson/P/', '')
                    jpg_name = jpg_name.replace('/', '_')
                    urllib.request.urlretrieve(url, 'jpgs/' + jpg_name)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    get_jpgs()
