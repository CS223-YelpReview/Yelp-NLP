from nltk.corpus import stopwords

word = "Tiger is national animal teh"
word_list = word.split();
print word_list
filtered_word_list = word_list[:] #make a copy of the word_list
for word in word_list: # iterate over word_list
  if word in stopwords.words('english'): 
    filtered_word_list.remove(word)
    
print filtered_word_list