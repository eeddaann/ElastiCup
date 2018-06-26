from elasticsearch import Elasticsearch
import logging
import requests

es = Elasticsearch(['http://elasticsearch:9200/']) # based on docker's network

r = requests.get('https://worldcup.sfg.io/matches') # download world cup matches data
if r.status_code is 200:
   logging.info('data downloaded successfully') # verifies that the data downloaded  
for match in r.json(): # iterates over the matches
    res = es.index(index="worldcup-matches", doc_type='match', body=match) # uploads each match as document