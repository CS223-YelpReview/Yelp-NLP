import json
import nltk

def outputReviewsCSV(jsonFile, businessId):
    currentData = []
    with open(jsonFile,'rb') as jsonFile:
        for line in jsonFile:
            json_data = json.loads(line)
            if json_data['business_id'] in businessId:
                data = []
                if (int(json_data['stars']) == 1):
                    data.append(json_data['text'])
                    data.append('neg')
                    tupl = tuple(data)
                    currentData.append(tupl)
                elif(int(json_data['stars']) == 5):
                    data.append(json_data['text'])
                    data.append('pos')
                    tupl = tuple(data)
                    currentData.append(tupl)
    jsonFile.close()
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
businessId = businessId[:10]
train = outputReviewsCSV('F:\Courses\Bio Informatics\Project\dataset\yelp_academic_dataset_review.json',businessId)
 
print train
cl = nltk.classify.NaiveBayesClassifier.train(train)

data = []
data.append("Their burgers are amazing")
data.append("I don't like their pizza.")
test = tuple(data)
print cl.classify("Their burgers are amazing") 
print cl.classify("I don't like their pizza.") 