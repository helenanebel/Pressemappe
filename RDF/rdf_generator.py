import os
import json
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, DCTERMS


total = []
for image_name in os.listdir("../GND/image_entities"):
    with open("../GND/image_entities/" + image_name, "r") as file:
        image = json.load(file)
    for entity in image:
        if "gnd" in entity:
            if entity["gnd"]["identifier"] not in total:
                total.append(entity["gnd"]["identifier"])

graph = Graph()

GND = Namespace("https://d-nb.info/standards/elementset/gnd#")
graph.bind("gndo", GND)
graph.bind("dcterms", DCTERMS)

for image_name in os.listdir("../GND/image_entities"):
    with open("../GND/image_entities/" + image_name, "r") as file:
        image = json.load(file)

    image_name = image_name.replace(".json", "")
    url = "http://webopac.hwwa.de/DigiPerson/P/" + image_name.replace("_", "/", 5) + ".JPG"

    graph.add((URIRef(url), RDF.type, DCTERMS.BibliographicResource))


    for entity in image:
        if "gnd" in entity:
            entity_id = entity["gnd"]["identifier"]

            if entity["type"] == "PER":
                graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), RDF.type, GND.DifferentiatedPerson))
            else:
                graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), RDF.type, GND.PlaceOrGeographicName))

            graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), GND.preferredName, Literal(entity["gnd"]["names"][0])))

            graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), DCTERMS.isReferencedBy, URIRef(url)))
            graph.add((URIRef(url), DCTERMS.references, URIRef("https://d-nb.info/gnd/" + entity_id)))

            for relation_id in entity["gnd"]["relations"]:
                if relation_id in total and relation_id != entity_id:
                    graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), DCTERMS.relation, URIRef("https://d-nb.info/gnd/" + relation_id)))
                    graph.add((URIRef("https://d-nb.info/gnd/" + relation_id), DCTERMS.relation, URIRef("https://d-nb.info/gnd/" + entity_id)))

graph.serialize(format="xml", destination="entities.rdf", encoding="utf-8")
graph.serialize(format="turtle", destination="entities.ttl", encoding="utf-8")
