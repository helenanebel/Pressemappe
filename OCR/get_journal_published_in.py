import json
import unidecode
from OCR.tesseract_pressemappe import get_text_files_from_jpgs
import os

journals_published_in = {}
pub_list = json.load(open('all_pubs.json', 'r'))
with open('descriptions.json', 'r') as descriptions:
    des = json.load(descriptions)
    last_file = ''
    pic_nr = 0
    for picture in os.listdir('jpgs'):
        if pic_nr >= 100:
            break
        else:
            pic_nr += 1
        if picture[:26] == last_file[:26]:
            continue
        print(picture)
        journals_published_in[picture] = ''
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
                        if title in description:
                            journals_published_in[picture] = 'https://zdb-katalog.de/list.xhtml?t=zdb%3D' + pub + '&key=cql'
            if not journals_published_in[picture]:
                text = get_text_files_from_jpgs([picture], 'jpgs', save_file=False)
                for pub in pub_list:
                    if 'title' in pub_list[pub]:
                        title = pub_list[pub]['title'].lower().replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('@', '').replace('ç', 'c')
                        title = unidecode.unidecode(title)
                        if title in text:
                            journals_published_in[picture] = 'https://zdb-katalog.de/list.xhtml?t=zdb%3D' + pub + '&key=cql'
            last_file = picture
        except Exception as e:
            print(e)
            last_file = ''
print(journals_published_in)
with open('journals_published_in.json', 'w') as file:
    json.dump(journals_published_in, file)






# es sind 24393 JPGS mit Beschreibungen versehen.
# von den 24145 publikationen, die über eine Quellenangabe verfügen,
# werden 23755 erfoglreich zugeordnet, 390 nicht zugeordnet,
# weil teilweise Namen falsch geschrieben sind (40 der nicht zugeordneten Publikationen entfallen auf Pester Loyd)
# oder die Namen der Publikationen in der Publikationsliste fehlen (22 der Publikationen entfallen auf das Zagreber Tagblatt)
# manche Beschreibungen bestehen nur aus Aufsatz [Aufsatznummer] ([Seitenanzahl] S.)