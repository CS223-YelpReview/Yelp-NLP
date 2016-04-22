import nltk as n
from nltk.sentiment import SentimentAnalyzer as sa
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import json
data=[]
with open ('yelp_academic_dataset_review.json')as dataf:
    for line in dataf:
        data.append(json.loads(line))

#sentim_analyzer = sa()
sid=SentimentIntensityAnalyzer()
           
for a in data:
    print a['text']
    ss = sid.polarity_scores(a['text'])
    for k in sorted(ss):
        print('{0}: {1}'.format(k, ss[k]))
    print()
   

#all_words_neg = sentim_analyzer.all_words(b)
#print b