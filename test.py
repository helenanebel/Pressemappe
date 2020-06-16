name = "Robert Koch"
import json
import urllib
from urllib import request, parse
from math import ceil
import gnd_relations

# jeweils 1000 Treffer seitenweise aus lobid abfragen
def get_member_list(url):
    req = request.Request(url)
    with request.urlopen(req) as response:
        json_response = response.read()
    json_response = json_response.decode("utf-8")
    json_response = json.loads(json_response)
    count = json_response["totalItems"]
    start = 0
    member = []
    for i in range(ceil(count / 1000)):
        url += "&from=" + str(start)
        req = request.Request(url)
        with request.urlopen(req) as response:
            json_response = response.read()
        json_response = json_response.decode("utf-8")
        json_response = json.loads(json_response)
        member.extend(json_response["member"])
        start += 1000
    return member


# Teil des Namens muss in preferredName oder variantName vorkommen
def clean_member_list(member_list, nameX):
    cleaned_member_list = []
    for member in member_list:

        names = []
        if "preferredName" in member:
            names.append(member["preferredName"])
            if "variantName" in member:
                for name in member["variantName"]:
                    names.append(name)
            print(nameX, " : ", names)
            for n in names:
                if nameX in n:
                    #print(nameX + " ist in " + n)
                    cleaned_member_list.append(member)
                    break

    return cleaned_member_list

nameXSplit = name.split()

possible_member_list = []

parts = []

# nur wenn länder als 1 string
for nameXPart in nameXSplit:


    url = "https://lobid.org/gnd/search?q="
    url += urllib.parse.quote_plus("preferredName:" + nameXPart) + "+OR+"
    url += urllib.parse.quote_plus("variantName:" + nameXPart)
    url += "&filter=" + urllib.parse.quote_plus("type:")
    url += "DifferentiatedPerson"
    url += "&size=1000&format=json"

    print(url)

    part_list = clean_member_list(get_member_list(url), nameXPart)

    part_list_clean = []

    for item in part_list:
        if "gndIdentifier" in item:
            if item["gndIdentifier"] not in part_list_clean:
                part_list_clean.append(item["gndIdentifier"])

    parts.append([nameXPart, part_list_clean])

# da jeder Teil im Namen sein muss, egal ob nur ersten prüfen

true_member = []

# hier evtl. Satzzeichen aus Parts entfernen

for gnd_id in parts[0][1]:
    gnd_id_counter = 1

    for part in parts[1:]:
        if gnd_id in part[1]:
            gnd_id_counter += 1
    if gnd_id_counter == len(nameXSplit):
        if gnd_id not in true_member:
            true_member.append(gnd_id)

with open("test.json", mode="w+", encoding="utf-8") as file:
    json.dump([{name: true_member}], file, indent=4)