import json
import unidecode
from OCR.tesseract_pressemappe import get_text_files_from_jpgs
import os
import re
import sys

journals_published_in = {}
pub_list = json.load(open('all_pubs.json', 'r'))
with open('descriptions.json', 'r') as descriptions:
    des = json.load(descriptions)
    last_file = ''
    pic_nr = 0
    for picture in os.listdir('jpgs'):
        with open('journals_published_in.json', 'r') as file:
            journals_published_in = json.load(file)
        if pic_nr >= 100:
            break
        else:
            pic_nr += 1
        if picture[:26] == last_file[:26]:
            continue
        print(picture)
        journals_published_in[picture] = ''
        found_pub = []
        year = None
        try:
            for pub in pub_list:
                if 'title' in pub_list[pub]:
                    title = pub_list[pub]['title'].lower().replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace(
                        '@', '').replace('ç', 'c')
                    title = unidecode.unidecode(title)
                    if picture in des:
                        description = \
                            des[picture].lower().replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('´', '').replace('ç', 'c')
                        description = unidecode.unidecode(description)
                        if 'quellenangabe' in description:
                            continue
                        if re.findall(r'19\d{2}', description):
                            year = re.findall(r'19\d{2}', description)[0]
                        if title in description:
                            found_pub = [pub_list[pub]]
            if not found_pub:
                text = get_text_files_from_jpgs([picture], 'jpgs', save_file=False)
                text = text[:300].lower().replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace(
                    '@', '').replace('ç', 'c')
                # print(text)
                if re.findall(r'19\d{2}', text):
                    year = re.findall(r'19\d{2}', text)[0]
                elif re.findall(r'19\d{1}', text):
                    year = re.findall(r'19\d{1}', text)[0] + '0'
                # lower evtl. wieder rausnehmen.
                all_pubs_found = []
                for pub in pub_list:
                    if 'title' in pub_list[pub]:
                        title_unreplaced_umlauts = pub_list[pub]['title'].lower().replace('@', '').replace('ç', 'c')
                        title = pub_list[pub]['title'].lower().replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('@', '').replace('ç', 'c')
                        title = unidecode.unidecode(title)
                        if title in text:
                            all_pubs_found.append(pub_list[pub])
                found_pub = [pub for pub in all_pubs_found if len(pub['title'].split()) > 1]
            for pub in found_pub:
                if not pub['end_date']:
                    pub['end_date'] = '2000'
            if len(found_pub) != 1:
                if year:
                    found_pub = [pub for pub in found_pub if pub['start_date'] <= year <= pub['end_date']]
                    if len(found_pub) > 1:
                        found_pub = [pub for pub in found_pub if not pub['sub_title']]
            if found_pub:
                journals_published_in[picture] = {'url': 'https://www.zeitschriftendatenbank.de/api/hydra/?q=zdbid%3D' + \
                                                 found_pub[0]['id'], 'title': found_pub[0]['title'], 'year': year}
                with open('journals_published_in.json', 'w') as file:
                    json.dump(journals_published_in, file)
            print('year:', year)
            if picture in journals_published_in:
                print(journals_published_in[picture])
            else:
                print('not found')
            last_file = picture
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('Error! Code: {c}, Message, {m}, Type, {t}, File, {f}, Line {line}'.format(
                c=type(e).__name__, m=str(e), t=exc_type, f=fname, line=exc_tb.tb_lineno))
            last_file = ''
print(journals_published_in)







# es sind 24393 JPGS mit Beschreibungen versehen.
# von den 24145 publikationen, die über eine Quellenangabe verfügen,
# werden 23755 erfoglreich zugeordnet, 390 nicht zugeordnet,
# weil teilweise Namen falsch geschrieben sind (40 der nicht zugeordneten Publikationen entfallen auf Pester Loyd)
# oder die Namen der Publikationen in der Publikationsliste fehlen (22 der Publikationen entfallen auf das Zagreber Tagblatt)
# manche Beschreibungen bestehen nur aus Aufsatz [Aufsatznummer] ([Seitenanzahl] S.)