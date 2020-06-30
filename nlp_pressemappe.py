import spacy
import os
import json
from collections import Counter
from langdetect import detect
nlp = spacy.load('xx_ent_wiki_sm')
nlpit = spacy.load('it_core_news_sm')
nlpde = spacy.load('de_core_news_sm')
nlpfr = spacy.load('fr_core_news_sm')
nlpen = spacy.load('en_core_web_sm')

docs ='zp' # Pfad zum Dateien Corpus
end_dict = {}  # speichert finalen Output in einem einzigen Dictionary
def get_filename(path):
    return [i.path for i in os.scandir(path) if i.is_file()]
files=get_filename(docs)

for filepath in files:

    with open(filepath, 'r', encoding='UTF8') as file_to_read:
        article_text = file_to_read.read()
        base_name = os.path.basename(filepath)
        print(base_name)
        lang = detect(article_text)
        print(lang)
        if lang == 'fr':
            doc = nlpfr(article_text)
        elif lang == 'it':
            doc = nlpit(article_text)
        elif lang == 'en':
            doc = nlpen(article_text)
        elif lang == 'de':
            doc = nlpde(article_text)
        else:
            doc = nlp(article_text)
        plist=[]
        llist=[]
        for ent in doc.ents:
             if ent.label_ == "PER":
                plist.append(str(ent))
             elif ent.label_ == "LOC":
                llist.append(str(ent))
        end_list = []

        # Entitäten zählen (PER)
        c = Counter(plist)
        for person, count in c.most_common():
            end_list.append({
                'name': person,
                'type': 'PER',
                'frequency': count,
                'Language': lang
            })

        # Entitäten der Locations zählen
        c = Counter(llist)
        for location, count in c.most_common():
            end_list.append({
                'name': location,
                'type': 'LOC',
                'frequency': count,
                'Language': lang
            })

        # Speicherung der Listen im Dictionary.
        # z.B. final_dict['JPG_basename.txt'] = [{'name': 'Abbas Hilmi', 'type': 'PER', 'frequency': 2}, ...]
        end_dict[base_name.replace('txt', 'JPG')] = end_list
        print('Final result', end_dict)
        print(type(end_dict))
sprachen={"ar": "arabic", "az": "azerbaijani", "da": "danish", "de": "german", "el": "greek", "en": "english", "es": "spanish", "fi": "finnish", "fr": "french", "hu": "hungarian", "id": "indonesian", "it": "italian", "kk": "kazakh", "ne": "nepali", "nl": "dutch", "no": "norwegian", "pt": "portuguese", "ro": "romanian", "ru": "russian", "sl": "slovene", "sv": "swedish", "tg": "tajik", "tr": "turkish"}
print(end_dict)

        # dict3 = {k: sprachen[v] for k, v in end_dict.items()}

for k, v in end_dict.items():
    for i in v:
        for m, w in i.items():
            if m == "Language":
                #print(i[m])
                i[m] = sprachen[w]


# Speicherung Dictionary in JSON Datei zur Weiterverarbeitung
with open('entities.json', mode="r+") as file:
    file.seek(0, 2)
    position = file.tell()
    file.seek(position)
    file.write(",{}".format(json.dumps(end_dict, indent=1)))
