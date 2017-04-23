#!/usr/bin/env python3
""" Simple little Typeform-to-CSV parser
1) insert your Typeform API key into apikey field
2) run script

Notes:
- each form will generate a csv file
- csv files are saved into the directory where this script resides
- csv files will be saved as <<form_name>>_<<YYMMDD>>_<<HHMMSS>>.csv
"""
__author__      = "Eva Yu"
__copyright__   = "Copyright 2017, Eva Yu"
__license__     = "MIT"
__version__     = "0.0.1"

import csv
import json
import requests
import time

typeformAPI = 'https://api.typeform.com/v1'

# insert API key here!
apikey = ''

payload = {}
getForms = '{}/forms'.format(typeformAPI)
payload['key'] = apikey
forms = requests.get(getForms, params = payload).json()

# add data to next payload
payload['completed'] = 'true'
for form in forms:
    #form id
    fid = form['id']
    formName = form['name']

    # make a request for submitted form data
    getFormData =  '{}/form/{}'.format(typeformAPI, fid)

    # get the form data as json
    data = requests.get(getFormData, params = payload).json()

    # check status
    if data['http_status'] != 200:
        eprint ( 'Oops! We encoutnered an http error: ' + data['http_status'])
        exit()

    # store all question fields
    fields = []
    for q in data['questions']:
        fields.append(q['id'])

    # store the data in the submissions
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

    # open a csv file and write the data
    timestamp = time.strftime("%y%m%d_%H%M%S", time.gmtime())
    filename = '{}_{}.csv'.format(formName,timestamp)
    with open(filename, 'w') as csvfile:
         writer = csv.DictWriter(csvfile, fieldnames=fields)
         writer.writeheader()
         writer.writerows(answers)
