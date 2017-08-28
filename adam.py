#!/usr/bin/python

'''
Created on Aug 15, 2017

@author: Leon (Jobs), Junaid (Woz)
'''
import pandas as pd
import numpy as np
import random as rrand
import math as math
import operator
from pandas_datareader import data as dreader
from sklearn.preprocessing import Normalizer 
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import sklearn.linear_model as lm
from sklearn.linear_model import Ridge

from pylab import * #Used to calculate Mean and maybe more stuff didn't check, can probably replace/get rid of it

stocks = "AAPL"
testNum = 120

def normalize(lst):
    s = (np.array(lst) - np.amin(lst))/(np.amax(lst) - np.amin(lst))
    return s

#getting the stock info [Date, Open, High, Low, Close, Volume]
allData_temp = dreader.DataReader(stocks,'google','2008-01-01','2017-08-27')
allData_temp.to_csv('data/'+str(stocks)+'.csv')

allData = pd.read_csv('data/'+str(stocks)+'.csv')
#print allData.Date

#Very dumb way to do it. but hell.. just wanna get it to work first 
allYear = [i.split('-')[0] for i in allData.Date]
allMonth = [i.split('-')[1] for i in allData.Date]
allDay = [i.split('-')[2] for i in allData.Date]
#print allDay

#calculating daily mean (open+close+high+low)/4 
allPrice_OC = map(operator.add, allData.Open, allData.Close)
allPrice_HL = map(operator.add, allData.High, allData.Low)
allPrice_TOT = map(operator.add, allPrice_OC, allPrice_HL)
allPrice_avg = np.array(allPrice_TOT)/4

#all volume
allVolume = allData.Volume


allData_reformat = pd.DataFrame(
	{'col1_Year': allYear,
	'col2_Month': allMonth,
	'col3_Day': allDay,
	#'col4_Volume': allVolume,
	'col5_avgPrice': allData.High
	})
allData_reformat.to_csv('data/'+str(stocks)+'_re.csv', index=False)

dataFrame = pd.read_csv('data/'+str(stocks)+'_re.csv')

#getting total number of samples
sampleNum = dataFrame.shape[0]

#split samples into 
testDate = sampleNum - testNum

stockData = dataFrame.values
tradingDate = stockData[:,0:3]
tradingPrice = stockData[:,3] 
#scaler2 = MinMaxScaler(feature_range=(0, 1))
#tradingDate_rescale = scaler2.fit_transform(tradingDate)
#print tradingDate_rescale[0:testDate,:]

price_train = tradingPrice[:testDate]
price_test = tradingPrice[testDate:sampleNum]

x_axis = np.linspace(1, sampleNum, sampleNum,dtype=float32)
print x_axis

#scaler2 = MinMaxScaler(feature_range=(0, 1))
x_axis_rescale = normalize(x_axis)
days_train = x_axis_rescale [:testDate]
days_test = x_axis_rescale [testDate:sampleNum]

print x_axis_rescale
print days_train
print days_test

plt.figure(figsize=(15,6))
plt.plot(x_axis[:sampleNum], tradingPrice[:sampleNum], '.')
#exit()
lrp = lm.RidgeCV(alphas=(1,0.01))

#we are iterating through 2 numbers of degrees (2 and 5), s is just a symbol for plotting
for deg, s in zip([15], ['-']):
	lrp.fit(np.vander(days_train, deg + 1), price_train)  #ALERT! FITTING HERE
	print lrp.alpha_
	print lrp.coef_.tolist()
	#y_lrp = lrp.predict(np.vander(days_test, deg+1)) #ALERT! TESTING HERE
	y_lrp = lrp.predict(np.vander(x_axis_rescale, deg+1)) #ALERT! TESTING HERE
	#plt.plot(x_axis[testDate:sampleNum], y_lrp[testDate:sampleNum], s, label='deg ' + str(deg))
	plt.plot(x_axis[:sampleNum], y_lrp[:sampleNum], s, label='deg ' + str(deg))
	plt.legend(loc=2)
	#plt.xlim(testDate, sampleNum)
	#plt.ylim(np.amin(y_lrp), np.amax(y_lrp))

plt.show()
