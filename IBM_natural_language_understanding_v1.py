from __future__ import print_function
import json
import pandas as pd
import re
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

#Instantiate NLU Object with your Credentials
service = NaturalLanguageUnderstandingV1(
     version='2018-03-16',
     #url is optional, and defaults to the URL below. Use the correct URL for your region.
     url='https://gateway.watsonplatform.net/natural-language-understanding/api',
     #change here to your apikey
     iam_apikey='apikey')

#read data
df = pd.read_csv("ads.csv")

#remove none value from text data
df = df[df["Ad_Text "] != 'none']

#make a test copy
test_data = df.head(50).copy()


for index, ad_text in df['Ad_Text '].iteritems():
        print(index)
        response = service.analyze(
            text=ad_text,
            features=Features(entities=EntitiesOptions(),
                              keywords=KeywordsOptions()),
            language='en'
        ).get_result()
        # text_characters
        text_characters = re.sub('["''{},:]', '', json.dumps(response['usage']['text_characters']))
        df.at[index, "text_characters"] = int(text_characters)
        #some text are too small to have 2 keywords and 3 entities, so using aviod error here
        try:
                # keyword
                keyword_1 = re.sub('["{},:]', '', json.dumps(response['keywords'][0]["text"]))
                relevance_1 = re.sub('["{},:]', '', json.dumps(response['keywords'][0]["relevance"]))
                keyword_1 = keyword_1.replace("'", " ").replace("'", " ").replace("'", "")
                test_data.at[index, str(keyword_1)] = float(relevance_1)
                keyword_2 = re.sub('["{},:]', '', json.dumps(response['keywords'][1]["text"]))
                relevance_2 = re.sub('["{},:]', '', json.dumps(response['keywords'][1]["relevance"]))
                keyword_2 = keyword_2.replace("'", " ").replace("'", " ").replace("'", "")
                #save keyword and score to dataframe
                test_data.at[index, str(keyword_2)] = float(relevance_2)
                # entities
                entity_1 = re.sub('["{},:]', '', json.dumps(response['entities'][0]["type"]))
                entity_relevance_1 = re.sub('["{},:]', '', json.dumps(response['entities'][0]["relevance"]))
                entity_2 = re.sub('["{},:]', '', json.dumps(response['entities'][1]["type"]))
                entity_relevance_2 = re.sub('["{},:]', '', json.dumps(response['entities'][1]["relevance"]))
                entity_3 = re.sub('["{},:]', '', json.dumps(response['entities'][2]["type"]))
                entity_relevance_3 = re.sub('["{},:]', '', json.dumps(response['entities'][2]["relevance"]))
                #save entity and score to dataframe
                test_data.at[index, str(entity_1)] = float(entity_relevance_1)
                test_data.at[index, str(entity_2)] = float(entity_relevance_2)
                test_data.at[index, str(entity_3)] = float(entity_relevance_3)
        except IndexError or ValueError:
                continue


test_data.to_csv('IBM_test_data.csv')
