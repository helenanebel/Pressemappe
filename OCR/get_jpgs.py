import urllib.request
from bs4 import BeautifulSoup
import os

# Tesseract liegt in: C:\Program Files\Tesseract-OCR
# für moritz die Texte generieren zum Zugriff auf die Beschreibung
# https://pm20.zbw.eu/list/publication/

jpgs_for_evaluation = [ "0000xx/000010/000xx/00002/PIC/P000010000000000000000020000_0000_00000000HP_A.JPG",
                        "0000xx/000010/000xx/00002/PIC/P000010000000000000000020001_0000_00000000HP_A.JPG",
                        "0000xx/000010/000xx/00001/PIC/P000010000000000000000010000_0000_00000000HP_A.JPG",
                        "0000xx/000012/000xx/00001/PIC/P000012000000191479000010000_0000_00000000HP_A.JPG",
                        "0000xx/000034/001xx/00168/PIC/P000034000000000000001680000_0000_00000P34HP_A.JPG",
                        "0077xx/007779/000xx/00001/PIC/P007779000000191478000010000_0000_00000000HP_A.JPG",
                        "0112xx/011242/000xx/00011/PIC/P011242000000191477000110000_0000_00000000HP_A.JPG",
                        "0074xx/007478/000xx/00004/PIC/P007478000000000000000040000_0000_00000000HP_A.JPG",
                        "0425xx/042518/000xx/00052/PIC/P042518000000000000000520000_0000_00000000KP_A.JPG",
                        "0425xx/042518/000xx/00052/PIC/P042518000000000000000520001_0000_00000000KP_A.JPG",
                        "0109xx/010995/000xx/00004/PIC/P010995000000000000000040000_0000_00000M48HP_A.JPG",
                        "0423xx/042397/000xx/00002/PIC/P042397000000191477000020000_0000_00000000HP_A.JPG",
                        "0423xx/042397/000xx/00002/PIC/P042397000000191477000020001_0000_00000000HP_A.JPG",
                        "0423xx/042397/000xx/00002/PIC/P042397000000191477000020002_0000_00000000HP_A.JPG",
                        "0423xx/042397/000xx/00002/PIC/P042397000000191477000020003_0000_00000000HP_A.JPG",
                        "0036xx/003644/000xx/00004/PIC/P003644000000000000000040000_0000_00000000HP_A.JPG",
                        "0000xx/000010/000xx/00005/PIC/P000010000000000000000050000_0000_00000000HP_A.JPG",
                        "0000xx/000012/000xx/00005/PIC/P000012000000191477000050000_0000_00000000HP_A.JPG",
                        "0000xx/000012/000xx/00005/PIC/P000012000000191477000050001_0000_00000000HP_A.JPG",
                        "0036xx/003644/000xx/00003/PIC/P003644000000000000000030000_0000_00000000HP_A.JPG",
                        "0044xx/004455/000xx/00001/PIC/P004455000000191478000010000_0000_00000000HP_A.JPG",
                        "0000xx/000022/000xx/00040/PIC/P000022000000000000000400000_0000_00000X49HP_A.JPG",
                        "0000xx/000022/000xx/00015/PIC/P000022000000000000000150000_0000_00000000HP_A.JPG",
                        "0032xx/003281/000xx/00008/PIC/P003281000000000000000080000_0000_00000000HP_A.JPG",
                        "0032xx/003281/000xx/00005/PIC/P003281000000000000000050000_0000_00000000HP_A.JPG",
                        "0000xx/000010/000xx/00006/PIC/P000010000000191477000060000_0000_00000000HP_A.JPG",
                        "0000xx/000010/000xx/00006/PIC/P000010000000191477000060001_0000_00000000HP_A.JPG",
                        "0000xx/000012/000xx/00002/PIC/P000012000000191479000020000_0000_00000000HP_A.JPG",
                        "0000xx/000034/001xx/00162/PIC/P000034000000000000001620000_0000_00000P34HP_A.JPG",
                        "0099xx/009942/000xx/00003/PIC/P009942000000000000000030000_0000_00000000HP_A.JPG",
                        "0099xx/009942/000xx/00003/PIC/P009942000000000000000030001_0000_00000000HP_A.JPG",
                        "0032xx/003274/000xx/00052/PIC/P003274000000000000000520000_0000_00000000HP_A.JPG",
                        "0090xx/009021/000xx/00004/PIC/P009021000000000000000040000_0000_00000X48HP_A.JPG",
                        "0001xx/000135/000xx/00067/PIC/P000135000000000000000670000_0000_00000X48HP_A.JPG",
                        "0046xx/004600/000xx/00003/PIC/P004600000000191477000030000_0000_00000000HP_A.JPG",
                        "0110xx/011060/000xx/00010/PIC/P011060000000191477000100000_0000_00000000HP_A.JPG",
                        "0110xx/011060/000xx/00040/PIC/P011060000000000000000400000_0000_00000000HP_A.JPG"]


def get_jpg_urls(jpg_amount: int = 2000):
    jpg_nr = 0
    jpg_urls = []
    url = 'https://zbw.eu/beta/pm20mets/pe/'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        dir_page = response.read()
    dir_page = dir_page.decode('utf-8')
    dir_soup = BeautifulSoup(dir_page, 'html.parser')
    for per_folder in [tr for tr in [tr.find('a')['href'] for tr in dir_soup.find_all('tr') if tr.find('a')] if 'xx' in tr]:
        if jpg_nr >= jpg_amount:
            jpg_urls = jpg_urls[:jpg_amount]
            break
        per_folder_url = 'https://zbw.eu/beta/pm20mets/pe/' + per_folder
        req = urllib.request.Request(per_folder_url)
        with urllib.request.urlopen(req) as response:
            per_folder_page = response.read()
        per_folder_page = per_folder_page.decode('utf-8')
        per_folder_soup = BeautifulSoup(per_folder_page, 'html.parser')
        for per_xml_url in [per_folder_url + tr for tr in [tr.find('a')['href'] for tr in per_folder_soup.find_all('tr') if tr.find('a')] if '.xml' in tr]:
            if jpg_nr >= jpg_amount:
                break
            req = urllib.request.Request(per_xml_url)
            with urllib.request.urlopen(req) as response:
                per_xml_page = response.read()
            per_xml_page = per_xml_page.decode('utf-8')
            print(per_xml_url)
            per_xml_soup = BeautifulSoup(per_xml_page, 'xml')
            jpg_urls += [img_tag['xlink:href'].replace('B.JPG', 'A.JPG') for img_tag in per_xml_soup.find('mets:fileGrp', USE="DEFAULT").find_all('mets:FLocat', LOCTYPE="URL")]
            jpg_nr = len(jpg_urls)
            print(jpg_nr)
    return jpg_urls


def get_jpg(jpg_url: str ,
             path_name: str = 'C://Users/Helena_Nebel/PycharmProjects/Pressemappe'):
    try:
        if 'jpgs' not in os.listdir(path_name + '/OCR'):
            os.mkdir('OCR/jpgs')
        print(jpg_url)
        jpg_name = jpg_url.replace('http://webopac.hwwa.de/DigiPerson/P/', '')
        jpg_name = jpg_name.replace('/', '_')
        urllib.request.urlretrieve(jpg_url, 'jpgs/' + jpg_name)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    jpg_list = ['http://webopac.hwwa.de/DigiPerson/P/' + jpg for jpg in jpgs_for_evaluation]
    for jpg in jpg_list:
        print(jpg)
        get_jpg(jpg)
