from Bio import Entrez
import pickle
import numpy as np
import pandas as pd
import pylab as plt
import seaborn as sns

def getRecord(organism,recordfile=None):
    #get an id list: this makes a big search and gets a list of id 
    # ned to use some email doesnt matter what
    Entrez.email ="ishanu@uchicago.edu"
    handle = Entrez.esearch(db='nucleotide', term = [organism], retmax=100000)
    record = Entrez.read(handle)
    handle.close()
    handle = Entrez.efetch(db="nucleotide", id=record["IdList"], retmode="xml")
    records = Entrez.read(handle)
    # pickle the records since the download takes time
    if recordfile is None:
        recordfile=organism.split('[')[0]+'rec'
    with open(recordfile,'wb') as f:
        pickle.dump(records,f,protocol=2)                      
    f.close() 
    return recordfile,len(record["IdList"])

def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.iteritems():
            if k == lookup_key:
                #print v
                yield v
                break
            else:
                for child_val in item_generator(v, lookup_key):
                    #print child_val
                    yield child_val
                    break
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, lookup_key):
                #print item_val
                yield item_val
                break
                
def item_generator_nobreak(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.iteritems():
            if k == lookup_key:
                yield v
            else:
                for child_val in item_generator_nobreak(v, lookup_key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator_nobreak(item, lookup_key):
                yield item_val

def procSequence(records,
                 begIndex=0,endIndex=1500,
                 N=10,LMAX=35000,integer_dataframe=False,
                 heatmap=False):              
    S=[]
    ACC=[]
    count=0
    for i in records:
        beg=[ x for x in item_generator(i,'GBInterval_from')][0]
        end=[ x for x in item_generator(i,'GBInterval_to')][0]
        seq=[ x for x in item_generator(i,'GBSeq_sequence')][0]
        acc=[ x for x in item_generator(i,'GBSeq_primary-accession')][0]

        xbeg=''.join('x' for i in np.arange(int(beg)))
        xend=''.join('x' for i in np.arange(LMAX-int(end)))
        seq=xbeg+seq+xend
        seq=seq[begIndex:endIndex]
        S=np.append(S,seq)
        ACC=np.append(ACC,acc)
        if count > N:
            break
        else:
            count=count+1
            
    SF=pd.DataFrame([list(x) for x in S]).replace('x',np.nan)
    SF['accession']=ACC
    SF=SF.dropna(how='all',axis=1)
    
    if heatmap:
        integer_dataframe=True
    if integer_dataframe:
        SFi=SF.fillna(-1).drop('accession',axis=1)#.values.astype(int) 
        values=np.unique(SFi.values)
        extra_values=set(values)-set(['-1','a','t','g','c','A','T','G','C'])
        for v in extra_values:
            SF=SF.replace(v,np.nan)
        SFi=SF.replace('a','0').replace('A','0').replace('t','1').replace('T','1').replace('g','2').replace('G','2')\
                .replace('c','3').replace('C','3').fillna(-1).drop('accession',axis=1).values.astype(int)
        if heatmap:
            sns.clustermap(SFi,cmap='jet')
        return SF,SFi
    return SF


def getInfo(record,VERBOSE=False):
    key=[]
    value=[]
    for i in item_generator_nobreak(record,'GBQualifier_name'):
        key=np.append(key,i)
    for i in item_generator_nobreak(record,'GBQualifier_value'):
        value=np.append(value,i)
    INFO={}
    if VERBOSE:
        print(key)
    for i  in zip(key,value):
        INFO[i[0]]=i[1]
    return INFO