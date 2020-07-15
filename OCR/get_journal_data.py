import urllib.request
from bs4 import BeautifulSoup
import json

url = 'https://pm20.zbw.eu/list/publication/'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    publications_page = response.read()
publications_page = publications_page.decode('utf-8')
publications_soup = BeautifulSoup(publications_page, 'html.parser')
nr= 0
all_pubs = {}
for tr in publications_soup.find_all('tr'):
    if tr.find('a'):
        id = tr.find('a')['href'].split('/')[-1]
        if id:
            journal_url = 'https://www.zeitschriftendatenbank.de/api/hydra/?q=zdbid%3D' + id
            # print(journal_url)
            try:
                req = urllib.request.Request(journal_url)
                with urllib.request.urlopen(req) as response:
                    journal_page = response.read()
                journal_page = journal_page.decode('utf-8')
                data_dict = {'id': id}
                for field in json.loads(journal_page)['member']:
                    data = field['data']
                    data_dict['language_code'] = data['010@'][0][0]['a'] if '010@' in data else ''
                    data_dict['start_date'] = ''
                    data_dict['end_date'] = ''
                    for subfield in data['011@'][0]:
                        data_dict['start_date'] = subfield['a']  if 'a' in subfield else data_dict['start_date']
                        data_dict['end_date']  = subfield['b']  if 'b' in subfield else data_dict['end_date']
                    data_dict['title'] = ''
                    data_dict['sub_title'] = ''
                    data_dict['responsible'] = ''
                    for subfield in data['021A'][0]:
                        data_dict['title'] = subfield['a'] if 'a' in subfield else data_dict['title']
                        data_dict['sub_title'] = subfield['d'] if 'd' in subfield else data_dict['sub_title']
                        data_dict['responsible'] = subfield['h'] if 'h' in subfield else data_dict['responsible']
                    if '021C' in data:
                        data_dict['series'] = data['021C'][0][0]['a']  if 'a' in data['021C'][0][0] else ''
                    data_dict['par_title'] = ''
                    data_dict['par_sub_title'] = ''
                    data_dict['par_responsible'] = ''
                    if '021G' in data:
                        for subfield in data['021G'][0]:
                            data_dict['par_title'] = subfield['a'] if 'a' in subfield else data_dict['par_title']
                            data_dict['par_sub_title'] = subfield['d'] if 'd' in subfield else data_dict['par_sub_title']
                            data_dict['par_responsible'] = subfield['h'] if 'h' in subfield else data_dict['par_responsible']
                    data_dict['short_title'] = data['026C'][0][0]['a'] if '026C' in data else ''
                    data_dict['place'] = ''
                    data_dict['publisher'] = ''
                    if '033A' in data:
                        for subfield in data['033A'][0]:
                            data_dict['place'] = subfield['p'] if 'p' in subfield else data_dict['place']
                            data_dict['publisher'] = subfield['n'] if 'n' in subfield else data_dict['publisher']
                    # bis hier funktionierend
                    data_dict['previous_resources'] = []
                    data_dict['following_resources'] = []
                    if '039E' in data:
                        for subfield in data['039E']:
                            if subfield[0]['b'] == 'f':
                                data_dict['previous_resources'] += [item[0] for item in subfield if isinstance(item, list)]
                            else:
                                data_dict['following_resources'] += [item[0] for item in subfield if
                                                                    isinstance(item, list)]
                all_pubs[id] = data_dict

            except Exception as e:
                print(journal_url, e)
        nr += 1

with open('all_pubs.json', 'w') as file:
    json.dump(all_pubs, file)