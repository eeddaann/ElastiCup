from elasticsearch import Elasticsearch
import logging
import requests
from retrying import retry
import datetime
import math

MATCH_FIELDS = ('location',
                'status',
                'weather',
                'attendance',
                'stage_name',
                'home_team_country',
                'away_team_country',
                'datetime',
                'winner')

def transform_match(raw_match):
    match = {k: raw_match[k] for k in MATCH_FIELDS} # include only relevant fields
    # add human friendly match name
    match['match_name'] = "%s, %s vs %s" % (match['stage_name'], match['home_team_country'], match['away_team_country'])
    return match

def transform_team_stats(match,team):
    team_stats = match[team+"_team_statistics"]
    team_stats['match_name'] = "%s, %s vs %s" % (match['stage_name'], match['home_team_country'], match['away_team_country'])
    team_stats['goals'] = match[team+'_team']['goals']
    team_stats['penalties'] = match[team+'_team']['penalties']
    team_stats['is_winner'] = match['winner'] == match[team+'_team']['country']
    team_stats.pop('starting_eleven', None)
    team_stats.pop('substitutes', None)
    return team_stats

def transform_team_events(es,match,team):
    for event in match[team+"_team_events"]:
        event['match_name'] = "%s, %s vs %s" % (match['stage_name'], match['home_team_country'], match['away_team_country'])
        event['country'] = match[team+'_team_country']
        if '+' in event['time']:
             event['time'] =generate_timestamp(90+int(event['time'][-2]))
        else:
            event['time']=generate_timestamp(int(event['time'][:-1]))
        event.pop('id', None)
        es.index(index="events",doc_type="event", body=event)
    return

def generate_timestamp(time):
    h = str(math.floor(time/60))
    if time%60 >= 10:
        m = str(time%60)
    else:
        m = str(0)+str(time%60)
    return "2018-01-01T0"+h+":"+m+":00Z"

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def wait_for_elasticsearch():
    try:
        es = Elasticsearch(['http://elasticsearch:9200/'],timeout=600) # based on docker's network
        es.cluster.health(wait_for_status='yellow')
        return es
    except:
        logging.warn("failed to connect to elasticsearch retrying to connect")
        raise Exception("failed to connect to elasticsearch")

es = wait_for_elasticsearch()
logging.info("connected successfully to elasticsearch")
r = requests.get('https://worldcup.sfg.io/matches') # download world cup matches data
if r.status_code is 200:
   logging.info('data downloaded successfully') # verifies that the data downloaded  
for match in r.json(): # iterates over the matches
    if match['status'] == "completed":
        es.index(index="matches",doc_type="match", body=transform_match(match)) # uploads each match as document
        es.index(index="team-stats",doc_type="team-statistics", body=transform_team_stats(match,"home"))
        es.index(index="team-stats",doc_type="team-statistics", body=transform_team_stats(match,"away"))
        transform_team_events(es,match,"home")
        transform_team_events(es,match,"away")
logging.info('data loaded successfully to elasticsearch')