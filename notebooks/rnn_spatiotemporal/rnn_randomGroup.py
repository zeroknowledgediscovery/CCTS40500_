#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import collections
import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow.keras.layers import Dense, LSTM, TimeDistributed

from sklearn.metrics import roc_auc_score, roc_curve, auc

import rnn

meta = pd.read_csv('../data/meta.csv', index_col=0)
X_raw = np.genfromtxt('../data/CRIME-_2014-01-01_2016-12-31.csv')


choices = [
	[298, 304, 908, 1176, 453],  
	[281, 947, 203, 1443, 159],
	[870, 109, 103, 1206, 1084], 
	[615, 1013, 324, 470, 901],
	[1025, 260, 1106, 551, 82], 
	[903, 1137, 1477, 210, 388],
	[824, 270,  595, 269, 454],
	[291, 637, 930, 292, 360],
	[832, 29, 320, 498, 1181], 
	[1352, 732, 1164, 488, 1124]]


group = int(sys.argv[1])

future = 7
for r in choices[group]:
	center = meta.index[r]

	tile = meta.loc[center, ['lat1', 'lat2','lon1', 'lon2']]

	X_train, Y_train, X_test, Y_test = rnn.getData(meta, X_raw, center, future)

	model = rnn.train(X_train, Y_train, epochs=200)
	prediction = model.predict(X_test)
	
	figTitle = './results/random_100-10_200/' + '#'.join(map(str, tile.values)) + '_{}'.format(future)
	dfName = figTitle + '.rnnres'
	rnn.Analysis(Y_test, prediction, figTitle, dfName)
	# rnnres = rnn.flexroc(dfName)
	# print(rnnres)
