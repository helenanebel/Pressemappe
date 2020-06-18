import json
from urllib import request, parse
from math import ceil


# jeweils 1000 Treffer seitenweise abfragen

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


# Beispielname
name = "Robert Koch"


# Anfrage für API bauen

url = "https://lobid.org/gnd/search?q="

for counter, part in enumerate(name.split()):

    url += parse.quote_plus("(preferredName:" + part) + "+OR+"
    url += parse.quote_plus("variantName:" + part + ")")

    if counter != (len(name.split()) - 1):
        url += "+AND+"

url += "&filter=" + parse.quote_plus("type:")
url += "DifferentiatedPerson"
url += "&size=1000&format=json"

print(url)