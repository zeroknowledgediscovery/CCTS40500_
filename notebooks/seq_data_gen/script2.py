import seqpull as sq
import pandas as pd
import pylab as plt
import numpy as np
import cPickle

#recordfile='SARS-CoV-2.rec'
#pkl_file=open(recordfile,'rb')
#records_sars=pickle.load(pkl_file)
#[SF,SFi]=sq.procSequence(records_sars,
#                         begIndex=21563,endIndex=25384,
#                         N=5000,LMAX=35000,
#                         integer_dataframe=True,heatmap=True)

recordfile='2019-nCoV.rec'
pkl_file=open(recordfile,'rb')
records_covid=cPickle.load(pkl_file)
[SFnc,SFinc]=sq.procSequence(records_covid,
                             begIndex=21563,endIndex=25384,
                             N=6000,LMAX=35000,
                             integer_dataframe=True,heatmap=False)
SFnc.to_csv('covid19.csv',index=None)


recordfile='betacoronav.rec'
pkl_file=open(recordfile,'rb')
records_covid=cPickle.load(pkl_file)
[SFnc,SFinc]=sq.procSequence(records_covid,
                             begIndex=21563,endIndex=25384,
                             N=6000,LMAX=35000,
                             integer_dataframe=True,heatmap=False)
SFnc.sample(1000).to_csv('betacorona.csv',index=None)


#accession_ncov=list(set(list(SFnc.accession.values)).intersection(set(list(SF.accession.values))))
