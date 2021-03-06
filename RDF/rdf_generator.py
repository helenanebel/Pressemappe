import os
import json
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, DCTERMS

def make_rdf():
    with open("RDF/journals_published_in.json", mode="r") as file:
        pubs = json.load(file)

    # Liste aller Entitäten
    total = []
    for image_name in os.listdir("GND/article_entities"):
        with open("GND/article_entities/" + image_name, "r") as file:
            image = json.load(file)
        for entity in image:
            if "gnd" in entity:
                if entity["gnd"]["identifier"] not in total:
                    total.append(entity["gnd"]["identifier"])

    graph = Graph()

    GND = Namespace("https://d-nb.info/standards/elementset/gnd#")
    graph.bind("gndo", GND)
    graph.bind("dcterms", DCTERMS)

    for image_name in os.listdir("GND/article_entities"):
        with open("GND/article_entities/" + image_name, "r") as file:
            image = json.load(file)

        # Link zu Dokument
        document_url = "http://webopac.hwwa.de/PresseMappe20Bookmark/PM20bm.cfm?mid=P" + image_name[7:13] + "&dn=" + str(int(image_name[20:25]))
        graph.add((URIRef(document_url), RDF.type, DCTERMS.BibliographicResource))

        image_name = image_name.replace(".json", ".JPG")

        if image_name in pubs:
            if pubs[image_name] != "":
                publication_url = pubs[image_name]["url"]
                graph.add((URIRef(publication_url), RDF.type, DCTERMS.BibliographicResource))
                graph.add((URIRef(publication_url), DCTERMS.title, Literal(pubs[image_name]["title"])))

                graph.add((URIRef(publication_url), DCTERMS.hasPart, URIRef(document_url)))
                graph.add((URIRef(document_url), DCTERMS.isPartOf, URIRef(publication_url)))

        for entity in image:
            if "gnd" in entity:
                entity_id = entity["gnd"]["identifier"]

                if entity["type"] == "PER":
                    graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), RDF.type, GND.DifferentiatedPerson))
                else:
                    graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), RDF.type, GND.PlaceOrGeographicName))

                graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), GND.preferredName, Literal(entity["gnd"]["names"][0])))

                graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), DCTERMS.isReferencedBy, URIRef(document_url)))
                graph.add((URIRef(document_url), DCTERMS.references, URIRef("https://d-nb.info/gnd/" + entity_id)))

                for relation_id in entity["gnd"]["relations"]:
                    if relation_id in total and relation_id != entity_id:
                        graph.add((URIRef("https://d-nb.info/gnd/" + entity_id), DCTERMS.relation, URIRef("https://d-nb.info/gnd/" + relation_id)))
                        graph.add((URIRef("https://d-nb.info/gnd/" + relation_id), DCTERMS.relation, URIRef("https://d-nb.info/gnd/" + entity_id)))

    graph.serialize(format="xml", destination="entities.rdf", encoding="utf-8")
    graph.serialize(format="turtle", destination="entities.ttl", encoding="utf-8")


if __name__ == '__main__':
    make_rdf()