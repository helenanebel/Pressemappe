import json
import os

if "image_entities" not in os.listdir():
    os.mkdir("image_entities")

for image_name in os.listdir("image_member"):
    with open("image_member/" + image_name, "r") as file:
        image = json.load(file)

    for entity in image:

        # Genaue Übereinstimmung bei Geografika
        if entity["type"] == "LOC":
            for match in entity["possible_gnd"]:
                if match["names"].count(entity["name"]) > 0:
                    entity["gnd"] = [match]
                    entity.pop("possible_gnd", None)
                else:
                    continue

        

    with open("image_member/../image_entities/" + image_name, "w+") as file:
        json.dump(image, file, indent=4)
