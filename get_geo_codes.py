import urllib.request
from bs4 import BeautifulSoup
import re
import json


def get_codes():
    try:
        url = 'https://d-nb.info/standards/vocab/gnd/geographic-area-code.html'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            dir_page = response.read()
        dir_page = dir_page.decode('utf-8')
        dir_soup = BeautifulSoup(dir_page, 'html.parser')
        # print([table.find('td', class_="width70").text for table in dir_soup.find_all('table')])
        new_dict = {re.findall(r'#(.+)$', table.find('td', class_="width70").text)[0]: re.findall(r'gnd/(.+$)', found.find('a')['href'])[0]  for table in dir_soup.find_all('table') for found in table.find_all('td') if not found.attrs and 'd-nb.info' in found.string}
        with open('country_codes', 'w') as dict_file:
            json.dump(new_dict, dict_file)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    get_codes()
