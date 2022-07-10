import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import csv
import numpy as np
import pandas as pd
import re
import string

from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score
from sklearn.cluster import KMeans

data_file='final_result_1_p-Copy_stop_eli.csv'
df=pd.read_csv(data_file, header=0, encoding="utf-8", engine='python')
questions=df['text_P'].tolist()

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text_P'].values.astype('U'))

true_k = 3
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

for i in range(true_k):
    print("Cluster %d:" % i),

    for ind in order_centroids[i, :15]:
        print(' %s' % terms[ind]),

    print('\n')

with open('final_result_1_p-Copy_stop_eli_3cluster.csv', mode='w') as employee_file:
    fieldnames = ['text_P', 'Group']
    employee_writer = csv.DictWriter(employee_file, fieldnames=fieldnames, lineterminator = '\n')
    employee_writer.writeheader()
    
    employee_writer = csv.writer(employee_file, quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

    for x2 in questions:
        x2=str(x2)
        Y = vectorizer.transform([x2])
        prediction = int(model.predict(Y))
        employee_writer.writerow([x2, prediction])
