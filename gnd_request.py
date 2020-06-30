import json
import os
from urllib import request, parse
from math import ceil
from nltk.corpus import stopwords


with open("entities.json", mode="r", encoding="utf-8") as file:
    image_list = json.load(file)[0]

with open("relations.json", mode="r", encoding="utf-8") as file:
    relations = json.load(file)

with open("geo_codes.json", mode="r", encoding="utf-8") as file:
    geo_codes = json.load(file)

with open("stopword_language.json", mode="r", encoding="utf-8") as file:
    language_codes = json.load(file)

if "image_member" not in os.listdir():
    os.mkdir("image_member")

def build_url(name, type):
    url = "https://lobid.org/gnd/search?q="

    for counter, part in enumerate(name.split()):
        url += parse.quote_plus("(preferredName:" + part) + "+OR+"
        url += parse.quote_plus("variantName:" + part + ")")

        if counter != (len(name.split()) - 1):
            url += "+AND+"

    # Person (ohne Nicht-Individualisierte Person) bzw. Geografikum
    if type == "PER":
        url += "+AND+_exists_" + parse.quote_plus(":") + "preferredNameEntityForThePerson"
        url += "&filter="
        url += parse.quote_plus("type:") + "Person+AND+NOT+"
        url += parse.quote_plus("type:") + "UndifferentiatedPerson"
        url += parse.quote_plus("")
    else:
        url += "&filter="
        url += "PlaceOrGeographicName"
    url += "&size=1000&format=json"

    return url


# nur bis 10.000 Treffer erfassen
def get_member(url):
    req = request.Request(url)
    with request.urlopen(req) as response:
        json_response = response.read()
    json_response = json_response.decode("utf-8")
    json_response = json.loads(json_response)
    count = json_response["totalItems"]
    start = 0
    member = []
    if count in range(1,10000):
        for c in range(ceil(count / 1000)):
            loop_url = url + "&from=" + str(start)
            req = request.Request(loop_url)
            with request.urlopen(req) as response:
                json_response = response.read()
            json_response = json_response.decode("utf-8")
            json_response = json.loads(json_response)
            member.extend(json_response["member"])
            start += 1000
    return member


def get_data(member_list):
    member_list_slim = []
    for member in member_list:
        gnd = {"identifier": member["gndIdentifier"], "names": [], "relations": [], "descriptions": []}
        gnd["names"].append(member["preferredName"])

        if "variantName" in member:
            for name in member["variantName"]:
                gnd["names"].append(name)

        for field in relations["relation"]:
            if field in member:
                for relation in member[field]:
                    gnd["relations"].append(relation["id"][22:])

        if "geographicAreaCode" in member:
            for code in member["geographicAreaCode"]:
                code = code["id"][59:]
                if code in geo_codes and code not in gnd["relations"] and code != gnd["identifier"]:
                    gnd["relations"].append(geo_codes[code])

        for field in relations["descriptions"]:
            if field in member:
                for text in member[field]:
                    gnd["descriptions"].append(text)
        member_list_slim.append(gnd)
    return member_list_slim


for image in image_list:
    for entity in image_list[image]:
        url = build_url(entity["name"], entity["type"])

        member_list = get_member(url)

        # Stoppwörter filtern
        if not member_list:
            if entity["language"] in language_codes:
                exclude = set(stopwords.words(language_codes[entity["language"]]))
                name = " ".join([part for part in entity["name"].split() if part.lower() not in exclude])
                url = build_url(name, entity["type"])
                member_list = get_member(url)

        # unscharfe Suche für jedes Zeichen
        if not member_list:
            for i, part in enumerate(entity["name"].split()):
                namelist = entity["name"].split()
                for index, char in enumerate(part):
                    word = list(part)
                    word[index] = "*" # alternativ ?
                    word = "".join(word)
                    namelist[i] = word
                    name = " ".join(namelist)
                    url = build_url(name, entity["type"])
                    for member in get_member(url):
                        if member not in member_list:
                            member_list.append(member)

        member_list = get_data(member_list)
        entity["possible_gnd"] = member_list
        entity["gnd"] = []

    with open("image_member/" + image.replace(".JPG", ".json"), "w+") as file:
        json.dump(image_list[image], file, indent=4)