import json
import nltk 
from nltk.corpus import stopwords

data = []
with open("yelp_academic_dataset_review.json") as json_file:
    for line in json_file:
        data.append(json.loads(line))

   
    
#filtered_words = [word for word in json_data if word not in stopwords.words('english')]    
      
       
        
         
          
           
             