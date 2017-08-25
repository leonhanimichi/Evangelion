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

from pylab import * #Used to calculate Mean and maybe more stuff didn't check, can probably replace/get rid of it

stocks = "AAPL"

#getting the stock info [Date, Open, High, Low, Close, Volume]
allData_temp = dreader.DataReader(stocks,'google','1970-01-01','2017-08-01')
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
	'col5_avgPrice': allPrice_avg
	})
allData_reformat.to_csv('data/'+str(stocks)+'_re.csv', index=False)

dataFrame = pd.read_csv('data/'+str(stocks)+'_re.csv')

stockData = dataFrame.values
tradingDate = stockData[:,0:3]
tradingPrice = stockData[:,3] 


scaler2 = MinMaxScaler(feature_range=(0, 1))
tradingDate_rescale = scaler2.fit_transform(tradingDate)
#print tradingDate_rescale[0:3500,:]

date_train = tradingDate_rescale[0:3500,:]
price_train = tradingPrice[:3500]

date_test = tradingDate_rescale[3500:4000,:]
price_test = tradingPrice[3500:4000]

print date_train
print date_test

x_axis = np.linspace(0., 4000, 4000)
plt.figure(figsize=(15,6))
plt.plot(x_axis[:4000], tradingPrice[:4000], '.')

lrp = lm.RidgeCV()

for deg, s in zip([3], ['-']):
	lrp.fit(date_train, price_train)  #ALERT! FITTING HERE
	print lrp.coef_.tolist()
	y_lrp = lrp.predict(date_test) #ALERT! TESTING HERE
	plt.plot(x_axis[3500:4000], y_lrp[0:500], s, label='degree ' + str(deg))
	plt.legend(loc=2)
	plt.xlim(3500, 4000)
	#plt.ylim(np.amin(y_lrp), np.amax(y_lrp))

plt.show()


exit()
allData = allData.swapaxes(0,2)

