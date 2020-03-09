#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function, unicode_literals

import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
# import collections

import os
import subprocess
import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow.keras.layers import Dense, LSTM, TimeDistributed

from sklearn.metrics import roc_auc_score, roc_curve, auc


def getData(meta, X_raw, tgt, future):
	"""
	Let us say that target 'tgt' is the index of a tile, 
	so we predict for all three variables, CASE
	"""
	
	AR = meta.loc[tgt, 'CASE']
	#PR = meta.loc[tgt, 'BURGLARY-THEFT-MOTOR_VEHICLE_THEFT']
	#AS = meta.loc[tgt, 'HOMICIDE-ASSAULT-BATTERY']
	
	#print('Arrest: {},\nProperty: {},\nAssault: {}.'.format(AR, PR, AS))
	
	X = X_raw.T
	Y = X_raw[[AR]].T

	# get train and test
	# Train is the first two years (2014, 2015), so of length 365 * 2 = 730
	# test is the last year (2016, a leap year), so of length 366
	X_train = X[:30 - future]
	Y_train = Y[future: 30]

	X_test = X[30 - future: -future]
	Y_test = Y[30:]
	
	# Reshape to fit RNN
	# The dimension of RNN input/output is (num_samples, length_in_time, data_dimension)
	X_train = X_train.reshape(1, *X_train.shape)
	Y_train = Y_train.reshape(1, *Y_train.shape)

	X_test = X_test.reshape(1, *X_test.shape)
	Y_test = Y_test.reshape(1, *Y_test.shape)
	
	print('Training data: input dim = {}, output dim = {}'.format(X_train.shape, Y_train.shape))
	print('Out-sample data: input dim = {}, output dim = {}'.format(X_test.shape, Y_test.shape))

	return X_train, Y_train, X_test, Y_test


def train(X_train, Y_train, epochs=200):

	model = tf.keras.Sequential()

	# Don't use unless you are sure test length is the same
	# as the train length, which is not the case for us
	# model.add(tf.keras.Input(X_train.shape[1:]))  

	# Two LSTM layers
	model.add(LSTM(units=30, input_shape=(None, X_train.shape[-1]), return_sequences=True))
	model.add(LSTM(units=10, return_sequences=True))
	
	# One output layers
	model.add(TimeDistributed(Dense(units=1, activation='sigmoid')))
	
	model.compile(loss='mse', optimizer='adam')

	model.summary()

	model.fit(X_train, Y_train, epochs=epochs, batch_size=1, verbose=1)
	
	return model


def train_3(X_train, Y_train, epochs=200):

	model = tf.keras.Sequential()

	# Don't use unless you are sure test length is the same
	# as the train length, which is not the case for us
	# model.add(tf.keras.Input(X_train.shape[1:]))  

	# Two LSTM layers
	model.add(LSTM(units=50, input_shape=(None, X_train.shape[-1]), return_sequences=True))
	model.add(LSTM(units=10, return_sequences=True))
	model.add(LSTM(units=10, return_sequences=True))
	
	# One output layers
	model.add(TimeDistributed(Dense(units=1, activation='sigmoid')))
	
	model.compile(loss='mse', optimizer='adam')

	model.summary()

	model.fit(X_train, Y_train, epochs=epochs, batch_size=1, verbose=1)
	
	return model



def Analysis(Y_test, prediction, figTitle, dfName):
  
	categories = ['CASE']
	
	fig, axes = plt.subplots(1, 1, figsize=(12, 4))
	res = {}
	for c, t, p, ax in zip(categories, Y_test[0].T, prediction[0].T, axes):
		res[c + '_grt'] = t.astype(int)
		res[c + '_prd'] = p

		y_true = t
		y_true[t > 0] = 1
		fpr, tpr, thresholds = roc_curve(y_true, p, pos_label=1)


		ax.plot(fpr, tpr)
		ax.set_aspect('equal')
		# plt.title(figTitle + '_' + c)
		ax.text(.05, .9, '{}, auc={:.3f}'.format(c, auc(fpr, tpr)), 
				 ha='left', 
				 va='bottom', 
				 transform=ax.transAxes, 
				 fontsize=15)
		ax.tick_params(labelsize=12)
	
	fig.suptitle(figTitle, fontsize=20)
	plt.savefig(figTitle + '.png', dpi=200, bbox_inches='tight')
	plt.show()
	
	resDf = pd.DataFrame(res)
	resDf.index = pd.date_range(start='1/1/2020', end='2/28/2016')
	resDf.to_csv(dfName)



def flexroc(fname):
	
	"""
	
	"""
	
	FLEXROC = '/home/yhuang10/Spatio-Temporal/cynet_/bin/flexroc'
	
	RES = {}
	
	h = np.array(fname.split('/')[-1].split('_')[0].split('#')).astype(float)
	RES['lat1'], RES['lat2'], RES['lon1'], RES['lon2'] = h 
	df = pd.read_csv(fname)

	df[['AR_grt','AR_prd']].to_csv('tmp.csv', header=None, index=None, sep=' ')
	cmd = '{} -i tmp.csv -w 1 -x 0 -t 0.8 -f 0.2 -E 0 -C 1 -L 1'.format(FLEXROC)
	result = subprocess.check_output(cmd, shell=True).decode('ascii')
	RES['VAR'] = float(result.split()[1])
	
	df[['AS_grt','AS_prd']].to_csv('tmp.csv', header=None, index=None, sep=' ')
	cmd = '{} -i tmp.csv -w 1 -x 0 -t 0.8 -f 0.2 -E 0 -C 1 -L 1'.format(FLEXROC)
	result = subprocess.check_output(cmd, shell=True).decode('ascii')
	RES['HOMICIDE-ASSAULT-BATTERY'] = float(result.split()[1])
	
	df[['PR_grt','PR_prd']].to_csv('tmp.csv',header=None,index=None,sep=' ')
	cmd = '{} -i tmp.csv -w 1 -x 0 -t 0.8 -f 0.2 -E 0 -C 1 -L 1'.format(FLEXROC)
	result = subprocess.check_output(cmd, shell=True).decode('ascii')
	RES['BURGLARY-THEFT-MOTOR_VEHICLE_THEFT'] = float(result.split()[1])
	
	os.system('rm tmp.csv')
	
	return RES




if __name__ == '__main__':
	RES = flexroc('results/top10_deeper/41.75704#41.7598#-87.65729#-87.65377_7.rnnres')
	print(RES)
