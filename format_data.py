from textblob import TextBlob
from operator import add
from pyspark.sql import SparkSession
from pyspark.mllib.linalg.distributed import CoordinateMatrix, MatrixEntry
from pyspark.mllib.linalg import Matrix, Matrices
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords

sia = SIA()
text = "Russian serial killer policeman found guilty of 56 more murders"
wiki = TextBlob(text)
print(sia.polarity_scores(text))
print(wiki.sentiment)