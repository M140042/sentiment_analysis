# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 10:34:36 2018

@author: M1400

"""
import re
import pandas as pd
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
import nltk
from nltk.corpus import stopwords

def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        res = []
        for t in tweet:
            res.append(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", t).split()))
        return res

def rem_stopwords(tweet):
    stopwords_set = set(stopwords.words("english"))
    tweets=[]
    for index, row in enumerate(tweet):
        words_filtered = [e.lower() for e in row.split() if len(e) >= 3]
        words_cleaned = [word for word in words_filtered if 'http' not in word and not word.startswith('@') and not word.startswith('#') and word != 'RT']
        words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
        final = ' '.join(words_without_stopwords)
        tweets.append(final)
    return tweets


    
def sentiment(analysis):
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
    
data=pd.read_csv("output_got.csv",sep=';', index_col=False)
data['text'] = data.text
tweet=clean_tweet(data['text'])
final=rem_stopwords(tweet)
senti=[]  
for temp in final:  
    senti.append(sentiment(TextBlob(temp)))
    

    

# picking positive tweets from tweets
ptweets = [tweet[i] for i in range(len(senti)) if senti[i] == 'positive']
# percentage of positive tweets
print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(senti)))
# picking negative tweets from tweets
ntweets = [final[i] for i in range(len(senti)) if senti[i]  == 'negative']
# percentage of negative tweets
print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(senti)))
# percentage of neutral tweets
neutweets = [final[i] for i in range(len(senti)) if senti[i]  == 'neutral']
print("Neutral tweets percentage: {} % \
         ".format(100*(len(neutweets))/len(senti)))

def wordcloud_draw(data, color = 'black'):
    words = ' '.join(data)
    cleaned_word = " ".join([word for word in words.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and not word.startswith('#')
                                and word != 'RT'
                            ])
    wordcloud = WordCloud(stopwords=STOPWORDS,
                      background_color=color,
                      width=2500,
                      height=2000
                     ).generate(cleaned_word)
    plt.figure(1,figsize=(13, 13))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    
print("Positive words")
wordcloud_draw(ntweets,'white')





