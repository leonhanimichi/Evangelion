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

from pylab import * #Used to calculate Mean and maybe more stuff didn't check, can probably replace/get rid of it

stocks = "INTC"

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

print allPrice_avg

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

exit()
allData = allData.swapaxes(0,2)

