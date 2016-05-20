import csv
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as mplot

class sentimentObj:
     def __init__(self):
         self.positiveVal = 0.0
         self.negativeVal = 0.0
         self.neutralVal = 0.0
         self.stars = 1

#for bargraphs
def plotGraph(posScore,negScore,poslabel,neglabel,title):
    fig, ax = mplot.subplots()
    index = np.arange(len(posScore))
    bar_width = 0.35
    opacity = 0.8
    mplot.bar(index, posScore, bar_width,alpha=opacity,color='b',label=poslabel)
    mplot.bar(index + bar_width, negScore, bar_width,alpha=opacity,color='g',label=neglabel)
    mplot.xlabel('Reviews')
    mplot.ylabel('Scores')
    mplot.title(title)
    mplot.xticks(index + bar_width, index)
    mplot.legend()
    mplot.tight_layout()
    mplot.show()
    
sid=SentimentIntensityAnalyzer()

totalSentimentdata=[]

with open('yelp_Review_CSV.csv', 'rb') as reviewFile:
    reader = csv.DictReader(reviewFile)
    reviewCount = 0
    for row in reader:
        try:
            if row['Reviews']:
                newReview = sentimentObj()
                ss = sid.polarity_scores(row['Reviews'])
            
                newReview.stars = row['Stars']
                newReview.negativeVal = ss['neg']
                newReview.positiveVal = ss['pos']
                newReview.neutralVal = ss['neu']
                totalSentimentdata.append(newReview)
                reviewCount += 1
                print reviewCount
        except:
            break
        

#to plot
plotGraph([review.positiveVal for review in totalSentimentdata if int(review.stars) == 1], [review.negativeVal for review in totalSentimentdata if int(review.stars) == 1],'Positive Score','Negative Score','Scores of Text with 1-star Review')
plotGraph([review.positiveVal for review in totalSentimentdata if int(review.stars) == 2], [review.negativeVal for review in totalSentimentdata if int(review.stars) == 2],'Positive Score','Negative Score','Scores of Text with 2-star Review')
plotGraph([review.positiveVal for review in totalSentimentdata if int(review.stars) == 3], [review.negativeVal for review in totalSentimentdata if int(review.stars) == 3],'Positive Score','Negative Score','Scores of Text with 3-star Review')
plotGraph([review.positiveVal for review in totalSentimentdata if int(review.stars) == 4], [review.negativeVal for review in totalSentimentdata if int(review.stars) == 4],'Positive Score','Negative Score','Scores of Text with 4-star Review')
plotGraph([review.positiveVal for review in totalSentimentdata if int(review.stars) == 5], [review.negativeVal for review in totalSentimentdata if int(review.stars) == 5],'Positive Score','Negative Score','Scores of Text with 5-star Review')

print "Percentage of positive values > negative values for 1-star Reviews: " + str(float(len([review.positiveVal for review in totalSentimentdata if int(review.stars) == 1 and review.positiveVal > review.negativeVal]))/len([review for review in totalSentimentdata if int(review.stars) == 1]))
print "Percentage of positive values > negative values for 2-star Reviews: " + str(float(len([review.positiveVal for review in totalSentimentdata if int(review.stars) == 2 and review.positiveVal > review.negativeVal]))/len([review for review in totalSentimentdata if int(review.stars) == 2]))
print "Percentage of positive values > negative values for 3-star Reviews: " + str(float(len([review.positiveVal for review in totalSentimentdata if int(review.stars) == 3 and review.positiveVal > review.negativeVal]))/len([review for review in totalSentimentdata if int(review.stars) == 3]))
print "Percentage of positive values > negative values for 4-star Reviews: " + str(float(len([review.positiveVal for review in totalSentimentdata if int(review.stars) == 4 and review.positiveVal > review.negativeVal]))/len([review for review in totalSentimentdata if int(review.stars) == 4]))
print "Percentage of positive values > negative values for 5-star Reviews: " + str(float(len([review.positiveVal for review in totalSentimentdata if int(review.stars) == 5 and review.positiveVal > review.negativeVal]))/len([review for review in totalSentimentdata if int(review.stars) == 5]))
    
   

