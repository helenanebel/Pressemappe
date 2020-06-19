import json
import os
from urllib import request, parse
from math import ceil


with open("entities.json", mode="r", encoding="utf-8") as file:
    image_list = json.load(file)[0]

# erstmal nur direkte Beziehungen ermitteln, daher nur Domain/Range spezifisch
with open("relations.json", mode="r", encoding="utf-8") as file:
    relations = json.load(file)

with open("geo_codes.json", mode="r", encoding="utf-8") as file:
    geo_codes = json.load(file)

if "image_member" not in os.listdir():
    os.mkdir("image_member")

def build_url(name, type):
    url = "https://lobid.org/gnd/search?q="

    for counter, part in enumerate(name.split()):
        url += parse.quote_plus("(preferredName:" + part) + "+OR+"
        url += parse.quote_plus("variantName:" + part + ")")

        if counter != (len(name.split()) - 1):
            url += "+AND+"

    # Individualisierte Person bzw. Geografikum
    url += "&filter=" + parse.quote_plus("type:")
    if type == "PER":
        url += "DifferentiatedPerson"
    else:
        url += "PlaceOrGeographicName"
    url += "&size=1000&format=json"

    return url


def get_member(url):
    req = request.Request(url)
    with request.urlopen(req) as response:
        json_response = response.read()
    json_response = json_response.decode("utf-8")
    json_response = json.loads(json_response)

    count = json_response["totalItems"]
    start = 0
    member = []

    for c in range(ceil(count / 1000)):
        url += "&from=" + str(start)
        req = request.Request(url)
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
        try:
            for name in member["variantName"]:
                gnd["names"].append(name)
        except KeyError:
            continue

        for field in relations["relation"]:
            try:
                for relation in member[field]:
                    gnd["relations"].append(relation["id"][22:])
            except KeyError:
                continue

        try:
            for code in member["geographicAreaCode"]:
                code = geo_codes[code["id"][59:]]
                if code not in gnd["relations"] and code != gnd["identifier"]:
                    gnd["relations"].append(code)
        except KeyError:
            continue

        for field in relations["descriptions"]:
            try:
                for text in member[field]:
                    gnd["descriptions"].append(text)
            except KeyError:
                continue

        member_list_slim.append(gnd)
    return member_list_slim


for image in image_list:
    for entity in image_list[image]:
        url = build_url(entity["name"], entity["type"])

        member_list = get_member(url)

        member_list = get_data(member_list)

        entity["possible_gnd"] = member_list

    with open("image_member/" + image.replace(".JPG", ".json"), "w+") as file:
        json.dump(image_list[image], file, indent=4)