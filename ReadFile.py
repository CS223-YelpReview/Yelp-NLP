import ujson
import csv
    
def outputReviewsCSV(jsonFile, outputCSV, businessId, dictKeys):
    csvReviewFile = open(outputCSV, 'a+')
    csvFileWriter = csv.writer(csvReviewFile)
    
    with open(jsonFile,'rb') as jsonFile:
        for line in jsonFile:
            json_data = ujson.loads(line)
            currentData = []
            if json_data['business_id'] in businessId:
                currentData.append(json_data['business_id'])
                for key in dictKeys:
                    if isinstance(json_data[key],basestring):
                        currentData.append(json_data[key].encode('ascii','ignore'))
                    else:
                        currentData.append(json_data[key])
                csvFileWriter.writerow(currentData)
    csvReviewFile.close()    
    
#def appendDataToCSV(csvFile,jsonFileToRead,dictKeys,dataTitles):
#    #open CSV file to write to
#    csvReviewFile = open(csvFile, 'a+')
#    csvFileWriter = csv.writer(csvReviewFile)
#    csvFileWriter.writerow(dataTitles)
#    
#    with open(jsonFileToRead, 'rb') as jsonFile:
#        for line in jsonFile:
#            json_data = ujson.loads(line)
#            currentData = []
#            for key in dictKeys:
#                if isinstance(json_data[key],basestring):
#                    #remove unicode characters in strings
#                    currentData.append(json_data[key].encode('ascii','ignore'))
#                else:
#                    currentData.append(json_data[key])
#        #try: 
#            csvFileWriter.writerow(currentData)
#        #except:
#        #    csvReviewFile.close()
#    csvReviewFile.close()

outputReviewsCSV('F:\Courses\Bio Informatics\Project\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json','F:\Courses\Bio Informatics\Project\yelp_dataset_challenge_academic_dataset\yelp_Review_CSV.csv',['UsFtqoBl7naz8AVUBZMjQQ'],['text','stars'])
#appendDataToCSV('F:\Courses\Bio Informatics\Project\yelp_dataset_challenge_academic_dataset\yelp_Review_CSV.csv','F:\Courses\Bio Informatics\Project\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json',['text','stars','business_id'],['Reviews','Stars','BusinessID'])
#appendDataToCSV('F:\Courses\Bio Informatics\Project\yelp_dataset_challenge_academic_dataset\yelp_Category_CSV.csv','F:\Courses\Bio Informatics\Project\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_business.json',['categories'],['Category'])

#TODO  - Map reviews to categories according to business IDs
#TODO - Find why the csv is getting stored on alternate lines
#TODO - write comments