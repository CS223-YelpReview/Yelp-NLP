import ujson
from textblob import TextBlob
import matplotlib.pyplot as mplot
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords

testSentences = []

def outputReviewsCSV(jsonFile, businessId):
    currentData = []
    with open(jsonFile,'rb') as jsonFile:
        reviewCnt = 0
        for line in jsonFile:
            json_data = ujson.loads(line)
            reviewCnt +=1
            print reviewCnt
            filtered_word_list = []
            word_list = json_data['text'].lower().split()
            for word in word_list: # iterate over word_list
                if word not in stopwords.words('english'): 
                    filtered_word_list.append(word)
            refined_text = " ".join(filtered_word_list)
            if json_data['business_id'] in businessId and reviewCnt < 80000 :
                      
                if (int(json_data['stars']) == 1):
                    tupl = (refined_text,'neg')
                    currentData.append(tupl)
                elif(int(json_data['stars']) == 5):
                    tupl = (refined_text,'pos')
                    currentData.append(tupl)
            elif reviewCnt < 80500:
                tupl = (refined_text,json_data['stars'])
                testSentences.append(tupl)
            else:
                break
    return currentData

def appendDataToCSV(jsonFileToRead):
    with open(jsonFileToRead, 'rb') as jsonFile:
        currentData = []
        for line in jsonFile:
            json_data = ujson.loads(line)
            category = ''.join(json_data['categories'])
            if "food" in category.lower():
                currentData.append(json_data['business_id'])
    return currentData

def testSentence(sentence,classifier):
    filtered_word_list = [word for word in sentence.lower().split() if word not in stopwords.words('english')]
    refinedText = " ".join(filtered_word_list)
    blob = TextBlob(refinedText, classifier=classifier)
    return blob.classify()

businessId = appendDataToCSV('yelp_academic_dataset_business.json')
print len(businessId)
businessId = businessId[:200]
train = outputReviewsCSV('yelp_academic_dataset_review.json',businessId)
 
print train
cl = NaiveBayesClassifier(train)

print cl.show_informative_features(20) 
#testing
finalOutput = []

for (sentence,rating) in testSentences:
    clOutput = testSentence(sentence,cl)
    #color = 'r' if (clOutput == 'pos') else 'g' 
    #finalOutput.append((clOutput,rating,color))
    print " ----" + str(rating) + "----" + clOutput

#plot
#mplot.plot([rating for (result,rating,color) in finalOutput], len(finalOutput),'r')
#mplot.show()