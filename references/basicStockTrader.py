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


#Class for doing trading on historical price data as if you only had data for that day and previous days.
class Trader:
    
    def __init__(self, init, dailyaction):
        '''
        Just pass in your own init and dailyaction functions.
        '''
        self.init = init
        self.dailyaction = dailyaction
        self.portfolio = {'money': 0}
        self.transactions = []
        
    #No idea what this func is for
    def actionNum(self,act,stknum):
        '''
        No Idea what this is for...
        '''
        return act+(stknum*10)
    
    
    def run(self, DATA, startmoney=100000, fee=.02, closePriceName='Close'):
        '''
        Runs your trading algorithm. First calls your init function, then runs your code. \
        Starting money is 100k default. Fee for trading is set to 2 cents per share.
        closePriceName is set to "Close", which works when importing data from google, but for yahoo might want to use "Adj Close" for example. some other sites might make it "close" instead.
        '''
        self.DATA = DATA
        self.fee = fee
        self.closePriceName = closePriceName
        self.startmoney = startmoney

        for stocks in DATA.keys():
            self.portfolio[stocks] = 0
        
        for x in np.array(DATA[DATA.keys()[0]][self.closePriceName]):
            self.transactions.append([])
        self.day = 0
        self.portfolio['money'] = startmoney
        self.init(self)
        for x in range(0,len(np.array(DATA[DATA.keys()[0]][self.closePriceName]))):
            self.day = x
            self.dailyaction(self)
        x = self.lastday() #debug: make sure x isn't out of bounds of the data if you want to print stuff after it runs
    
    def buystocks(self,stockname,amount):
        '''
        Buys stocks for the stock name, at most the number given by amount. If too expensive, buys as many as you can.
        Note fee is added so might be able to buy less than you thought.
        '''
        price = np.array(self.DATA[stockname][self.closePriceName])[self.day] + self.fee
        amt = int(amount)
        moneyb4 = self.portfolio['money']
        if price*amount > self.portfolio['money']:
            amt = int(moneyb4/price)
        self.portfolio['money'] -= amt * price
        assert self.portfolio['money'] >= 0
        self.portfolio[stockname] += amt
        self.transactions[self.day].append([stockname,amt,price,self.portfolio[stockname],self.portfolio['money']])
        return amt, price, self.portfolio[stockname],self.portfolio['money']
    
    def buystockspercentage(self,stockname,perc):
        '''
        perc should be fraction of how much of your portfolio you want to spend, so perc must be between 0-1
        Buy stocks for the stockname. Buys as many stocks as you can afford based on perc*cash you have.
        So if perc is .5, will buy as many stocks as you can afford based on half the cash you have.
        '''
        if perc < 0:
            "ERROR: Trying to buy stock by percentage but perc is set to less than 0!"
            perc = 0
        if perc> 1:
            "ERROR: Trying to buy stock by percentage but perc is set to >1. Will buy as if perc = 1"
            perc = 1
        
        price = np.array(self.DATA[stockname][self.closePriceName])[self.day] + self.fee
        moneyb4 = self.portfolio['money']
        amt = int((perc*moneyb4)/price)
        self.portfolio['money'] -= amt * price
        assert self.portfolio['money'] >= 0
        self.portfolio[stockname] += amt
        self.transactions[self.day].append([stockname,amt,price,self.portfolio[stockname],self.portfolio['money']])
        return amt, price, self.portfolio[stockname],self.portfolio['money']
        
    def sellstocks(self,stockname, amount):
        '''
        Sells stocks for stockname by amount.
        If amount is greater than the number of stocks you have, sells all the stocks.
        For short selling use sellshort function.
        '''
        price = np.array(self.DATA[stockname][self.closePriceName])[self.day] - self.fee
        amt = int(amount)
        moneyb4 = self.portfolio['money']
        if amount > self.portfolio[stockname]:
            amt = self.portfolio[stockname]
        self.portfolio['money'] += amt * price
        assert self.portfolio['money'] >= 0
        self.portfolio[stockname] -= amt
        #assert self.portfolio[stockname] >= 0 #TODO: comment out for support for short selling
        self.transactions[self.day].append([stockname,amt,price,self.portfolio[stockname],self.portfolio['money']])
        return amt, price, self.portfolio[stockname],self.portfolio['money']
    
    def sellshort(self,stockname,amount):
        '''
        Short sells stocks. Sells stocks you don't have now, but then your portfolio has "negative" stocks.
        Note, not totally realistic because in real life you have a time limit on when you can pay-back the stocks you borrowed.
        '''
        price = np.array(self.DATA[stockname][self.closePriceName])[self.day] - self.fee
        amt = int(amount)
        moneyb4 = self.portfolio['money']
        if price*amount > self.portfolio['money']:
            amt = int(moneyb4/price)
        if self.portfolio[stockname] < 0:
            amt = 0
        self.portfolio['money'] += amt * price
        assert self.portfolio['money'] >= 0
        self.portfolio[stockname] -= amt
        #assert self.portfolio[stockname] >= 0 #TODO: comment out for support for short selling
        self.transactions[self.day].append([stockname,amt,price,self.portfolio[stockname],self.portfolio['money']])
        return amt, price, self.portfolio[stockname],self.portfolio['money']
    
    #note fee is subtracted from price
    def sellstockspercentage(self,stockname, perc):
        '''
        Sells percentage of stocks you have.
        '''
        price = np.array(self.DATA[stockname][self.closePriceName])[self.day] - self.fee
        moneyb4 = self.portfolio['money']
        amt = int(self.portfolio[stockname] * perc)
        self.portfolio['money'] += amt * price
        assert self.portfolio['money'] >= 0
        self.portfolio[stockname] -= amt
        assert self.portfolio[stockname] >= 0 #TODO: comment out for support for short selling
        self.transactions[self.day].append([stockname,amt,price,self.portfolio[stockname],self.portfolio['money']])
        return amt, price, self.portfolio[stockname],self.portfolio['money']
    
    def todaysprice(self,stockname):
        '''
        Returns the closing price of the day for given stockname
        '''
        return np.array(self.DATA[stockname][self.closePriceName])[self.day]
    
    #Days includes today, so days=1 would be just todays info. 
    def pricehistory(self,stockname,days,key):
        '''
        Returns price history of stockname for the days "days", in the category "key".
        Including today.
        So stockname=AAPL, days=2, key="Close" would return closing price of AAPL for today, and yesterday.  
        '''
        retlist = []
        for x in range(self.day-days+1,self.day+1):
            retlist.append(np.array(self.DATA[stockname][key])[x])
        assert len(retlist) == days
        return retlist
    
    def lastday(self):
        '''
        Returns the last index for "DATA" array provided on initialization
        '''
        return len(self.transactions)-1
    
    def totalmoney(self):
        '''
        Returns: total portfolio value+cash, just portfolio value, stock indexes originally given.
        Mostly first two are important, last one is for debugging mostly.
        '''
        total = 0
        #print  total, "start"
        keys = self.DATA.keys()
        #print keys
        for key in keys:
            #assert self.portfolio[key] >= 0
            #print self.portfolio[key]
            
            total += self.portfolio[key] * self.todaysprice(key)
            #print  total, key, self.portfolio[key]
       
        #print "Stocks checked, total money from stocks: ", keys, total
        totalstks = total
        total+= self.portfolio['money']
        assert self.portfolio['money'] >= 0
        #print  total
        return total, totalstks, keys
    
    #doesn't return the extra junk
    def totalmoneysimple(self):
        '''
        Just returns total portfolio value+cash
        '''
        total = 0
        #print  total, "start"
        keys = self.DATA.keys()
        #print keys
        for key in keys:
            #assert self.portfolio[key] >= 0
            #print self.portfolio[key]
            total += self.portfolio[key] * self.todaysprice(key)
            #print  total, key, self.portfolio[key]
       
        #print "Stocks checked, total money from stocks: ", keys, total
        totalstks = total
        total+= self.portfolio['money']
        assert self.portfolio['money'] >= 0
        #print  total
        return total

