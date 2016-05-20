# File Name:  naiveBayes.py 
# By: Pratibha, Praveen, Shivika, Ahsish 
# Date: 5/19/2016
# Python Version(s) 2.7.3: 
""" FILE DESCRIPTION: 
    The file takes review text and rating from Yelp data set, train the models 
    using textblobber naive Bayes package, tests the test data with the model 
    outputs the accuracy"""

import ujson
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
#Importing library for stopwords
from nltk.corpus import stopwords
#Importing library for system arguments
import sys

# Class naiveBayes 
class naiveBayes:
    def __init__(self):
        self.testSentences = []
        
       
    def deriveBusinessId(self,jsonFileToRead):
        """ DESCRIPTION: deriveBusinessId   Function to extract the business Id of the 'food' category 
            PRECONDITIONS:  jsonFileToRead must be present in the directory.   
            POSTCONDITIONS: Function outputs Business Id's for which  
            SIDEEFFECTS:  
            ERROR CONDITIONS: File not found error if input file not found  """ 
        with open(jsonFileToRead, 'rb') as jsonFile:
            #create a temp list to store results
            currentData = []
            for line in jsonFile:
                json_data = ujson.loads(line)
                category = ''.join(json_data['categories'])
                if "food" in category.lower():
                    currentData.append(json_data['business_id'])
        return currentData

    #Function to extract the review text and ratings from th json file
    def getTrainData(self, jsonFile, businessId):
        currentData = []
        with open(jsonFile,'rb') as jsonFile:
            reviewCnt = 0
            for line in jsonFile:
                json_data = ujson.loads(line)
                
                reviewCnt +=1
                print reviewCnt
                filtered_word_list = []
                word_list = json_data['text'].lower().split()
                #code to 
                for word in word_list: # iterate over word_list
                    if word not in stopwords.words('english'): 
                        filtered_word_list.append(word)
                refined_text = " ".join(filtered_word_list)
                if json_data['business_id'] in businessId and reviewCnt < 80000 :
                    #considering only rating 1 and 5 which will give good results
                    if (int(json_data['stars']) == 1):
                        tupl = (refined_text,'neg')
                        currentData.append(tupl)
                    elif(int(json_data['stars']) == 5):
                        tupl = (refined_text,'pos')
                        currentData.append(tupl)
                elif reviewCnt < 80500:
                    tupl = (refined_text,json_data['stars'])
                    self.testSentences.append(tupl)
                else:
                    break
        return currentData

    

    def testSentence(self,sentence,classifier):
        filtered_word_list = [word for word in sentence.lower().split() if word not in stopwords.words('english')]
        refinedText = " ".join(filtered_word_list)
        blob = TextBlob(refinedText, classifier=classifier)
        return blob.classify()
    
    def calcAccuracy(self,fileName= "naiveBayesResult.txt"):
        """ DESCRIPTION: calcAccuracy   Function to accuracy of the naive bayes model 
            PRECONDITIONS:  jsonFileToRead must be present in the directory.   
            POSTCONDITIONS: Function outputs Business Id's for which  
            SIDEEFFECTS:  
            ERROR CONDITIONS: File not found error if input file not found  """ 
        wrong1predicted, wrong2predicted, wrong3predicted = (0,)*3
        wrong4predicted, wrong5predicted = (0,) *2
        total1, total2, total3, total4, total5 = (0,)*5 
        with open(fileName,'rb') as csv:
            for line in csv:
                data = line.split()
                if(int(data[0]) == 1):
                    total1 = total1 +1
                    if(data[1]!='neg'):
                        wrong1predicted = wrong1predicted +1
                elif(int(data[0]) == 2):
                    total2 = total2 +1
                    if(data[1]!='neg'):
                        wrong2predicted = wrong2predicted +1
                        
                elif(int(data[0]) == 3):
                    total3 = total3 +1
                    if(data[1]!='pos'):
                        wrong3predicted = wrong3predicted +1
                    
                elif(int(data[0]) == 4):
                    total4 = total4 +1
                    if(data[1]!='pos'):
                        wrong4predicted = wrong4predicted +1
                    
                elif(int(data[0]) == 5):
                    total5 = total5 +1
                    if(data[1]!='pos'):
                        wrong5predicted = wrong5predicted +1
            
        # print "total 1: ",total1, "wrongPredicted: ",wrong1predicted,"Accuracy: ",(total1-wrong1predicted)*100/total1 
        # print "total 2: ",total2, "wrongPredicted: ",wrong2predicted,"Accuracy: ",(total2-wrong2predicted)*100/total2 
        #print "total 3: ",total3, "wrongPredicted: ",wrong3predicted,"Accuracy: ",(total3-wrong3predicted)*100/total3 
        #print "total 4: ",total4, "wrongPredicted: ",wrong4predicted,"Accuracy: ",(total4-wrong4predicted)*100/total4 
        #print "total 5: ",total5, "wrongPredicted: ",wrong5predicted,"Accuracy: ",(total5-wrong5predicted)*100/total5 
        print '{0:10} ==> {1:10d}'.format('accuracy for rating 1',  (total1-wrong1predicted)*100/total1)
        print '{0:10} ==> {1:10d}'.format('accuracy for rating 2',  (total2-wrong2predicted)*100/total2)
        print '{0:10} ==> {1:10d}'.format('accuracy for rating 3',  (total3-wrong3predicted)*100/total3)
        print '{0:10} ==> {1:10d}'.format('accuracy for rating 4',  (total4-wrong4predicted)*100/total4)
        print '{0:10} ==> {1:10d}'.format('accuracy for rating 5',  (total5-wrong5predicted)*100/total5)
        csv.close()

def main(argv=0):
    nBObj = naiveBayes()
    businessId = nBObj.deriveBusinessId('yelp_academic_dataset_business.json')
    print len(businessId)
    businessId = businessId[:10]
    train = nBObj.getTrainData('yelp_academic_dataset_review.json',businessId)
 
    print train
    cl = NaiveBayesClassifier(train)

    print cl.show_informative_features(20) 
    print "Opening the file..."
    target = open("naiveBayesResult.txt", 'w')

    for (sentence,rating) in nBObj.testSentences:
        clOutput = nBObj.testSentence(sentence,cl)
        strToWrite = str(rating) + "\t" + clOutput
        target.write(strToWrite)
        target.write("\n")
      
    target.close()
    nBObj.calcAccuracy()
  
        
if __name__ == "__main__":
    main(sys.argv)