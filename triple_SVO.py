import pandas as pd
import csv, re, json, string
from stanfordcorenlp import StanfordCoreNLP

def lemmatize_corenlp(conn_nlp, sentence):
    props = {
        'annotators': 'pos,lemma',
        'pipelineLanguage': 'en',
        'outputFormat': 'json'
    }

    sents = conn_nlp.word_tokenize(sentence)# tokenize into words

    sents_no_punct = [s for s in sents if s not in string.punctuation] # remove punctuations from tokenised list

    sentence2 = " ".join(sents_no_punct)# form sentence
    
    parsed_str = conn_nlp.annotate(sentence2, properties=props) # annotate to get lemma
    #print(parsed_str)
    
    parsed_dict = json.loads(parsed_str)
    #print(parsed_dict)
    
    lemma_list = [v for d in parsed_dict['sentences'][0]['tokens'] for k,v in d.items() if k == 'lemma'] # extract the lemma for each word

    return " ".join(lemma_list)

data_file='covid_pdata_pos_p_SVO_SENTI_covid.csv'
df=pd.read_csv(data_file, header=0, encoding="utf-8", engine='python')

wholelist=df['Triples'].tolist()
sentimentlist=df['Sentiment'].tolist()

i=1
nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=30000)

with open('covid_pdata_pos_p_SVO_SENTI_covid_lemma.csv', mode='w', encoding="utf-8") as f:
    fieldnames = ['subject', 'relation', 'object', 'sentiment']

    f_writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator = '\n')
    f_writer.writeheader()
    f_writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

    for (everystringinlist, sentiment) in zip(wholelist, sentimentlist):
        subject=""
        relation=""
        objectt=""

        thisstring=""

        if "@@@" in everystringinlist:
            maxlen=0
            singlelist=str(everystringinlist).split("@@@")
            #print(singlelist)

            for astring in singlelist:
                lowstring=astring.lower()
                if "covid" in lowstring and len(astring)>maxlen:
                    thisstring=str(astring)
                    maxlen=len(astring)
        
            resstring=str(thisstring.strip('{}'))
            reslist=resstring.split(", ")

            subject=reslist[0][12:-1]
            relation=reslist[1][13:-1]
            objectt=reslist[2][11:-1]


        else:
            singlelist=str(everystringinlist).split(",")
            #print(singlelist)
            subject=singlelist[0][13:-1]
            relation=singlelist[1][14:-1]
            objectt=singlelist[2][12:-2]
        
        if( (re.search('[a-zA-Z0-9]', subject)==None) or (re.search('[a-zA-Z0-9]', relation)==None) or (re.search('[a-zA-Z0-9]', objectt)==None) ):
            continue
        else:
            subjectlemma = lemmatize_corenlp(conn_nlp=nlp, sentence=subject.lower())
            relationlemma = lemmatize_corenlp(conn_nlp=nlp, sentence=relation.lower())
            objectlemma = lemmatize_corenlp(conn_nlp=nlp, sentence=objectt.lower())

            print(subjectlemma, relationlemma, objectlemma)
            f_writer.writerow([str(subjectlemma), str(relationlemma), str(objectlemma), str(sentiment)])
            
            singlelist=[]
            
            print("\n")
'''
the_string=" ---123"
print(re.search('[a-zA-Z0-9]', the_string))
'''