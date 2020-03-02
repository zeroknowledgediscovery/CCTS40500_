#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function, unicode_literals

import collections

import sys
import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow.keras.layers import Dense, LSTM, TimeDistributed

from sklearn.metrics import roc_auc_score, roc_curve, auc

import rnn

meta = pd.read_csv('../data/meta.csv', index_col=0)
X_raw = np.genfromtxt('../data/CRIME-_2014-01-01_2016-12-31.csv')

cynetTop = [
    '41.8828#-87.7435', '41.7584#-87.6555', 
    '41.8828#-87.6274', '41.7750#-87.6520', 
    '41.9104#-87.7048', '41.7446#-87.6520',
    '41.9270#-87.7364', '41.7833#-87.5957', 
    '41.9823#-87.6555', '41.8275#-87.6168'
]


center = cynetTop[int(sys.argv[1])]
tile = meta.loc[center, ['lat1', 'lat2','lon1', 'lon2']]
    
future = 7
    
X_train, Y_train, X_test, Y_test = rnn.getData(meta, X_raw, center, future)

model = rnn.train_3(X_train, Y_train, epochs=200)
prediction = model.predict(X_test)


figTitle = 'results/top10_deeper/' + '#'.join(map(str, tile.values)) + '_{}'.format(future)
dfName = figTitle + '.rnnres'
rnn.Analysis(Y_test, prediction, figTitle, dfName)
res = rnn.flexroc(dfName)
print(res)

# future = 7
# RES = []
# for center in cynetTop:
#     tile = meta.loc[center, ['lat1', 'lat2','lon1', 'lon2']]
# 
#     X_train, Y_train, X_test, Y_test = rnn.getData(meta, X_raw, center, future)
# 
#     model = rnn.train_3(X_train, Y_train, epochs=200)
#     prediction = model.predict(X_test)
#     
#     figTitle = '#'.join(map(str, tile.values)) + '_{}'.format(future)
#     dfName = 'results/top10_deeper/' + figTitle + '.rnnres'
#     rnn.Analysis(Y_test, prediction, figTitle, dfName)
#     rnnres = flexroc(dfName)
#     RES.append(rnnres)
# 
# 
# 
# cynet = pd.read_csv('../data/cynet_performance.csv').round(4)
# rnn = pd.DataFrame(data=RES)
# rnn = rnn.set_index(['lat1','lat2','lon1','lon2']).stack().reset_index().rename(columns={'level_4':'var',0:'auc_NN'}).round(4)
# df = cynet.set_index(['lat1','lat2','lon1','lon2','var']).join(rnn.set_index(['lat1','lat2','lon1','lon2','var'])).reset_index().dropna()
# 
# 
# sns.distplot(df.auc)
# sns.distplot(df.auc_NN)
# plt.show()
# 
# 
# random = [ 
#     298, 304, 908, 1176, 453,  
#     281, 947, 203, 1443, 159,  
#     870, 109, 103, 1206, 1084, 
#     615, 1013, 324, 470, 901,
#     1025, 260, 1106, 551, 82, 
#     903, 1137, 1477, 210, 388,
#     824, 270,  595, 269, 454,
#     291, 637, 930, 292, 360,
#     832, 29, 320, 498, 1181, 
#     1352, 732, 1164, 488, 1124
# ]

