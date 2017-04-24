#!/usr/bin/env python3

""" Simple little Typeform-to-CSV parser
1) insert your Typeform API key into apikey field ( Line 25 )
2) Run Script

Notes:
- each form will generate a csv file
- csv files are saved into the directory where this script resides
- csv files will be saved as <<form_name>>_<<YYMMDD>>_<<HHMMSS>>.csv
"""
__author__      = "Eva Yu"
__copyright__   = "Copyright 2017, Eva Yu"
__license__     = "MIT"
__version__     = "0.0.1"

import sys
import csv
import json
import requests
import time

typeformAPI = 'https://api.typeform.com/v1'

# insert API key here!
apikey = ''

# make sure API Key is here
if not apikey:
    sys.stderr.write('Oops! We could not detect an API Key.\n')
    sys.stderr.write('Please insert an API key into line 25.\n')
    exit()

# request values
payload = {}
payload['key'] = apikey
reqErrMsg = 'Oops! We encountered an http error: {}\n'

#getForms url formatting
getForms = '{}/forms'.format(typeformAPI)

#first request gets all the forms as json
forms = requests.get(getForms, params = payload)

# check status
if forms.status_code != 200:
    sys.stderr.write (reqErrMsg.format(forms.status_code))
    exit()

# add submitted forms to payload
payload['completed'] = 'true'

# iterate through all the forms found
for form in forms.json():
    fid = form['id']
    formName = form['name']

    # format getFormData request
    getFormData =  '{}/form/{}'.format(typeformAPI, fid)

    # get the form data
    data = requests.get(getFormData, params = payload)

    # check status
    if data.status_code != 200:
        sys.stderr.write (reqErrMsg.format(data.status_code))
        exit()

    # store all question fields
    fields = []
    for q in data.json()['questions']:
        fields.append(q['id'])

    # store the data in the submissions
    NaN = 'NaN'
    answers = []
    for res in data.json()['responses']:
        current = {}
        for field in fields:
            answer = res['answers'].get(field)
            if answer == None:
                answer = NaN
            current[field] = answer
        answers.append(current)

    timestamp = time.strftime("%y%m%d_%H%M%S", time.gmtime())
    filename = '{}_{}.csv'.format(formName,timestamp)
    # open a csv file and write the data
    with open(filename, 'w') as csvfile:
         writer = csv.DictWriter(csvfile, fieldnames=fields)
         writer.writeheader()
         writer.writerows(answers)
