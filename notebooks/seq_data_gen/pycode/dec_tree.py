#!/usr/bin/python

import numpy as np
import pandas as pd
import subprocess
import os
import sys

import mlx as ml 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as stat 
import argparse
#import sparkline
import warnings
import tempfile
import operator
import pickle

warnings.filterwarnings("ignore")


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')



parser = argparse.ArgumentParser(description='Example with non-optional arguments')

parser.add_argument('--response', dest='RESPONSE', action="store", type=str,
                    default='SPECIES',help="Response Variable")
parser.add_argument('--file', dest='FILE', action="store", type=str,
                    default='../../data/database_may30_2017/AA_Human_20022003')
parser.add_argument('--filex', dest='FILEx', action="store", type=str,
                    default='../../data/database_may30_2017/AA_Human_20042005')
parser.add_argument('--ntree', dest='NUMTREE',
                    action="store", type=int,
                    default=300,help="Number of trees in rndom forest")
parser.add_argument('--cores', dest='CORES',
                    action="store", type=int,
                    default=10,help="Number of cores to use in rndom forest")
parser.add_argument('--sample', dest='SAMPLES',
                    action="store", type=int,default=10,help="sample size for columns")
parser.add_argument("--plot", type=str2bool, nargs='?',dest='PLOT_',
                    const=True, default=False,
                    help="Show plot")
parser.add_argument("--varimp", type=str2bool, nargs='?',dest='VARIMP',
                    const=True, default=False,
                    help="Feature importance")
parser.add_argument("--balance", type=str2bool, nargs='?',dest='BALANCE',
                    const=True, default=False,
                    help="Balance class frequency of reposnse variable")
parser.add_argument("--samplefeatures", type=str2bool, nargs='?',dest='SAMPLECOL',
                    const=True, default=False,
                    help="Choose a random sample of features")
parser.add_argument('--del', dest='DELETE',
                    action="store", type=str,nargs='+', default='',help="Deleted features")
parser.add_argument('--inconly', dest='INCLUDEONLY',
                    action="store", type=str,nargs='+',
                    default='',help="Included features, only")
parser.add_argument('--inc', dest='INCLUDE',
                    action="store", type=str,nargs='+', default='',help="Included features")
parser.add_argument("--verbose", type=str2bool, nargs='?',dest='VERBOSE',
                    const=True, default=False,
                    help="Verbose")
parser.add_argument('--treename', dest='TREENAME', action="store", type=str,
                    default='')
parser.add_argument('--zerodel', dest='ZERODEL',
                    action="store", type=str,nargs='+',
                    default='',
                    help="Delete rows where response is in zerodel")
parser.add_argument('--importance_threshold', dest='FEATURE_IMP_THRESHOLD',
                    action="store", type=float,
                    default=0.2,
                    help="Feature importance threshold: default 0.2")


results=parser.parse_args()
RESPONSE=results.RESPONSE
FILE=results.FILE
FILEx=results.FILEx
VERBOSE=results.VERBOSE
NUMTREE=results.NUMTREE
CORES=results.CORES
VARIMP=results.VARIMP
PLOT=results.PLOT_
DELETE=results.DELETE
INCLUDE=results.INCLUDE
INCLUDEONLY=results.INCLUDEONLY
TREENAME=results.TREENAME
SAMPLES=results.SAMPLES
BALANCE=results.BALANCE
SAMPLECOL=results.SAMPLECOL
ZERODEL=results.ZERODEL
FEATURE_IMP_THRESHOLD=results.FEATURE_IMP_THRESHOLD
#RESPONSE = map(ml.nameclean,RESPONSE)
#RESPONSE='P10'
print RESPONSE
#------------------------------
#------------------------------
RS=RESPONSE
if INCLUDE != "":
    INCLUDE=list(set(list(set(INCLUDE)).extend(RS)))
    
INPUTFILE_=""
    
datatrain=ml.setdataframe(FILE,outname=INPUTFILE_,
                          delete_=DELETE,
                          include_=INCLUDEONLY,
                          select_col=SAMPLECOL,
                          rand_col_sel=SAMPLES,
                          response_var=RS,
                          balance=BALANCE,
                          zerodel=ZERODEL)

datatest=ml.setdataframe(FILEx,
                         include_=datatrain.columns,
                         response_var=RS,
                         zerodel=ZERODEL)

CT,Pr,ACC,CF,Prx,ACCx,CFx,TR=ml.Xctree(RESPONSE__=RESPONSE,
                                       datatrain__=datatrain,
                                       datatest__=datatest,
                                       VERBOSE=VERBOSE,
                                       TREE_EXPORT=False)
if TR is not None:
    sorted_feature_imp = sorted(TR.significant_feature_weight_.items(),
                                key=operator.itemgetter(1))
    for i in sorted_feature_imp:
        if i[1] > FEATURE_IMP_THRESHOLD:
            print i[0],RS[0],i[1]
else:
    print "XX",RS[0],0.0

print TR.num_pass_
ml.tree_export(TR,outfilename=TREENAME+'.dot')


with open('tree.pkl', 'wb') as f:
    pickle.dump(TR, f)


sys.stdout.write(ml.RESET)
#------------ EOF
 
