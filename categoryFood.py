import ujson
import csv
    
def appendDataToCSV(csvFile,jsonFileToRead,dictKeys,dataTitles):
    #open CSV file to write to
    csvReviewFile = open(csvFile, 'a+')
    csvFileWriter = csv.writer(csvReviewFile)
    csvFileWriter.writerow(dataTitles)
    
    with open(jsonFileToRead, 'rb') as jsonFile:
        newList = []
        for line in jsonFile:
            json_data = ujson.loads(line)
            currentData = []
            for key in dictKeys:
                if isinstance(json_data[key],basestring):
                    #remove unicode characters in strings~\Desktop\Sem 2\CS-223\CS223 - PROJECT\yelp_dataset_challenge_academic_dataset
                    currentData.append(json_data[key].encode('ascii','ignore'))
                else:
                    currentData.append(json_data[key])       
            
            #print currentData
            writeData = "" 
            #newList1 = []
            newList2 = []
            
            newList2 = foodInCategory(currentData)

#            for cat_list in currentData: 
#                try:     
#                    if any('food' in string1 for string1 in cat_list):
#                        #print currentData[0],cat_list 
#                        newList1.append(currentData[0])
#                        newList1.append(currentData[1])
#                except:
#                    cat_list = []
        
            #print newList2
                    
        #try: 
            csvFileWriter.writerow(currentData)
        #except:
        #    csvReviewFile.close()
    csvReviewFile.close()
    
    
###################################################################################################################################################    
#This function selects the category where 'food' is one of the subcategories and returns it with a corresponding Business_id in the form of a list.

def foodInCategory(currentData):
    for cat_list in currentData: 
        try: 
            newList1 = []    
            if any('food' in string1 for string1 in cat_list):
                print currentData[0],currentData[1]
                #newList1.append(currentData[0])
                #newList1.append(currentData[1])
        except:
            cat_list = []
    return newList1

#################################################################################################################################################



#appendDataToCSV('yelp_Review_CSV.csv','yelp_academic_dataset_review.json',['text','stars','business_id'],['Reviews','Stars','BusinessID'])
appendDataToCSV('yelp_Category_CSV.csv','yelp_academic_dataset_business.json',['business_id','categories'],['Category','Business-ID'])

#TODO  - Map reviews to categories according to business IDs
#TODO - Find why the csv is getting stored on alternate lines
#TODO - write comments~\Desktop\Sem 2\CS-223\CS223 - PROJECT\yelp_dataset_challenge_academic_dataset