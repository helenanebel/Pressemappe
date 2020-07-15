import json
import unidecode
from OCR.tesseract_pressemappe import get_text_files_from_jpgs
import os

pub_list = json.load(open('all_pubs.json', 'r'))
with open('descriptions.json', 'r') as descriptions:
    des = json.load(descriptions)
    descriptions_nr = 0
    success_nr = 0
    without_quellenangabe = 0
    for d in des:
        description = des[d].lower().replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('´', "'").replace('ç', 'c')
        description = unidecode.unidecode(description)
        descriptions_nr += 1
        if 'quellenangabe' in description:
            without_quellenangabe += 1
            continue
        success = False
        for pub in pub_list:
            if success:
                success_nr += 1
                break
            if 'title' in pub_list[pub]:
                title = pub_list[pub]['title'].lower().replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('@', '').replace('ç', 'c')
                title = unidecode.unidecode(title)
                if title in description:
                    success = True
        if not success:
            if d in os.listdir('jpgs'):
                get_text_files_from_jpgs([d], source_dir_path='jpgs')
                d = d.replace('.JPG', '')
                with open('pressemappe_text_files/' + d , 'r') as textfile:
                    print(textfile.read())
            # hier noch die OCR-Texte überprüfen.
# Richtung ändern, sodass die Publikationen in den Descriptions gesucht werden; dann geht das mit dem OCR auch.

# es sind 24393 JPGS mit Beschreibungen versehen.
# von den 24145 publikationen, die über eine Quellenangabe verfügen,
# werden 23755 erfoglreich zugeordnet, 390 nicht zugeordnet,
# weil teilweise Namen falsch geschrieben sind (40 der nicht zugeordneten Publikationen entfallen auf Pester Loyd)
# oder die Namen der Publikationen in der Publikationsliste fehlen (22 der Publikationen entfallen auf das Zagreber Tagblatt)
# manche Beschreibungen bestehen nur aus Aufsatz [Aufsatznummer] ([Seitenanzahl] S.)