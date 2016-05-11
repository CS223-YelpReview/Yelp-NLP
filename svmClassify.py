import ujson
from textblob.classifiers import NaiveBayesClassifier
import unicodedata
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report



def outputReviewsCSV(jsonFile, businessId):
    currentData = []
    with open(jsonFile,'rb') as jsonFile:
        for line in jsonFile:
            json_data = ujson.loads(line)
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
            json_data = ujson.loads(line)
            category = ''.join(json_data['categories'])
            if "food" in category.lower():
                currentData.append(json_data['business_id'])
    return currentData
    
    
    
def newClassifier(values,test_data):
    newList = []
    train_data = []
    train_labels = []
    test_labels = []
    for data in values:
        trainStr = unicodedata.normalize('NFKD', data[0]).encode('ascii','ignore')      #Sentences
        #print trainStr
        #print data[1]      #reviews, positive or negative
        word_list = trainStr.split();
        print word_list
        for word in word_list: # iterate over word_list
            newList.append(word.lower()) 
        print newList  
        filtered_word_list = newList[:] #make a copy of the word_list
        #print filtered_word_list
        for word in newList: # iterate over word_list
            if word in stopwords.words('english'): 
                filtered_word_list.remove(word)
        #print filtered_word_list
        #train_data.append(filtered_word_list[:])
        train_labels.append((data[1]))
        
    #print train_data
    #print train_labels     
            
    vectorizer = TfidfVectorizer(decode_error='ignore',
                     strip_accents='unicode',
                     use_idf=True)
                     
    train_vectors = vectorizer.fit_transform(train_data)

    # Perform classification with SVM, kernel=rbf
    classifier_rbf = svm.SVC()
    classifier_rbf.fit(train_vectors, train_labels)
        
    test_vectors = vectorizer.transform(test_data)      
    prediction_rbf = classifier_rbf.predict(test_vectors)
    print(classification_report(test_labels, prediction_rbf))

businessId = appendDataToCSV('C:\Users\shivika\Desktop\Sem 2\CS-223\CS223 - PROJECT\dataset\yelp_academic_dataset_business.json')
print len(businessId)
businessId = businessId[:100]
train = outputReviewsCSV('C:\Users\shivika\Desktop\Sem 2\CS-223\CS223 - PROJECT\dataset\yelp_academic_dataset_review.json',businessId)


#print train
#cl = NaiveBayesClassifier(train)
test_data = ["their burgers are amazing"]
#print cl.classify("I don't like their pizza.") 

newData = train[:10]
#print newData
newClassifier(newData,test_data)
#classif = SklearnClassifier(SVC(), sparse=False).train(newData)
#classif.classify_many("I don't like their pizza.")
