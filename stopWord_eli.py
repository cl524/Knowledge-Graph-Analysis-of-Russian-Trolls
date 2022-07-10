import nltk, string, csv, json, numpy as np, pandas as pd
import itertools, re

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=30000)

data_file='final_result_1_p-Copy.csv'
df=pd.read_csv(data_file, header=0, encoding="utf-8", engine='python')

o_sentence=df['text'].tolist()

o_ss=[]
for s1 in o_sentence:
    o_ss.append(str(s1))

filtered_sentence = []

stop_words = set(stopwords.words('english'))

def preprocessing(line):
    #line = line.lower()
    line = re.sub(r"[{}]".format(string.punctuation), "", line)
    return line

def lemmatize_corenlp(conn_nlp, sentence):
    props = {
        'annotators': 'lemma',
        'pipelineLanguage': 'en',
        'outputFormat': 'json'
    }

    sents = conn_nlp.word_tokenize(sentence)# tokenize into words

    #sents_no_punct = [s for s in sents if s not in string.punctuation] # remove punctuations from tokenised list

    sentence2 = " ".join(sents)

    parsed_str = conn_nlp.annotate(sentence2, properties=props) # annotate to get lemma
    #print(parsed_str)

    parsed_dict = json.loads(parsed_str)
    #print(parsed_dict)

    lemma_list = [v for d in parsed_dict['sentences'][0]['tokens'] for k,v in d.items() if k == 'lemma'] 
    # extract the lemma for each word

    return " ".join(lemma_list)


for example_sent in o_ss: #eliminate stop word
    example_sent=example_sent.lower()

    example_sent=re.sub("\'\S+", '', example_sent)
    example_sent=example_sent.replace("\\", "")

    example_sent = preprocessing(example_sent)

    example_sent=example_sent.strip()
    example_sent=re.sub(' +', ' ',example_sent)

    example_sent=lemmatize_corenlp(conn_nlp=nlp, sentence=example_sent)

    word_tokens=[]
    word_tokens = example_sent.split(' ')

    strs=""
    ind=0
    for w in word_tokens:
        if w not in stop_words and w.isnumeric()==False and w!="\\":

            strs=strs+w
            if ind<len(word_tokens)-1:
                strs=strs+" "
        ind+=1

    strs=strs.strip()
    strs=re.sub(' +', ' ',strs)

    filtered_sentence.append(strs) 

with open('final_result_1_p-Copy_stop_eli.csv', mode='w', encoding="utf-8") as employee_file:
    fieldnames = ['text', 'text_P']
    employee_writer = csv.DictWriter(employee_file, fieldnames=fieldnames, lineterminator = '\n')
    employee_writer.writeheader()

    employee_writer = csv.writer(employee_file, quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

    for (x1, x2) in zip(o_ss, filtered_sentence):
        s1=""+str(x1)
        s2=""+str(x2)

        employee_writer.writerow([s1, s2])