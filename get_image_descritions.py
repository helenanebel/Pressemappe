import urllib.request
from bs4 import BeautifulSoup
import re
import json


def get_jpg_descriptions(jpg_amount: int = 2000):
    all_descriptions = {}
    jpg_nr = 0

    url = 'https://zbw.eu/beta/pm20mets/pe/'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        dir_page = response.read()
    dir_page = dir_page.decode('utf-8')
    dir_soup = BeautifulSoup(dir_page, 'html.parser')
    for per_folder in [tr for tr in [tr.find('a')['href'] for tr in dir_soup.find_all('tr') if tr.find('a')] if 'xx' in tr]:
        if jpg_nr >= jpg_amount:
            break
        per_folder_url = 'https://zbw.eu/beta/pm20mets/pe/' + per_folder
        print(per_folder_url)
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
            per_xml_soup = BeautifulSoup(per_xml_page, 'xml')
            for jpg_url in [img_tag['xlink:href'].replace('B.JPG', 'A.JPG') for img_tag in per_xml_soup.find('mets:fileGrp', USE="DEFAULT").find_all('mets:FLocat', LOCTYPE="URL")]:
                jpg_name = jpg_url.replace('http://webopac.hwwa.de/DigiPerson/P/', '')
                jpg_name = jpg_name.replace('/', '_')
                doc_nr = 'doc' + re.findall(r'_([^_]+)_PIC', jpg_name)[0]
                article_description = per_xml_soup.find('mets:structMap', TYPE="LOGICAL").find('mets:div', ID=doc_nr)['LABEL']
                if 'Presseartikel' not in article_description:
                    all_descriptions[jpg_name] = article_description
    with open('descriptions.json', 'w') as file:
        json.dump(all_descriptions, file)

if __name__ == '__main__':
    get_jpg_descriptions()