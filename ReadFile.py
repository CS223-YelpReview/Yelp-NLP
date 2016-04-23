import ujson
import csv
    
def appendDataToCSV(csvFile,jsonFileToRead,dictKeys,dataTitles):
    #open CSV file to write to
    csvReviewFile = open(csvFile, 'a+')
    csvFileWriter = csv.writer(csvReviewFile)
    csvFileWriter.writerow(dataTitles)
    
    with open(jsonFileToRead, 'rb') as jsonFile:
        for line in jsonFile:
            json_data = ujson.loads(line)
            currentData = []
            for key in dictKeys:
                if isinstance(json_data[key],basestring):
                    #remove unicode characters in strings
                    currentData.append(json_data[key].encode('ascii','ignore'))
                else:
                    currentData.append(json_data[key])
        #try: 
            csvFileWriter.writerow(currentData)
        #except:
        #    csvReviewFile.close()
    csvReviewFile.close()


appendDataToCSV('yelp_Review_CSV.csv','yelp_academic_dataset_review.json',['text','stars','business_id'],['Reviews','Stars','BusinessID'])
appendDataToCSV('yelp_Category_CSV.csv','yelp_academic_dataset_business.json',['categories'],['Category'])

#TODO  - Map reviews to categories according to business IDs
#TODO - Find why the csv is getting stored on alternate lines
#TODO - write comments