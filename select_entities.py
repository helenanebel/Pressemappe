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


if "image_entities" not in os.listdir():
    os.mkdir("image_entities")

for image_name in os.listdir("image_member"):
    with open("image_member/" + image_name, "r") as file:
        image = json.load(file)

    for entity in image:

        filtered_name = filter_stopwords(entity["name"], entity["language"])

        # genaue Übereinstimmung bei Geografika
        if entity["type"] == "LOC":
            for match in entity["possible_gnd"]:
                if match["names"].count(entity["name"]) > 0:
                    entity["gnd"].append(match)
                    break
            entity.pop("possible_gnd", None)

        # genaue Übereinstimmung bei Geografika ohne Stoppwörter
        if not entity["gnd"]:
            if entity["type"] == "LOC":
                for match in entity["possible_gnd"]:
                    if match["names"].count(filtered_name) > 0:
                        entity["gnd"].append(match)
                        break
                entity.pop("possible_gnd", None)

        # nur Treffer mit vollständigen Namen behalten
        if not entity["gnd"] and len(filtered_name.split()) > 1:
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

        nimage = image[:]
        nimage.remove(entity)

    with open("image_member/../image_entities/" + image_name, "w+") as file:
        json.dump(image, file, indent=4)


for image_name in os.listdir("image_entities"):
    with open("image_entities/" + image_name, "r") as file:
        image = json.load(file)
    for entity in image:
        filtered_name = filter_stopwords(entity["name"], entity["language"])

        # Beziehungen zu eindeutigen Entitäten abgleichen
        nimage = image[:]
        nimage.remove(entity)
        if not entity["gnd"] and len(filtered_name.split()) > 1:
            most_relations = 0
            for match in entity["possible_gnd"]:
                relevant_relations = 0
                for nentity in nimage:
                    if nentity["gnd"]:
                        for match2 in nentity["gnd"]:
                            try:
                                if (match2["identifier"] in match["relations"]) or (match["identifier"] in match2["relations"]):
                                    relevant_relations += 1
                            except KeyError:
                                continue
                if relevant_relations == most_relations:
                    entity["gnd"].append(match)
                elif relevant_relations > most_relations:
                    entity["gnd"] = [match]
                    most_relations = 0 + relevant_relations

            entity.pop("possible_gnd", None)

    with open("image_entities/" + image_name, "w+") as file:
        json.dump(image, file, indent=4)
