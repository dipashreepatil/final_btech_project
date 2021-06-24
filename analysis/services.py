import os
from nltk.tokenize import word_tokenize
import requests
import pandas as pd
import tweepy as tw
from sqlalchemy import create_engine
import sqlalchemy
import MySQLdb
import pymysql
import numpy as np
import spacy
import re
import preprocessor as p
from keras.preprocessing.sequence import pad_sequences

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from django.db import IntegrityError
import yfinance as yf
from datetime import timedelta
from datetime import date



def normalization(clean_list):
    lem = WordNetLemmatizer()
    normalized_list = []
    for word in clean_list:
        normalized_txt = lem.lemmatize(word,'v')
        normalized_list.append(normalized_txt)
    return normalized_list

def remove_stopwords_normalize(tweet):
    tweet_list = [elem for elem in tweet.split()]
    clean_list = [word for word in tweet_list if word.lower() not in stopwords.words('english')]
    normalized_list = normalization(clean_list)
    new_txt = " ".join([word for word in normalized_list])
    return new_txt

def preprocess(tweets_list):
    df1 = pd.DataFrame(tweets_list, columns = ['id','date','company','text','place','retweets_count','favorites_count','user_name','followers_count'])
  
    
    for i in range(len(df1)):
        txt = df1.loc[i]["text"]
        user = df1.loc[i]["user_name"]
        user = re.sub(r'[^a-zA-Z0-9_]', '', user)
        txt = txt.lower()
        txt=re.sub('@[A-Z0-9a-z_:]+','',txt)#replace username-tags
        txt=re.sub('^RT+','',txt)#replace RT-tags
        txt = re.sub('https?://[A-Za-z0-9./]+','',txt)#replace URLs
        txt=re.sub("[^a-zA-Z]", " ",txt)#replace hashtags
        df1.at[i,"preprocessed_text"]=txt
        df1.at[i, "user_name"] = user
         
        txt = df1['preprocessed_text'].iloc[i]
        new_txt = remove_stopwords_normalize(txt)
        df1.at[i,"preprocessed_text"] = new_txt
        
    df1 = df1.drop_duplicates(['preprocessed_text'])
    return df1

def preprocess_news(news_list):
  df2 = pd.DataFrame(news_list,columns=['date','company','title','description','content'])
  for i in range(len(df2)):
        txt = df2.loc[i]["content"]
        txt = txt.lower()
        txt=re.sub('^RT+','',txt)#replace RT-tags
        txt = re.sub('https?://[A-Za-z0-9./]+','',txt)#replace URLs
        df2.at[i,"preprocessed_content"]=txt         
        txt = df2['preprocessed_content'].iloc[i]
        new_txt = remove_stopwords_normalize(txt)
        df2.at[i,"preprocessed_content"] = new_txt
        
  
  return df2

def collect_news(search_words):
    from_date = "2021-06-20"
      #to_date = "2021-05-10"
    url = ('http://newsapi.org/v2/everything?'
       'q={}&'
       'from={}&'
       'sortBy=popularity&'
       'apiKey=82cb329eecdf4725b4d599b626d24411').format(search_words,from_date)
        
    response = requests.get(url)
    ft_dict = response.json()
    news_data = ft_dict['articles']
    news_list = []
    company = search_words
    for news in news_data:
      lst = []
      lst.extend((news['publishedAt'],company,news['title'],news['description'],news['content']))
      news_list.append(lst)

    df = preprocess_news(news_list) # preprocess data

  
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                .format(user="root",
                        pw="",
                        db="text_data")) 
   # Insert whole DataFrame into MySQL without duplicate entries
    for i in range(len(df)):
      try: 
        df.iloc[i:i+1].to_sql('news_table', con =engine, if_exists = 'append', chunksize = 1000,index=False)
      except sqlalchemy.exc.IntegrityError:
        continue                    

   

