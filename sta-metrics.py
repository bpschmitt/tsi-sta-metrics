from random import *
import time
import json
import requests
import datetime

MEASUREMENTSAPI = "https://api.truesight.bmc.com/v1/measurements"
APIKEY = "<api key>"
EMAIL = "<email>"
APP_ID = "<app_id>"
TIMESTAMP = int(time.time())
HUMANTIME=datetime.datetime.fromtimestamp(TIMESTAMP).strftime('%Y-%m-%d %H:%M:%S')
CONFIGFILE="/path/to/json/config"

with open(CONFIGFILE) as datafile:
    data = json.load(datafile)

for sd in data['serviceDesks']:
    for name in sd:
        for stuff in sd[name]:
            for metric,values in stuff.iteritems():
                #print("service desk: %s - metric: %s - avg: %s - stdev: %s" % (name,metric,values[0]['avg'],values[0]['stdev']))
                measure = {
                    "source": name,
                    "metric": metric,
                    "measure": randint(values[0]['avg'] - values[0]['stdev'], values[0]['avg'] + values[0]['stdev']),
                    "timestamp": TIMESTAMP,
                    "metadata": {
                        "app_id": APP_ID
                    }
                }

                #print(json.dumps(measure,indent=4))

                try:
                    r = requests.post(MEASUREMENTSAPI, data=json.dumps(measure),
                                      headers={'Content-type': 'application/json'}, auth=(EMAIL, APIKEY))
                except requests.exceptions.RequestException as e:
                    print(e)
                    exit(1)
                else:
                    # print(json.dumps(chunk,indent=4))
                    print("TS: %s - Source: %s - Metric: %s - Measurements Response Code: %s - %s" % (HUMANTIME,name,metric,r.status_code, r.reason))
