import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import string

from spacy.symbols import ORTH
from collections import Counter
from bs4 import BeautifulSoup
from functools import reduce
import nltk
import nltk.data
import pandas as pd
import csv
import re

from pycorenlp import StanfordCoreNLP
from nltk.tokenize import sent_tokenize, word_tokenize

data_file='final_result_1_p-Copy_stop_eli.csv'
df=pd.read_csv( data_file, header=0, encoding="ISO-8859–1", engine='python' )
#df=df.sort_values('Sentences')

questions=df['text'].tolist()
#questions=list(filter(None, questions))


'''
def preprocessing(line):
    #line = line.lower()
    line = re.sub(r"[{}]".format(string.punctuation), " ", line)
    return line
'''

'''
def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 128)
    return ''.join(stripped)

def deCamel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)

def alphaDig(name):
    s1 = re.sub('([A-Za-z])([0-9]+)', r'\1 \2', name)
    return re.sub('([0-9])([A-Za-z])', r'\1 \2', s1)

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]

res=[]
for sstt in questions:

    sstt=str(sstt)
    sstt=strip_non_ascii(sstt)

    sstt=re.sub("RT", ' ', sstt)
    sstt=re.sub("http\S+", ' ', sstt)
    sstt=re.sub("\S+.com\S*", ' ', sstt)

    sstt=re.sub("@\S+:", "", sstt)
    sstt=re.sub('(\S+\:)(\S+)', r'\1 \2', sstt)
    sstt=re.sub("\S+\:\s+", " ", sstt)

    sstt=re.sub("\s+\.", '', sstt)
    sstt=re.sub('([!@?.,])([!@?.,]+)', r'\1', sstt)
    
    sstt=re.sub("[#@]", "", sstt)

    sstt=re.sub(' +', ' ',sstt)
    sstt=sstt.strip()
    
    sstt=re.sub("&amp", " ", sstt)

    sstt=re.sub(' +', ' ',sstt)
    sstt=sstt.strip()
    
    sstt=deCamel(sstt)
    sstt=alphaDig(sstt)
    sstt=deEmojify(sstt)

    sstt=re.sub( "(\s+)([;:,?.!])", r'\2', sstt)
    sstt=re.sub( "[.!?]", ";", sstt)

    sstt=re.sub('(\n)(\s+)', r'\1', sstt)
    sstt=re.sub('(\s+)(\n)', r'\2', sstt)

    sstt=re.sub(' +', ' ',sstt)
    sstt=sstt.strip()
    
    res.append(sstt)

#res=unique(res)
'''


nlp = StanfordCoreNLP('http://localhost:9000')

with open('final_result_1_p-Copy_stop_eli_senti_re_P_Q_E.csv', mode='w', encoding="utf-8") as employee_file:
    fieldnames = ['text', 'sentiment']
    
    employee_writer = csv.DictWriter(employee_file, fieldnames=fieldnames, lineterminator = '\n')
    employee_writer.writeheader()
    employee_writer = csv.writer(employee_file, quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
    
    for sstt in questions:
        stt=str(sstt)
        stt=re.sub("[?.!]", ";", stt)

        if(len(stt)>0):
            res = nlp.annotate(stt, properties={ 'annotators': 'sentiment', 'outputFormat': 'json' } )

            for s in res["sentences"]:
                employee_writer.writerow([stt, s["sentiment"]])
        else:
            employee_writer.writerow(["N/a", "N/a"])