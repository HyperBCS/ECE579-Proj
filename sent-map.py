#!/usr/bin/python
import pyspark
import json
import time
import glob
import re
from operator import add
from pyspark.sql import SparkSession
from pyspark.mllib.linalg.distributed import CoordinateMatrix, MatrixEntry
from pyspark.mllib.linalg import Matrix, Matrices
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sc = pyspark.SparkContext('local[*]')
spark = SparkSession(sc)
sia = SIA()
sub_filter = ['news', 'worldnews', 'politics', 'wow', 'destinythegame','leagueoflegends', 'overwatch','globaloffensive','the_donald','minecraft']


def filter(arg):
    dic  = json.loads(arg)
    try:
	    if dic['score'] > 500 and dic['subreddit'].lower() in sub_filter:
	        return True
    except:
    	return False
    return False

def clean_post(txt):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \.\'\t])|(\w+:\/\/\S+)", " ", txt).split())

def mapper(arg):
    post = json.loads(arg)
    post_txt = clean_post(post['title'])
    pol_score = sia.polarity_scores(post_txt)
    res_score = [0,0,0]
    if pol_score['pos'] > pol_score['neg']:
        res_score[2] = 1
    elif pol_score['pos'] < pol_score['neg']:
        res_score[0] = 1
    else:
        res_score[1] = 1
    tm = post['created_utc']
    month = time.strftime('%m-%y', time.localtime(tm))
    return ((post['subreddit'],month), res_score)

def reducer(arg1, arg2):
    return list(map(add,arg1,arg2))

# Task 3
data_files = glob.glob('input/*')
rdds = []
for f in data_files:
    rdds.append(sc.textFile(f))
fr = sc.union(rdds).filter(filter).map(mapper)
frd = fr.reduceByKey(reducer)
dr = frd.collect()

print("\n%s\t%s\t%s\t%s\t%s"%("subreddit","date","neg","neu","pos"))
for x in dr:
    subr = x[0][0]
    date = x[0][1]
    num = x[1]
    print("%s\t%s\t%s\t%s\t%s"%(subr,date,num[0],num[1],num[2]))