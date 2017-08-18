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

stocks = "TSLA"

#Get data for stocks, from google, starting at 2012-01-15 ending at 2016-09-01

testdata = dreader.DataReader(stocks,'google','2008-01-01','2017-01-01')
testdata.to_csv('data/TSLA.csv')

exit()
testdata = testdata.swapaxes(0,2)

