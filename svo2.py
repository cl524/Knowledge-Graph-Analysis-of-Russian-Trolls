
import pandas as pd
import csv
import re

from openie import StanfordOpenIE

with StanfordOpenIE() as client:
    '''
    data_file='final_result_1_p.csv'
    df=pd.read_csv(data_file, header=0, encoding="utf-8", engine='python')
    #df=df.sort_values('Sentences')
    questions=df['text'].tolist()
    #questions=list(set(filter(None, questions)))
    #questions.sort()


    with open('final_result_1_p_SVO.csv', mode='w', encoding="utf-8") as f:
        fieldnames = ['triples']
        f_writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator = '\n')
        f_writer.writeheader()
        
        f_writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

        for st in questions:
            s1=""
            i=1
            for triple in client.annotate(str(st)):
                s1=s1+str(triple)
                if i==10:
                    break 
                    #print(type(triple))
                i+=1
            
            s1=s1.strip()
            f_writer.writerow([str(s1)])
    '''
######################################################################################################################

    data_file2='final_result_1_p-Copy_stop_eli.csv'
    df2=pd.read_csv( data_file2, header=0, encoding="utf-8", engine='python' )
    #df=df.sort_values('Sentences')
    questions2=df2['text'].tolist()
    #questions=list(set(filter(None, questions)))
    #questions.sort()

    with open('final_result_1_p-Copy_stop_eli_SVO.csv', mode='w', encoding="utf-8") as f2:
        fieldnames2 = ['triples']
        f_writer2 = csv.DictWriter(f2, fieldnames=fieldnames2, lineterminator = '\n')
        f_writer2.writeheader()
        
        f_writer2 = csv.writer(f2, quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

        for st2 in questions2:
            s2=""
            i=1

            for triple2 in client.annotate(str(st2)):
                s2=s2+str(triple2)
                if i==10:
                    break

                i+=1
            
            s2=s2.strip()
            f_writer2.writerow([str(s2)])