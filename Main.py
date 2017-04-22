#!/usr/bin/env python3
""" Simple little Typeform-to-CSV parser
1) insert your Typeform API key into apikey field
2) run script

Notes:
- csv files are saved into the directory where this script resides
- csv files will be saved as <<form_name>>_<<YY-MM-DD>>_<<HH:MM:SS>>.csv
"""
__author__      = "Eva Yu"
__copyright__   = "Copyright 2017, Eva Yu"
__license__     = "MIT"
__version__     = "1.0.0"

import csv
import json
import requests
import time

typeformAPI = 'https://api.typeform.com/v1/form/'

#insert API key here!
apikey = ''
fid = ''

#name of form
data = requests.get(typeformAPI + fid +'?key=' + apikey + '&completed=true').json()

#check status
if data['http_status'] != 200:
    eprint ( 'Oops! We encoutnered an http error: ' + data['http_status'])
    exit()

#store all question fields
fields = []
for q in data['questions']:
    fields.append(q['id'])

#store the data in the submissions
NaN = 'NaN'
answers = []
for res in data['responses']:
    current = {}
    for field in fields:
        answer = res['answers'].get(field)
        if answer == None:
            answer = NaN
        current[field] = answer
    answers.append(current)

#open a csv file and write the data
name = 'Keboola Test Dungeon'
timestamp = time.strftime("%y-%m-%d_%H:%M:%S", time.gmtime())
with open(name + '_'+ timestamp + '.csv', 'w') as csvfile:
     writer = csv.DictWriter(csvfile, fieldnames=fields)
     writer.writeheader()
     writer.writerows(answers)
