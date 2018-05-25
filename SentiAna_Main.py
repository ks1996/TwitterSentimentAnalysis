# Winter Rsearch Internship on Sentiment Analysis
#Challenge was to successfully acquire the tweets having bitcoin as keyword from twitter and in English language, clean them, extract their related information like time,date, place them in text or csv files with the features, bag of words and their frequency in order to create the dataset for training the SVM or Naive Bayes. 

import pandas as pd
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
import time
import tweepy
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re 
import datetime
import numpy as np
import pyexcel as pe
import csv
import nltk.classify
import codecs
from unidecode import unidecode
from operator import itemgetter
import six 
from io import StringIO
import operator

now = datetime.datetime.now()
debug = True
#Function for cleaning the tweets 
def processTweet(tweetFeed):
    #Convert to lower case
    tweetFeed = tweetFeed.lower()
    #Convert www.* or https?://* to URL
    tweetFeed = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',tweetFeed)
    #Convert @username to AT_USER
    tweetFeed = re.sub('@[^\s]+','',tweetFeed)
     #Convert rt to " "
    tweetFeed = re.sub('^rt+','',tweetFeed)
    #Remove additional white spaces
    tweetFeed = re.sub('[\s]+', ' ', tweetFeed)
    #Replace #word with word
    tweetFeed = re.sub(r'#([^\s]+)', r'\1', tweetFeed)
    #Remove the URLs
    tweetFeed = re.sub(r"http\S+", "", tweetFeed)
    #Remove number string
    tweetFeed = re.sub(r'[0-9]+', '', tweetFeed)
    #trim
    tweetFeed = tweetFeed.strip('\'"')
    return tweetFeed

