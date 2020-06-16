import spacy
import os
import json
from collections import Counter
from langdetect import detect
nlp = spacy.load('xx_ent_wiki_sm')
nlpit = spacy.load('it_core_news_sm')
nlpde = spacy.load('de_core_news_md')
nlpfr = spacy.load('fr_core_news_md')
nlpen = spacy.load('en_core_web_md')

docs ='pressemappe_text_Files' # Pfad zum Dateien Corpus
final_dict = {}  # speichert finalen Output in einem einzigen Dictionary
def get_filename(path):
    return [i.path for i in os.scandir(path) if i.is_file()]
files=get_filename(docs)

for filepath in files:

    with open(filepath, 'r', encoding='UTF8') as file_to_read:
        some_text = file_to_read.read()
        base_name = os.path.basename(filepath)
        print(base_name)
        lang = detect(some_text)
        print(lang)
        if lang == 'fr':
            doc = nlpfr(some_text)
        elif lang == 'it':
            doc = nlpit(some_text)
        elif lang== 'fr':
            doc = nlpfr(some_text)
        elif lang == 'de':
            doc = nlpde(some_text)
        else:
            doc = nlp(some_text)
        perlist=[]
        loclist=[]
        for ent in doc.ents:
             if ent.label_ == "PER":
                perlist.append(str(ent))
             elif ent.label_ == "LOC":
                loclist.append(str(ent))
        final_list = []  # {JPG_basename.txt": final_list}

        # Entitäten zählen (PER)
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

        # Speicherung der Listen im Dictionary.
        # z.B. final_dict['JPG_basename.txt'] = [{'name': 'Abbas Hilmi', 'type': 'PER', 'frequency': 2}, ...]
        final_dict[base_name.replace('txt', 'JPG')] = final_list
        print('Final result', final_dict)

# Speicherung Dictionary in JSON Datei zur Weiterverarbeitung
with open('entities.json', mode="r+") as file:
    file.seek(0, 2)
    position = file.tell()
    file.seek(position)
    file.write(",{}".format(json.dumps(final_dict, indent=1)))
