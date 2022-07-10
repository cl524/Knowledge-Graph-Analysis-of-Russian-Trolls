
import pandas as pd
import csv
import re

from openie import StanfordOpenIE

with StanfordOpenIE() as client:
    data_file2='final_result_1_p-Copy_stop_eli.csv'
    df2=pd.read_csv( data_file2, header=0, encoding="utf-8", engine='python' )
    #df=df.sort_values('Sentences')
    questions2=df2['text'].tolist()

    for st2 in questions2:
        s2=""
        i=1

        for triple2 in client.annotate(str(st2)):
            s2=s2+str(triple2)