#I don't use this anymore I think but useful data structure. Can ignore for now.
class circularList:
    def __init__(self, size, initVal = 0):
        self.size = size
        self.clist = []
        for x in range (0,size):
            self.clist.append(initVal)
    def getElement(self,loc):
        return self.clist[loc]
    def getMostRecent(self):
        return self.clist[self.size-1]
    def shiftList(self):
        for x in range(1, self.size):
            self.clist[x-1] = self.clist[x] 
    def addElement(self,value):
        self.shiftList()
        self.clist[self.size-1] = value
    

stocks = ['QQQ','SPY','DIA',
        'EBAY','YHOO','EA','GOOG',
        'ATVI',
        ]

#Get data for stocks, from google, starting at 2012-01-15 ending at 2016-09-01
testdata = dreader.DataReader(stocks,'google','2012-01-15','2016-09-01')

#Use this to print general structure of the data
print "DATA: ", testdata

exit()
#print pnls.keys(), pnls['Close']['GOOG'][0]

#Have to swapaxes because my Trader class uses it like data[stockname]['Close']
testdata = testdata.swapaxes(0,2)


#The way it works is all you need is an init function and a dailyaction function, which I make here:

#This is my init function, given to and then called by "Trader" class later, just sets up some arrays I use for storage later that I use to track what my algo did.
def myinit(self):

    self.i = 0    
    self.beststk = "YHOO" #No idea why but my example algo bases its STD off of this stock
    
    self.holding = []
    self.pricelevellow = []
    self.pricelevelhigh = []
    self.oldprice = []
    for x in range(0,len(stocks)):
        self.holding.append(0)
        self.pricelevellow.append(0)
        self.pricelevelhigh.append(0)
        self.oldprice.append(0)
    self.movehist = []
    self.totaltrades = 0

