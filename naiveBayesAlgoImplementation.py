from __future__ import division 
import ujson
import csv
from nltk.corpus import stopwords
import re
import sys

class naiveBayes:
    stopset = set(stopwords.words('english'))

    def __init__(self):
        self.posWordDict = dict()
        self.posWordProb = dict()
        self.negWordDict = dict()
        self.negWordProb = dict()
        self.allWordDict = dict()
        self.probPositive = 0
        self.probNegative = 0
        self.countReviews = 0
        self.countPosReviews = 0
        self.countNegReviews= 0
        
    def stringTok(self,string):
        word_list = string.split()
        filtered_word_list = word_list[:] #make a copy of the word_list
        for word in word_list: # iterate over word_list
            if word in stopwords.words('english'): 
                filtered_word_list.remove(word)
            
            filteredString = ' '.join(filtered_word_list)
            filteredString = re.sub('[^A-Za-z ]+', '', filteredString)
        return filteredString



    def outputReviewsCSV(self,jsonFile, outputCSV, businessId, dictKeys):
        csvReviewFile = open(outputCSV, 'w')
        #csvFileWriter = csv.writer(csvReviewFile)
        with open(jsonFile,'rb') as jsonFile:
            for line in jsonFile:
                json_data = ujson.loads(line)
               
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
                            filteredString = filteredString.strip('\n') 
                            print filteredString  
                            csvReviewFile.write(","+filteredString)
                        else:
                            csvReviewFile.write(str(json_data[key]))
                    csvReviewFile.write("\n")    
                   # if currentData:
                    #    csvReviewFile.write(currentData)
        csvReviewFile.close()    
    

    def formProbability(self,csvFile):
        with open(csvFile, "rb") as f:
            reader = csv.reader(f, delimiter="\t")
            for lines in reader:
                line = lines[0].split(',')
                wordList = line[0].split()
                if(int(line[1])<4 & int(line[1]) > 0 ):
                    self.countNegReviews += 1
                    for word in wordList:
                        if self.negWordDict.has_key(word):
                            self.negWordDict[word] += 1
                        else:
                            self.negWordDict[word] = 1
                elif(int(line[1])>3 & int(line[1]) < 6):
                    self.countPosReviews += 1
                    for word in wordList:
                        if self.posWordDict.has_key(word):
                            self.posWordDict[word] += 1
                        else:
                            self.posWordDict[word] = 1
            
        f.close()
    

    def naiveBayes(self):
        entireVoc =  set(self.negWordDict.keys())
        entireVoc.update(self.posWordDict.keys())
        totalCount = len(entireVoc)
        negWordCount = len(self.negWordDict)
        posWordCount = len(self.posWordDict)
                
        print "Total Reviews: ",self.countReviews
        print "Positive Reviews: ",self.countPosReviews
        print "Negative Reviews: ",self.countNegReviews
        print "Neg words: ",negWordCount
        print "Pos words: ",posWordCount
        print "Total words: ",totalCount
        print "Pos Good: ",self.posWordDict['good']
       # print "Neg Good: ",self.negWordDict['good']
        for key,value in self.negWordDict.iteritems():
            self.negWordProb[key] = (1 + value) / (negWordCount + totalCount)
        
        for key,value in self.posWordDict.iteritems():
            self.posWordProb[key] = (1 + value) / (posWordCount + totalCount)
        
        #print "Negative Probablity:\n", self.negWordProb
        print "\n"
        #print "Positive Probablity:\n", self.posWordProb
    


    def findProbablity(self,review_input):
        totalCount = self.countPosReviews + self.countNegReviews 
        posProb = self.countPosReviews / totalCount
        negProb = self.countNegReviews / totalCount
        posProbWord = posProb
        negProbWord = negProb
        filteredString = self.stringTok(review_input)
        for word in filteredString:
            if word in self.posWordProb:
                posProbWord = posProbWord * self.posWordProb[word]
            
            if word in self.negWordProb:
                negProbWord = negProbWord * self.negWordProb[word]
        
        print "Positive Prob word: ", posProbWord
        print "Negative Prob word: ", negProbWord
        if(posProbWord > negProbWord):
            print "Positive Review"
        else:
            print "Negative Review"
        
    
    def appendDataToCSV(self,jsonFileToRead):
    #def appendDataToCSV(csvFile,jsonFileToRead,dataTitles):
        #csvReviewFile = open(csvFile, 'a+')
        #csvFileWriter = csv.writer(csvReviewFile)
        #csvFileWriter.writerow(dataTitles)
        with open(jsonFileToRead, 'rb') as jsonFile:
            currentData = []
            for line in jsonFile:
                json_data = ujson.loads(line)
                category = ''.join(json_data['categories'])
                if "food" in category.lower():
                    currentData.append(json_data['business_id'])
                    #currentData.append(json_data['categories'])
                    #csvFileWriter.writerow(currentData)
                    #json_data['business_id']
        #csvReviewFile.close()
        return currentData
 
    def main(argv=0):
        if (argv == 0):
            print "please enter the file name to read"
        naiveBayesObj = naiveBayes()
        businessId = naiveBayesObj.appendDataToCSV('F:\Courses\Bio Informatics\Project\dataset\yelp_academic_dataset_business.json')
        print len(businessId)
        businessId = businessId[:100]
        print businessId
        naiveBayesObj.outputReviewsCSV('F:\Courses\Bio Informatics\Project\dataset\yelp_academic_dataset_review.json','F:\Courses\Bio Informatics\Project\dataset\yelp_Review_CSV.txt',businessId,['stars','text'])
        naiveBayesObj.formProbability('F:\Courses\Bio Informatics\Project\dataset\yelp_Review_CSV.csv')
        naiveBayesObj.naiveBayes()

        while(1):
            var = raw_input("Enter the Review (Exit to quit): ")
            if var.lower() == "exit":
                break
            naiveBayesObj.findProbablity (var)
    

    if __name__ == "__main__":
        main(sys.argv)