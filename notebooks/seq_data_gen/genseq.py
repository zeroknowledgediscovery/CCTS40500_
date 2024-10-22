import seqpull as sq
import pandas as pd
import pylab as plt
import numpy as np
import pickle

recordfile='SARS-CoV-2.rec'
pkl_file=open(recordfile,'rb')
records_sars=pickle.load(pkl_file)

[SF,SFi]=sq.procSequence(records_sars,
                 begIndex=21563,endIndex=25384,
                         N=5000,LMAX=35000,integer_dataframe=True,heatmap=False)

SF.to_csv('corona.csv',index=None)