#Helper function that just calculates STD
def getSTD(prices):
    avg = mean(prices)
    totalstd = 0
    for x in prices:
        diff = x-avg
        totalstd += (diff *diff)
    totalstd = totalstd/len(prices)
    return math.sqrt(totalstd)

#Helper function that tells me if there is a uptrend since yesturday
def uptrend(prices):
    diff =  prices[-1] - prices[0] 
    if diff> 0 :
        return True
    else:
        return False

#Helper function that gets the price change since yesturday in relation to STD.
def stdchange(prices):
    std = getSTD(prices)
    diff =  prices[-1] - prices[0] 
    return float(diff/std) 


#This is what my algo's dailyaction function. Its pretty much bullshit, I don't really know why it does what it does but you can use it as example of what you could do.
def myAction(self):
    self.i += 1
        
    #Constants that impact this trading algo
    minDaysToPredict = 10
    sellSTD = 2
    buySTD = .5
    actSTD = .5
    
    if self.i< (minDaysToPredict) :#going to get shitty training if you don't have a few days of data to look at first.
        #print "Skipping"
        #self.actionHistory.addElement(2)
        self.movehist.append("Wait to start")
        return                                                                                       

    
    moneytot, crap1,crap2= self.totalmoney()
    
    #Trader.pricehistory function gives you an array of prices for the given stockname, previous number of days to look at, and price type (open, close, etc).
    #So for example pricehistory('AAAPL',3,'Close') will give you the closing price aapl had for the previous 3 days. 
    #I only use 'Close" here.
    opens = self.pricehistory(self.beststk,minDaysToPredict,'Open')
    closes = self.pricehistory(self.beststk,minDaysToPredict,'Close')
    highs = self.pricehistory(self.beststk,minDaysToPredict,'High')
    lows = self.pricehistory(self.beststk,minDaysToPredict,'Low')
            
    #get STD of recent days for closing price for "beststk"
    stdd = getSTD(closes)
    
    stknum = -1
    for stk in stocks:
        stknum +=1
        self.beststk = stk
        todaysPrice = self.todaysprice(self.beststk)    
        
        #I stored how much of a stock I'm holding in self.holding. IDK because I can just use Trader.portfolio[stockName]
        if self.holding[stknum] != 0: #If you have some of the stock already, decide if you want to buy more, or sell it all
            if self.holding[stknum] > 0:
                #here I do some weird algo where I store the highest and lowest prices seen and trade based on that and STD
                if todaysPrice >= self.pricelevelhigh[stknum]:
                    self.pricelevellow[stknum] = todaysPrice- (stdd* sellSTD)
                    self.pricelevelhigh[stknum] = todaysPrice + (stdd * buySTD)
                    return
                elif todaysPrice < self.pricelevellow[stknum]:
                    self.sellstockspercentage(self.beststk,1)
                    self.movehist.append("Sell"+self.beststk)
                    print "Sold:", self.beststk, todaysPrice
                    self.holding[stknum] = 0
                    print "Buy Profit:",todaysPrice-self.oldprice[stknum]
                    self.totaltrades +=1
                    return
            else: 
                #Buy back stocks maybe
                #only make holding positive if you buy back all your stocks
                if todaysPrice <= self.pricelevelhigh[stknum]:
                    self.pricelevellow[stknum] = todaysPrice + (stdd* sellSTD)
                    self.pricelevelhigh[stknum] = todaysPrice - (stdd * buySTD)
                    return
                elif todaysPrice > self.pricelevellow[stknum]:
                    #Here I buy stocks using Trader.buystocks 
                    self.buystocks(self.beststk,self.portfolio[self.beststk]*-1)
                    self.movehist.append("Buyback"+self.beststk)
                    print "Buyback:", self.beststk, todaysPrice
                    
                    #Here I use Trader.portfolio[stockname] to see if I have any stocks for beststk
                    if self.portfolio[self.beststk] == 0:
                        self.holding[stknum] = 0
                        print "Fully bought back"
                        self.totaltrades +=1
                    print "Short Profit:",self.oldprice[stknum]-todaysPrice
                    return
        else: #If you don't own any of that stock, think about buying more
            if stdchange(closes) > actSTD: 
                amt = (moneytot / todaysPrice) * (1.0/len(stocks)) #amount of stocks to buy
                print moneytot, todaysPrice,(1.0/len(stocks))
                print "Bought:", self.beststk,todaysPrice, amt
                self.buystocks(self.beststk,amt)
                self.pricelevelhigh[stknum] = todaysPrice + (stdd * buySTD)
                self.pricelevellow[stknum] = todaysPrice - (stdd* sellSTD)
                self.movehist.append("Buy"+self.beststk)
                self.holding[stknum] = 1 #set holding to 1 if you bought some stocks.
               
            elif stdchange(closes) < -1*actSTD:
                #shortsell
                amt = (moneytot / todaysPrice) * (1.0/len(stocks))
                print "Short Sold:", self.beststk,todaysPrice, amt
                self.sellshort(self.beststk,amt)
                self.pricelevelhigh[stknum] = todaysPrice - (stdd * buySTD)
                self.pricelevellow[stknum] = todaysPrice + (stdd* sellSTD)
                self.movehist.append("Shortsell"+self.beststk)
                self.holding[stknum] = -1 #set holding to -1 if you shortsell a stock
            self.oldprice[stknum] = todaysPrice


#Initialize "Trader". All you have to do is give it a "init" function and "myAction" (short for my action) function. 
#The trader will then run your dailyaction (myAction) function every day using the data you provide in run. 
#So for example you can make myAction function just "buy GOOG", and it will buy GOOG every day
t = Trader(myinit,myAction)

#Runs the Trader algorithm on the test data provided as if each datapoint is 1 day.
t.run(testdata)

#t.totalmoney() will return: total value of portfolio+cash, value in stocks (not cash), and lastly the stock names supplied in data(for debugging mostly). 
print "Total Moneys Made:", t.totalmoney()

#Movehist is a giant array of every action the algorithm took. Note your dailyaction function should append these values to the array itself!
print "MoveList: ", t.movehist

#I manually stored how many trades I had in self.totaltrades
print "Number of Total Trades: ", t.totaltrades
