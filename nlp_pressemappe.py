import spacy
import os
import json
from collections import Counter
nlp = spacy.load('xx_ent_wiki_sm')
docs ='path to files'

def get_filename(path):
    return [i.path for i in os.scandir(path) if i.is_file()]

files=get_filename(docs)
final_dict = {}
for filepath in files:

    with open(filepath, 'r', encoding='UTF8') as file_to_read:
        some_text = file_to_read.read()
        base_name = os.path.basename(filepath)
        print(base_name)
        doc = nlp(some_text)
        perlist=[]
        loclist=[]
        for ent in doc.ents:
             if ent.label_ == "PER":
                perlist.append(str(ent))
             elif ent.label_ == "LOC":
                loclist.append(str(ent))
        final_list = []

        # Entitäten ählen (PER)
        c = Counter(perlist)
        for p, count in c.most_common():
            final_list.append({
                'name': p,
                'type': 'PER',
                'frequency': count
            })

        # Entitäten zählen LOC)
        c = Counter(loclist)
        for l, count in c.most_common():
            final_list.append({
                'name': l,
                'type': 'LOC',
                'frequency': count
            })


        final_dict[base_name] = final_list

        print('Final result', final_dict)


with open('entities.json', mode="r+") as file:
    file.seek(0, 2)
    position = file.tell()
    file.seek(position)
    file.write(",{}".format(json.dumps(final_dict, indent=1)))
