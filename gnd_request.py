import json
import urllib
from urllib import request, parse

with open("./entities.json", mode="r", encoding="utf-8") as file:
    image_list = json.load(file)[0]

for image in image_list:
    for entity in image_list[image]:
        search_url = "https://lobid.org/gnd/search?q="

        # erstmal nur Felder für Namen durchsuchen
        search_url += urllib.parse.quote_plus("preferredName:")
        search_url += "\"" + urllib.parse.quote_plus(entity["name"]) + "\""  # exakte Suche

        search_url += "+OR+"

        search_url += urllib.parse.quote_plus("variantName:")
        search_url += urllib.parse.quote_plus(entity["name"])

        # Typ
        search_url += "&filter=" + urllib.parse.quote_plus("type:")
        if entity["type"] == "PER":
            search_url += "Person"
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
            entity["possibleGndId"] = []
            break
        elif json_response["totalItems"] < 1001:
            entity["possibleGndId"] = []
            for gnd_entity in json_response["member"]:
                entity["possibleGndId"].append(gnd_entity["gndIdentifier"])

with open("./entities.json", mode="w+", encoding="utf-8") as file:
    json.dump([image_list], file, indent=4)