def collect_tweets(search_words):
        search_words = search_words
        
        # API keys assigned after creating a project using tweepy api on twitter developer site
        api_key = 'bXa3bAs7M4O1d9a3wCyYRq5dn'
        api_secret_key = 'IMXOI0vFU9KhN8Fnjm04K7NCRK6EGy5nxSUuh8FR07s78pHd65'
        access_token = '1300274872958873600-bMOVNLomg5ZZxLLA19AMShgGxB3Xrw'
        access_token_secret = 'oN3gya8E0OVJVD6Q2UTlMJrWrHAELy115qngQweYI80CJ'

        # Connect to Twitter API using the secrets
        auth = tw.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tw.API(auth, wait_on_rate_limit=True) #wait_on_rate_limit=True to avoid tweeter error status code 429(invalid url error)
        today = date.today()
        
        company = search_words.split()[0]
        tweets_data = tw.Cursor(api.search,q=search_words,lang="en",since="2021-06-20").items(800)
        tweets_list=[]

        for tweet in tweets_data:         
            lst = []
            lst.extend((tweet.id,tweet.created_at,company,tweet.text,tweet.place,tweet.retweet_count,tweet.favorite_count,tweet.user._json['name'],tweet.user._json['followers_count']))
            tweets_list.append(lst) 

       
        df = preprocess(tweets_list) # preprocess data

        # create sqlalchemy engine
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 
        print(df)
        # Insert whole DataFrame into MySQL without duplicate entries
        for i in range(len(df)):
              try: 
                df.iloc[i:i+1].to_sql('tweets_table', con =engine, if_exists = 'append', chunksize = 1000,index=False)
              except sqlalchemy.exc.IntegrityError:
                continue
        #df.to_sql('tweets_table', con =engine, if_exists = 'append', chunksize = 1000,index=False)
        
       

def collect_stock_indices():
              
        df = yf.download(tickers = "AMZN AAPL MSFT GOOGL GME IBM TSLA JPM FB NFLX",
                          interval = "60m",
                          start=date.today()-timedelta(days=7),end=date.today())
        df1 = df.loc[:, [('Close', 'AMZN'),('Close',  'AAPL'),('Close', 'MSFT'),('Close', 'GOOGL'),('Close', 'GME'),('Close', 'IBM'),('Close', 'TSLA'),('Close', 'JPM'),('Close', 'FB'),('Close', 'NFLX')]]
        df1.columns = df1.columns.droplevel()
        df1['Datetime'] = df.index
        df1 = df1[['Datetime','AMZN','AAPL','MSFT','GOOGL','GME','IBM','TSLA','JPM','FB','NFLX']]
         # create sqlalchemy engine
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="numeric_data")) 

        df1.to_sql('stock_indices', con =engine, if_exists = 'replace', chunksize = 1000,index=False)


def create_tokens_list(df):
      # text_lines is list of list consisting of tokens of each line
  text_tokens_list = list()
  lines = df['text'].values.tolist() # list of all news
  
  for line in lines:
    tokens = word_tokenize(line)
    text_tokens_list.append(tokens) # lists of lists containing tokens of a news headline

  return text_tokens_list

def create_sequences(text_tokens_list):
  #vectorize text samples into 2D tensor
  tokenizer_obj = Tokenizer()
  tokenizer_obj.fit_on_texts (text_tokens_list)
  sequences = tokenizer_obj.texts_to_sequences(text_tokens_list) 
  return sequences



def padding_sequences(df,sequences,max_length):
  text_pad = pad_sequences(sequences, maxlen = max_length)

  print("Shape of text tensor: ", text_pad.shape)
  return text_pad

def create_embedding_index(filepath):
      #Embedding index stores word2vec for each word in key-value pair format
  embedding_index = {}
  f = open(os.path.join('', filepath), encoding = "utf-8")
  for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:])
    embedding_index[word] = coefs
 
  f.close()
  return embedding_index
  
def prepare_test_set(df):
      
  
  #train word2vec model
  EMBEDDING_DIM = 300
  text_tokens_list = create_tokens_list(df)
  
  #save word2vec model
  #model.wv.save_word2vec_format("demo_project\\analysis\\models\\embedding_word2vec.txt", binary = False)
  sequences = create_sequences(text_tokens_list)

  MAX_SEQUENCE_LENGTH = 100
  text_pad = padding_sequences(df,sequences,MAX_SEQUENCE_LENGTH)
  return text_pad