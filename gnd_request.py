import json
import urllib
from urllib import request, parse
from fuzzywuzzy import fuzz

with open("./entities.json", mode="r", encoding="utf-8") as file:
    image_list = json.load(file)[0]

# führt eindeutige Dubletten zusammen
for image in image_list:

    per_list = []
    loc_list = []

    for entity in image_list[image]:
        if entity["type"] == "PER":
            per_list.append(entity["name"])
        else:
            loc_list.append(entity["name"])

    per_possible_duplicate_list = []
    loc_possible_duplicate_list = []

    for name in per_list:
        temp_per_list = per_list[:per_list.index(name)] + per_list[per_list.index(name) + 1:]

        for other_name in temp_per_list:

            # Simpson == Homer Simpson, andere Minimalwerte möglich
            if fuzz.token_set_ratio(name, other_name) == 100:
                if sorted([name, other_name]) not in per_possible_duplicate_list:
                    per_possible_duplicate_list.append(sorted([name, other_name]))

    for name in loc_list:
        temp_loc_list = loc_list[:loc_list.index(name)] + loc_list[loc_list.index(name) + 1:]

        for other_name in temp_loc_list:

            if fuzz.token_set_ratio(name, other_name) == 100:
                if sorted([name, other_name]) not in loc_possible_duplicate_list:
                    loc_possible_duplicate_list.append(sorted([name, other_name]))

    per_duplicate_list = []
    loc_duplicate_list = []

    for possible_duplicate in per_possible_duplicate_list:
        per_duplicate_list += possible_duplicate

    for possible_duplicate in loc_possible_duplicate_list:
        loc_duplicate_list += possible_duplicate

    for name in per_duplicate_list:
        if per_duplicate_list.count(name) > 1:
            for possible_duplicate in per_possible_duplicate_list:
                if name in possible_duplicate:
                    per_possible_duplicate_list.remove(possible_duplicate)

    for name in loc_duplicate_list:
        if loc_duplicate_list.count(name) > 1:
            for possible_duplicate in loc_possible_duplicate_list:
                if name in possible_duplicate:
                    loc_possible_duplicate_list.remove(possible_duplicate)

    for definitive_duplicate in per_possible_duplicate_list:
        for entity in image_list[image]:
            if entity["name"] in definitive_duplicate and entity["type"] == "PER":
                if len(definitive_duplicate) < 3:
                    definitive_duplicate.append(entity["frequency"])
                else:
                    definitive_duplicate[2] += entity["frequency"]

    for definitive_duplicate in loc_possible_duplicate_list:
        for entity in image_list[image]:
            if entity["name"] in definitive_duplicate and entity["type"] == "LOC":
                if len(definitive_duplicate) < 3:
                    definitive_duplicate.append(entity["frequency"])
                else:
                    definitive_duplicate[2] += entity["frequency"]

    per_dict_list = [entity for entity in image_list[image] if (entity["type"] == "PER")]
    loc_dict_list = [entity for entity in image_list[image] if (entity["type"] == "LOC")]

    for definitive_duplicate in per_possible_duplicate_list:
        per_dict_list = [entity for entity in per_dict_list if (entity["name"] not in definitive_duplicate[:2])]
        if len(definitive_duplicate[0]) > len(definitive_duplicate[1]):
            per_dict_list.append({"name": definitive_duplicate[0], "type": "PER", "frequency": definitive_duplicate[2]})
        else:
            per_dict_list.append({"name": definitive_duplicate[1], "type": "PER", "frequency": definitive_duplicate[2]})

    for definitive_duplicate in loc_possible_duplicate_list:
        loc_dict_list = [entity for entity in loc_dict_list if (entity["name"] not in definitive_duplicate[:2])]
        if len(definitive_duplicate[0]) > len(definitive_duplicate[1]):
            loc_dict_list.append({"name": definitive_duplicate[0], "type": "LOC", "frequency": definitive_duplicate[2]})
        else:
            loc_dict_list.append({"name": definitive_duplicate[1], "type": "LOC", "frequency": definitive_duplicate[2]})

    image_list[image] = per_dict_list + loc_dict_list


# Vornamen Nachname -> Nachname, Vornamen
for image in image_list:
    for entity in image_list[image]:
        if entity["type"] == "PER":
            entity_name_split = entity["name"].split()
            if len(entity_name_split) > 1:
                entity_new_name = entity_name_split[-1] + ","

                for particial_name in entity_name_split[:-1]:
                    entity_new_name += " " + particial_name

                entity["name"] = entity_new_name


# ID und Label
rel_id_list = [
    "placeOfBirth",
    "placeOfDeath",
    "placeOfExile",
    "placeOfActivity",
    "familialRelationship",
    "professionalRelationship",
    "aquaintanceshipOrFriendship",
    "relatedPerson",
    "relatedPlaceOrGeographicName",
    "place",
    "characteristicPlace",
    "hierarchicalSuperiorOfPlaceOrGeographicName",
    "buildingOwner",
    "architect",
    "startingOrFinalPointOfADistance"
]

# Freitext
rel_text_list = [
    "definition",
    "biographicalOrHistoricalInformation"
]


for image in image_list:
    for entity in image_list[image]:
        search_url = "https://lobid.org/gnd/search?q="

        # erstmal nur Felder für Namen durchsuchen
        search_url += urllib.parse.quote_plus("preferredName:")
        search_url += "\"" + urllib.parse.quote_plus(entity["name"]) + "\""  # exakte Suche

        search_url += "+OR+"

        search_url += urllib.parse.quote_plus("variantName:")
        search_url += "\"" + urllib.parse.quote_plus(entity["name"]) + "\""

        # Typ
        search_url += "&filter=" + urllib.parse.quote_plus("type:")
        if entity["type"] == "PER":
            search_url += "DifferentiatedPerson"
        else:
            search_url += "PlaceOrGeographicName"

        # Menge und Ausgabeformat
        search_url += "&size=1000&format=json"

        # hier weitermachen

        req = urllib.request.Request(search_url)
        with urllib.request.urlopen(req) as response:
            json_response = response.read()
        json_response = json_response.decode('utf-8')
        json_response = json.loads(json_response)

        if json_response["totalItems"] < 1:
            entity["possibleGndId"] = [] # mit anderen Einstellungen wiederholen
        else: # hier fehlt noch Schleife bei mehr als 1000 Treffern
            entity["possibleGndId"] = []
            for gnd_entity in json_response["member"]:

                # jeder Treffer als Liste anlegen
                possible_gnd_id_list = []

                # 1. Element: Identifier als String
                possible_gnd_id_list.append(gnd_entity["gndIdentifier"])

                gnd_id_relation_list = []

                # 2. Element: Beziehungen zu anderen Identifiern als Strings in Liste
                for rel_field in rel_id_list:
                    try:
                        for relation in gnd_entity[rel_field]:
                            gnd_id_relation_list.append(relation["id"][22:])
                    except KeyError:
                        continue

                possible_gnd_id_list.append(gnd_id_relation_list)

                gnd_text_relation_list = []

                # 3. Element: Freitext-Beschreibungen als Strings in Liste
                for rel_field in rel_text_list:
                    try:
                        for information in gnd_entity[rel_field]:
                            gnd_text_relation_list.append(information)
                    except KeyError:
                        continue

                possible_gnd_id_list.append(gnd_text_relation_list)

                entity["possibleGndId"].append(possible_gnd_id_list)


with open("./gnd_ids_relation.json", mode="w+", encoding="utf-8") as file:
    json.dump([image_list], file)
