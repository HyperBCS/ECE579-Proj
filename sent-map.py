#!/usr/bin/python
import pyspark
import json
import time
import glob
from pyspark.sql import SparkSession
from pyspark.mllib.linalg.distributed import CoordinateMatrix, MatrixEntry
from pyspark.mllib.linalg import Matrix, Matrices
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sc = pyspark.SparkContext('local[*]')
spark = SparkSession(sc)
sia = SIA()

def filter(arg):
    dic  = json.loads(arg)
    if dic['score'] > 1000:
        return True
    return False

def mapper(arg):
    post = json.loads(arg)
    pol_score = sia.polarity_scores(post['title'])
    if pol_score['pos'] > pol_score['neg']:
        pol_score = 1
    elif pol_score['pos'] < pol_score['neg']:
        pol_score = -1
    else:
        pol_score = 0
    tm = post['created']
    month = time.strftime('%m', time.localtime(tm))
    return ((pol_score,month), 1)

def reducer(arg1, arg2):
    return arg1 + arg2

# Task 3
data_files = glob.glob('input/*')
rdds = []
for f in data_files:
    rdds.append(sc.textFile(f))
fr = sc.union(rdds).filter(filter).map(mapper)
frd = fr.reduceByKey(reducer)
dr = frd.collect()
for x in dr:
    print(x)