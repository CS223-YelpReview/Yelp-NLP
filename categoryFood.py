import ujson
import csv
    
def appendDataToCSV(csvFile,jsonFileToRead,dataTitles):
    #open CSV file to write to
    csvReviewFile = open(csvFile, 'a+')
    csvFileWriter = csv.writer(csvReviewFile)
    csvFileWriter.writerow(dataTitles)
    
    with open(jsonFileToRead, 'rb') as jsonFile:
        for line in jsonFile:
            currentData = []
            json_data = ujson.loads(line)
            category = ''.join(json_data['categories'])
            if "food" in category.lower():
                currentData.append(json_data['business_id'])
                currentData.append(json_data['categories'])
                csvFileWriter.writerow(currentData)
    csvReviewFile.close()
    


appendDataToCSV('yelp_Category_CSV1.csv','yelp_academic_dataset_business.json',['Business-ID','Category'])

