#!/usr/bin/python

'''
Created on Aug 15, 2017

@author: Leon (Jobs), Junaid (Woz)
'''
import pandas as pd
import numpy as np
import random as rrand
import math as math
from pandas_datareader import data as dreader

from pylab import * #Used to calculate Mean and maybe more stuff didn't check, can probably replace/get rid of it

stocks = "AAPL"

#Get data for stocks, from google, starting at 2012-01-15 ending at 2016-09-01

allData_temp = dreader.DataReader(stocks,'google','2008-01-01','2009-01-03')
allData_temp.to_csv('data/'+str(stocks)+'.csv')

allData = pd.read_csv('data/'+str(stocks)+'.csv')
print allData.Date

exit()
allData = allData.swapaxes(0,2)

