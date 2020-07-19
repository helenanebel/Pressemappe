import json
import os
from nltk.corpus import stopwords

with open("stopword_language.json", mode="r", encoding="utf-8") as file:
    language_codes = json.load(file)

def filter_stopwords(name, language):
    if language in language_codes:
        exclude = set(stopwords.words(language_codes[language]))
        filter_name = " ".join([part for part in name.split() if part.lower() not in exclude])
    else:
        filter_name = name
    return filter_name

if "article_entities" not in os.listdir():
    os.mkdir("article_entities")

for image_name in os.listdir("article_member"):
    with open("article_member/" + image_name, "r") as file:
        image = json.load(file)

    for entity in image:

        filtered_name = filter_stopwords(entity["name"], entity["language"])

        # genaue Übereinstimmung bei Geografika
        if entity["type"] == "LOC":
            for match in entity["possible_gnd"]:
                if match["names"].count(entity["name"]) > 0:
                    if "gnd" not in entity:
                        entity["gnd"] = match
                    else:
                        entity.pop("gnd", None)
            if "gnd" in entity:
                entity.pop("possible_gnd", None)

        # genaue Übereinstimmung bei Geografika ohne Stoppwörter
        if "gnd" not in entity:
            if entity["type"] == "LOC":
                for match in entity["possible_gnd"]:
                    if match["names"].count(filtered_name) > 0:
                        if "gnd" not in entity:
                            entity["gnd"] = match
                        else:
                            entity.pop("gnd", None)
                if "gnd" in entity:
                    entity.pop("possible_gnd", None)

        # nur Treffer mit vollständigen Namen berücksichtigen
        if "gnd" not in entity and len(filtered_name.split()) > 1:
            delete_match = []
            for match in entity["possible_gnd"]:
                match_names = match["names"][:]
                for match_name in match["names"]:
                    filtered_remains = filtered_name.split()
                    for part in match_name.split():
                        for word in filtered_remains[:]:
                            if word in part:
                                filtered_remains.remove(word)
                    if len(filtered_remains) > 0:
                        match_names.remove(match_name)
                if not match_names:
                    delete_match.append(match)
            if len(delete_match) != len(entity["possible_gnd"]):
                for match in delete_match:
                    entity["possible_gnd"].remove(match)

    with open("article_member/../article_entities/" + image_name, "w+") as file:
        json.dump(image, file, indent=4)

for image_name in os.listdir("article_entities"):
    with open("article_entities/" + image_name, "r") as file:
        image = json.load(file)
    for entity in image:
        filtered_name = filter_stopwords(entity["name"], entity["language"])

        nimage = image[:]
        nimage.remove(entity)

        # Beziehungen prüfen, wenn Name aus mehreren Wörtern besteht
        if "gnd" not in entity and len(filtered_name.split()) > 1:
            most_relations = 0
            for match in entity["possible_gnd"]:
                relevant_relations = 0
                for nentity in nimage:
                    if "gnd" in nentity and nentity["gnd"]:
                        try:
                            if (nentity["gnd"]["identifier"] in match["relations"]) or (match["identifier"] in nentity["gnd"]["relations"]):
                                relevant_relations += 1
                        except KeyError:
                            continue
                if relevant_relations == most_relations:
                    # Treffer mit meisten Beziehungen auswählen
                    if "gnd" in entity and entity["gnd"]:
                        entity.pop("gnd", None)
                    else:
                        entity["gnd"] = match
                elif relevant_relations > most_relations:
                    entity["gnd"] = match
                    most_relations = 0 + relevant_relations

            if "gnd" in entity:
                entity.pop("possible_gnd", None)

    with open("article_entities/" + image_name, "w+") as file:
        json.dump(image, file, indent=4)
