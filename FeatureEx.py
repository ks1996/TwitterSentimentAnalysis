# code for extracting feature, i.e creating bag of words and checking the frequency of each word in the tweet.
import pandas as pd
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
import time
import json
import numpy as np
import pyexcel as pe
import csv, codecs
from unidecode import unidecode
from operator import itemgetter
import operator

#Function that reads the frequency matrix and prints it to file in the desired order.
def write_matrix_to_textfile(a_matrix, file_to_write):

    def compile_row_string(a_row):
        return str(a_row).strip(']').strip('[').replace(' ',',')

    with open(file_to_write, 'a') as f:
        for row in a_matrix:
            f.write(compile_row_string(row)+'\n')

    return True

df = pd.read_csv('TextOnly.csv',error_bad_lines=False, sep='delimiter',  engine='python')#Twidb11.csv
#data = pd.read_csv('Twidb10.txt', error_bad_lines=False)
# Creating Bag of Words
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(df.Text)
freq_matrix = count_vect.fit_transform(df.Text).toarray()
print freq_matrix
#X_train_counts.shapea
words = count_vect.vocabulary_
words = {str(i):j for i,j in words.items()}
#print words
sorted_words = sorted(words.items(), key=operator.itemgetter(1))
print sorted_words
saveFile8 = open('TweetDataSet.txt', 'a')#Twidb18.txt
count = 0;
for key, value in sorted_words:
	saveThis8 = key
	saveFile8.write(saveThis8)
	
	count+=1
	if count <len(sorted_words):
		saveFile8.write(',')

saveFile8.write('\n')
saveFile8.close()

ab = write_matrix_to_textfile(freq_matrix, 'TweetDataSet.txt')

