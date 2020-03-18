import seqpull as sq
import pandas as pd
import pylab as plt
import numpy as np
import pickle

organism="2019-nCoV[Orgn]"
recordfile,num=sq.getRecord(organism)
pkl_file=open(recordfile,'rb')
records_cov=pickle.load(pkl_file)
[SFnc,SFinc]=sq.procSequence(records_cov,
                 begIndex=21563,endIndex=25384,
                 N=6000,LMAX=35000,integer_dataframe=True,heatmap=True)

SFnc.to_csv('covid19.csv',index=None)