#Function to look for 2 or more repetitions of character and replace with the character itself
def replaceTwoOrMore(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


#Function to read Stop Words(common terms not required for sentiment Analysis)
def getStopWordList(stopWordListFileName):
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords



'''#Extract words for features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        if word in tweet_words:
	    features['(%s)' % word] = '1'
	else:
	    features['(%s)' % word] = '0'
    return features
'''

#Extracting Feature and cleaning the tweet once more
def getFeatureVector(tweet, stopWords):
    featureVector = []  
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences 
        w = replaceTwoOrMore(w) 
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if it consists of only words
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        #ignore if it is a stopWord
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector    

# Authentication keys taken from the Twitter API
ckey='6Yjmz6kKuo3roS3OYTzGEUQWa'
csecret='nlPhSo2TRcC82BuumsfdULWYCW0oS4OZnbjNw1uetR2nCvgJlL'
atoken='198871758-7qhNSAVlNOD8KqWgVwE3vA6w3zidxRj6c7OZhkll'
asecret='30EfVf8V3AMxI7P5ht93PftbsLhnEYl2sNRQIgcIvb6xv'

#Authenticating
auth=tweepy.OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

api = tweepy.API(auth)

#Taking a set of live Tweets with keyword Bitcoin
public_tweets = api.search('Bitcoin')


# Adding the cleaned tweets, processed to files
# the text files include 
for tweet in public_tweets:
    if tweet.lang == "en":
       	processedTweet = processTweet(tweet.text)
	saveFile13= open('Twidb20.txt', 'a')#Text of tweet and time stamp converted to time of tweet 
	posix1_time = time.time()
	unix1_timestamp  = int(posix1_time)
	utc1_time = time.gmtime(unix1_timestamp)
	local_time = time.localtime(unix1_timestamp)
	saveThis13= (time.strftime("%H:%M:%S", local_time)+ '|' +processedTweet).encode('utf-8')
	saveFile13.write(saveThis13)
	saveFile13.write('\n')
	saveFile13.close()
	analysis = TextBlob(processedTweet)
	Senti = analysis.sentiment.polarity
	Senti1 = analysis.sentiment.subjectivity
	if Senti > 0:
		saveFile11 = open('Twidb11.csv', 'a')#Text of tweet only
		saveThis11 = (processedTweet+" "+ "zzzPositive").encode('utf-8')
		saveFile11.write(saveThis11 + " ")
		saveFile11.write('\n')
		saveFile11.close()
	elif Senti == 0:
		saveFile11 = open('Twidb11.csv', 'a')
		saveThis11 = (processedTweet+" "+ "zzzNeutral").encode('utf-8')
		saveFile11.write(saveThis11 + " ")
		saveFile11.write('\n')
		saveFile11.close()
	else: 
		saveFile11 = open('Twidb11.csv', 'a')
		saveThis11 = (processedTweet+" "+ "zzzNegative").encode('utf-8')
		saveFile11.write(saveThis11 + " ")
		saveFile11.write('\n')
		saveFile11.close()
	if Senti > 0:
	    if Senti1>=0.5:
	       saveFile = open('Twidb4.csv', 'a')# date, sentiment(Positive/Negative/neutral also Fact/Opinion),processed and cleaned tweet
	       saveThis = (str("Opii")+ ':'+str("POS")+':'+str(time.time())+ ':'+ str(now.year)+'-'+str(now.month)+'-'+str(now.day)+ ':'+ processedTweet).encode('utf-8')
	       saveFile.write(saveThis)
	       saveFile.write('\n')
	       saveFile.close()
	    else: 
	       saveFile = open('Twidb4.csv', 'a')
	       saveThis = (str("Fact")+ ':'+str("POS")+':'+str(time.time())+ ':'+ str(now.year)+'-'+str(now.month)+'-'+str(now.day)+ ':'+ processedTweet).encode('utf-8')
	       saveFile.write(saveThis)
	       saveFile.write('\n')
	       saveFile.close()
	elif Senti == 0:
	    if Senti1>=0.5:
	       saveFile = open('Twidb4.csv', 'a')
	       saveThis = (str("Opii")+ ':'+str("NEU")+':'+str(time.time())+ ':'+ str(now.year)+'-'+str(now.month)+'-'+str(now.day)+ ':'+ processedTweet).encode('utf-8')
	       saveFile.write(saveThis)
	       saveFile.write('\n')
	       saveFile.close()
	    else: 
	       saveFile = open('Twidb4.csv', 'a')
	       saveThis = (str("Fact")+ ':'+str("NEU")+':'+str(time.time())+ ':'+ str(now.year)+'-'+str(now.month)+'-'+str(now.day)+ ':'+ processedTweet).encode('utf-8')
	       saveFile.write(saveThis)
	       saveFile.write('\n')
	       saveFile.close()
	else:
	    if Senti1>0.5:
	       saveFile = open('Twidb4.csv', 'a')
	       saveThis = (str("Opii")+ ':'+str("NEG")+':'+str(time.time())+ ':'+ str(now.year)+'-'+str(now.month)+'-'+str(now.day)+ ':'+ processedTweet).encode('utf-8')
	       saveFile.write(saveThis)
	       saveFile.write('\n')
	       saveFile.close()
	    else: 
	       saveFile = open('Twidb4.csv', 'a')
	       saveThis = (str("Fact")+ ':'+str("NEG")+':'+str(time.time())+ ':'+ str(now.year)+'-'+str(now.month)+'-'+str(now.day)+ ':'+ processedTweet).encode('utf-8')
	       saveFile.write(saveThis)
	       saveFile.write('\n')
	       saveFile.close()
      	print(analysis.sentiment)
	stopWords = []
	


#Read the tweets one by one and process it
fp = open('Twidb4.csv', 'r')
line = fp.readline()

st = open('StopWords.txt', 'r')# all the stop words
stopWords = getStopWordList('StopWords.txt')

while line:
    processedTweet = processTweet(line)
    featureVector = getFeatureVector(processedTweet, stopWords)
    saveFile1 = open('Twidb5.txt', 'a')#prints featureVector
    saveThis1 = str(featureVector).encode('utf-8')
    saveFile1.write(saveThis1)
    saveFile1.write('\n')
    saveFile1.close()
    line = fp.readline()
fp.close()

#Read the tweets one by one and process it
inpTweets = csv.reader(open('Twidb4.csv', 'rb'), delimiter=':')
tweets = []
featureList=[]
for row in inpTweets:
    sentiment = row[1]
    tweet = row[4]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment));
#print tweets
saveFile2 = open('Twidb6.txt', 'a')# main words and the tweet's sentiment
saveThis2 = str(tweets).encode('utf-8')
saveFile2.write(saveThis2)
saveFile2.write('\n')
saveFile2.close()







