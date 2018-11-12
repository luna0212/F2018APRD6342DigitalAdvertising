from __future__ import print_function
from watson_developer_cloud import ToneAnalyzerV3
import pandas as pd
import json

#Instantiate TA Object with your Credentials
service = ToneAnalyzerV3(
     #url is optional, and defaults to the URL below. Use the correct URL for your region.
     url='https://gateway.watsonplatform.net/tone-analyzer/api',
     version='2017-09-21',
     iam_apikey='apikey')

#read data
data = pd.read_csv("/Users/pudin/Desktop/digital/project1/russian_dataset_with_datesplit_clean.csv")

#make a test copy
test_data = data.head(50).copy()

#get result
for index, review in data['Ad_Text '].iteritems():
    result = json.dumps(
            service.tone(
                tone_input=review,
                content_type="text/plain").get_result(),
            indent=2)
    for i in json.loads(result)['document_tone']['tones']:
        print(index, i['tone_name'], i['score'])
        #save tone and score to dataframe
        data.at[index, str(i['tone_name'])] = float(i['score'])


data.to_csv('test_data.csv')


