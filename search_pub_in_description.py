import json
import unidecode

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
            print('no success')
            print(des[d])
print(descriptions_nr, success_nr, without_quellenangabe)
print(descriptions_nr-without_quellenangabe)
print(descriptions_nr-without_quellenangabe-success_nr)

# es sind 24393 JPGS mit Beschreibungen versehen.
# von den 24145 publikationen, die über eine Quellenangabe verfügen,
# werden 23755 erfoglreich zugeordnet, 390 nicht zugeordnet,
# weil teilweise Namen falsch geschrieben sind oder die Namen der Publikationen in der Publikationsliste fehlen.