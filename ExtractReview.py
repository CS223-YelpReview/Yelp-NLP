from __future__ import division 
import ujson
import csv
from nltk.corpus import stopwords
import re


posWordDict = dict()
posWordProb = dict()
negWordDict = dict()
negWordProb = dict()
allWordDict = dict()
probPositive = 0
probNegative = 0
countReviews = 0
countPosReviews = 0
countNegReviews= 0
    
stopset = set(stopwords.words('english'))

def stringTok(string):
    word_list = string.split()
    filtered_word_list = word_list[:] #make a copy of the word_list
    for word in word_list: # iterate over word_list
        if word in stopwords.words('english'): 
            filtered_word_list.remove(word)
            
        filteredString = ' '.join(filtered_word_list)
        filteredString = re.sub('[^A-Za-z ]+', '', filteredString)
    return filteredString



def outputReviewsCSV(jsonFile, outputCSV, businessId, dictKeys):
    csvReviewFile = open(outputCSV, 'w')
    csvFileWriter = csv.writer(csvReviewFile)
    with open(jsonFile,'rb') as jsonFile:
        for line in jsonFile:
            json_data = ujson.loads(line)
            currentData = []
            if json_data['business_id'] in businessId:
                for key in dictKeys:
                    if isinstance(json_data[key],basestring):
                        word_list = json_data[key].encode('ascii','ignore').lower().split()
                        filtered_word_list = word_list[:] #make a copy of the word_list
                        for word in word_list: # iterate over word_list
                            if word in stopwords.words('english'): 
                                filtered_word_list.remove(word)
                                
                            filteredString = ' '.join(filtered_word_list)
                            filteredString = re.sub('[^A-Za-z ]+', '', filteredString)
                        currentData.append(filteredString)
                    else:
                        currentData.append(json_data[key])
                   
                csvFileWriter.writerow(currentData)
    csvReviewFile.close()    
    

def formProbability(csvFile):
    global countReviews
    global countNegReviews
    global countPosReviews
    with open(csvFile, "rb") as f:
        reader = csv.reader(f, delimiter="\t")
        for lines in reader:
            countReviews += 1
            line = lines[0].split(',')
            wordList = line[0].split()
            if(int(line[1])<3):
                countNegReviews += 1
                for word in wordList:
                    if negWordDict.has_key(word):
                        negWordDict[word] += 1
                    else:
                        negWordDict[word] = 1
            else:
                countPosReviews += 1
                for word in wordList:
                    if posWordDict.has_key(word):
                        posWordDict[word] += 1
                    else:
                        posWordDict[word] = 1
            
    f.close()
    

def naiveBayes():
    entireVoc =  set(negWordDict.keys())
    entireVoc.update(posWordDict.keys())
    totalCount = len(entireVoc)
    negWordCount = len(negWordDict)
    posWordCount = len(posWordDict)
    
   
    for key,value in negWordDict.iteritems():
        negWordProb[key] = (1 + value) / (negWordCount + totalCount)
        
    for key,value in posWordDict.iteritems():
        posWordProb[key] = (1 + value) / (posWordCount + totalCount)
    
    print "Negative Probablity:\n", negWordProb
    print "\n"
    print "Positive Probablity:\n", posWordProb
    
outputReviewsCSV('F:\Courses\Bio Informatics\Project\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json','F:\Courses\Bio Informatics\Project\yelp_dataset_challenge_academic_dataset\yelp_Review_CSV.csv',['UsFtqoBl7naz8AVUBZMjQQ'],['text','stars'])
formProbability('F:\Courses\Bio Informatics\Project\yelp_dataset_challenge_academic_dataset\yelp_Review_CSV.csv')
naiveBayes()

def findProbablity(review_input):
    posProb = countPosReviews / countReviews
    negProb = countNegReviews / countReviews
    posProbWord = posProb
    negProbWord = negProb
    filteredString = stringTok(review_input)
    for word in filteredString:
        if word in posWordProb:
            posProbWord = posProbWord * posWordProb[word]
            
        if word in negWordProb:
            negProbWord = negProbWord * negWordProb[word]
        
    print "Positive Prob word: ", posProbWord
    print "Positive Neg word: ", negProbWord
    if(posProbWord > negProbWord):
        print "Positive Review"
    else:
        print "Negative Review"
        
    
    

var = raw_input("Enter the Review: ")
findProbablity (var)
