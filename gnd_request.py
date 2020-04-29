import urllib
from urllib import request
import json
import time

entities = ['London']


found_gnd_items = 0
search_not_successfull = []
missing_gnd_ids = {}
ids_processed = 0
for entity in entities:
    success = False
    #hier mal überprüfen, was da überhaupt in den Daten steht und was dann da rauskommt.
    search_url = "https://lobid.org/gnd/search?q=" + entity
    trials = 0
    found=False
    while success!=True:
        if trials >= 10:
            search_not_successfull.append(entity)
            break
        try:
            req = urllib.request.Request(search_url)
            with urllib.request.urlopen(req) as response:
                json_response=response.read()
            json_response=json_response.decode('utf-8')
            json_response=json.loads(json_response)
            if json_response['totalItems']>0:
                id = json_response['member'][0]['id']
                found_gnd_items +=1
                found=True
                print(json_response)
            time.sleep(1)
            success=True
        except Exception as e:
            print('Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e)))
            print('gescheitert:', search_url)
            print(entity, entities[entity])
            time.sleep(7)
    ids_processed +=1