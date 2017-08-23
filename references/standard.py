#!/usr/bin/python

import numpy as np
import scipy.stats as st
import sklearn.linear_model as lm
import matplotlib.pyplot as plt
import pandas
from sklearn.preprocessing import Normalizer 
from sklearn.preprocessing import MinMaxScaler

dataFrame = pandas.read_csv('../data/INTC_re.csv')
#print dataFrame

stockData = dataFrame.values
tradingDate = stockData[:,0:3]
tradingPrice = stockData[:,3]

print tradingDate
print "\n\n normalized"
scaler1 = Normalizer().fit(tradingDate)
tradingDate_norm = scaler1.transform(tradingDate)
print tradingDate_norm

print "\n\n rescaled"
scaler2 = MinMaxScaler(feature_range=(0, 1))
tradingDate_rescale = scaler2.fit_transform(tradingDate)
print tradingDate_rescale

print "\n\n normalized and rescaled"
scaler3 = MinMaxScaler(feature_range=(0, 1))
rescaledX = scaler3.fit_transform(tradingDate_norm)
print rescaledX

