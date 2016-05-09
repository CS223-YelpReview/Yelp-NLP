import json
from textblob.classifiers import NaiveBayesClassifier

def outputReviewsCSV(jsonFile, businessId):
    currentData = []
    negReview = 0
    posReview = 0
    with open(jsonFile,'rb') as jsonFile:
        for line in jsonFile:
            json_data = json.loads(line)
            if json_data['business_id'] in businessId:
                data = []
                if (int(json_data['stars']) == 1):
                    print json_data['text']
                    data.append(json_data['text'])
                    data.append('neg')
                    tupl = tuple(data)
                    currentData.append(tupl)
                    negReview = negReview +1
                elif(int(json_data['stars']) == 5):
                    data.append(json_data['text'])
                    data.append('pos')
                    tupl = tuple(data)
                    currentData.append(tupl)
                    posReview = posReview +1
    jsonFile.close()
    print "Neg: ",negReview," Pos: ",posReview
    return currentData

def appendDataToCSV(jsonFileToRead):
    with open(jsonFileToRead, 'rb') as jsonFile:
        currentData = []
        for line in jsonFile:
            json_data = json.loads(line)
            category = ''.join(json_data['categories'])
            if "food" in category.lower():
                currentData.append(json_data['business_id'])
    return currentData
  
businessId = appendDataToCSV('F:\Courses\Bio Informatics\Project\dataset\yelp_academic_dataset_business.json')
print len(businessId)
businessId = businessId[:1000]
train = outputReviewsCSV('F:\Courses\Bio Informatics\Project\dataset\yelp_academic_dataset_review.json',businessId)
 
#print train
cl = NaiveBayesClassifier(train)

print cl.classify("Their burgers are amazing") 
print cl.classify("Pizza is very bad.") 