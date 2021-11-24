# -*- coding: utf-8 -*-

# Created on Fri Apr  9 21:26:09 2021

# @author: TonyTian
from statsmodels.tsa.stattools import coint
import pandas_datareader.data as web
from statsmodels.tsa.stattools import adfuller
import numpy as np
import pandas as pd
import datetime


class Test():


  ###pearson's correlation
  ###split is a list containing start and end for sr.loc[] function, not sr.iloc[]
  def Correlation(sr1,sr2,split=None):
    if split==None:
      return np.corrcoef(sr1,sr2)[0][1]
    else:
      start=split[0]
      end=split[1]
      return np.corrcoef(sr1[start:end],sr2[start:end])[0][1]




  ###Check if a time series is stationary or not
  def StationarityTest(sr,cutoff=0.01,start=None,end=None):
    if start==None and end==None:
      pvalue=adfuller(sr)[1]

    elif start==None:
      pvalue=adfuller(sr.loc[:end])[1] 
    
    elif end==None:
      pvalue=adfuller(sr.loc[start:])[1] 

    else:
      pvalue=adfuller(sr.loc[start:end])[1] 

    return int(pvalue<cutoff)

  
  ###Check pairs of stocks in a dictionary(StockData={'stockname':stockdata}) is cointegrated or not
  ###split is a list of two datetime data, denonting the first and last date of the data in the CointTest
  def CointTest_StockData(StockData,cutoff=0.01,split=None):
    Pair_List=[]
    Pvalue=[]
    names=list(StockData.keys())
    if split!=None:
      start=split[0]
      end=split[1]
  
      for i in range(len(names)):
        Yname=names[i]
        Y=StockData[Yname].loc[start:end]
        for j in range(i+1,len(names)):
          Xname=names[j]
          X=StockData[Xname].loc[start:end]
          pval=coint(Y,X)[1]
          if pval<cutoff:
            Pair_List.append([Yname,Xname])
            Pvalue.append(pval)
  
    if split ==None:
      for i in range(len(names)):
        Yname=names[i]
        Y=StockData[Yname]
        for j in range(i+1,len(names)):
          Xname=names[j]
          X=StockData[Xname]
          pval=coint(Y,X)[1]
          if pval<cutoff:
            Pair_List.append([Yname,Xname])
            Pvalue.append(pval)

    return [Pair_List,Pvalue]
  
  ###Check one pair of stocks  
  def CointTest(Y,X,cutoff=0.01):
    pval=coint(Y,X)[1]
    return int( pval<cutoff)


  
  
  ###Check if a series data's starttime and endtime data
  ###are on the different side of the threshold or not
  ###on==True means if endtime_data==threshold, it counts as different side
  def CrossThreshold(thre,series,starttime,endtime,on=False):
    a=series.loc[endtime]
    b=series.loc[starttime]
    if (a-thre)*(b-thre)<0:
      return 1
    if on==True:
      return int( a==thre)
    else:
      return 0


  ###on==True means if exsit some x1==threshold but (x0-thre)(x2-thre)>0, it counts as crossed
  ###if on==True, and the last element in the series==threshold, it counts as crossed
  def CrossingTime(thre,series,starttime,endtime,on=False):
    sr=series.loc[starttime:endtime]
    length=len(sr.index)
    time=0
    for i in range(length-1):
      x0=sr.iloc[i]
      x1=sr.iloc[i+1]
      if x1!=thre:
        time+= int(((x0-thre)*(x1-thre))<0)
  
      elif on==True:
        
        time+=1
        
      elif i!=(length-1):
        x2=sr.iloc[i+2]
        time+=int((x0-thre)*(x2-thre)<0)
    return time

        



  def hurst( ts):
    """
    Returns the Hurst Exponent of the time series vector ts.
    Series vector ts should be a price series.
    Source: https://www.quantstart.com/articles/Basics-of-Statistical-Mean-Reversion-Testing"""
    ts=ts.to_numpy()
    lags = range(2, 100)
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)

        
    return poly[0] * 2.0


class Gen():

  #Generate return data
  #D stands for discrete return, 'C' stands for continuous one
  def ReturnGen(sr,IncludeNan=False,type='D'):
    try:
      if type=='D':
        if IncludeNan==True:
          return (sr-sr.shift())/sr.shift()
        return ((sr-sr.shift())/sr.shift()).iloc[1:]
  
      elif type=='C':
        r=np.log(sr) - np.log(sr.shift(1))
        if IncludeNan==True:
          return r
        return r.iloc[1:]
  
    except:
        print('Wrong type, should be of type pandas.series')

  def FutureReturnGen(sr,IncludeNan=False,type='D'):
    try:
      sr1=sr.shift(-1)
      if type=='D':
        if IncludeNan==True:
          return (sr1-sr)/sr
        return ((sr1-sr)/sr).dropna()
  
      elif type=='C':
        r=np.log(sr1) - np.log(sr)
        if IncludeNan==True:
          return r
        return r.dropna()
  
    except:
        print('Wrong type, should be of type pandas.series')
  
  
  #standardizer using sample variance
  #ddof stands for degree of freedom in the calculation of std
  def Standardizer(sr,ddof=1):
    sr1=sr.copy()
    (sr1 - sr.mean()) / sr.std(ddof=ddof)
    return sr1
  
  
  def ColumnStandardizer(df,ddof=1):
    df1=df.copy()
    for i in range(len(df.columns)):
      df1.iloc[:,i]=Standardizer(df1.iloc[:,i],ddof=ddof)
    
    return df1


  def GetYahooData(ticker_list,start_time=None,end_time=None):
    d={}
    if start_time==None and end_time==None:
      for ticker in ticker_list:
        try:
          a=web.get_data_yahoo(ticker)
          d[ticker]=a

        except:
          print(ticker,'failed')
          

    elif start_time==None:

      for ticker in ticker_list:
        try:
          a=web.get_data_yahoo(ticker,end=end_time)
          if a.index[-1]==end_time:
            
            d[ticker]=a
          else:
            print('last index of',ticker,'is',a.index[-1])
        except:
          print(ticker,'failed')
          

    elif end_time==None:

      for ticker in ticker_list:
        try:
          a=web.get_data_yahoo(ticker,start_time)
          if a.index[0]==start_time:
            
            d[ticker]=a
          else:
            print('first index of',ticker,'is',a.index[0])
        except:
          print(ticker,'failed')
          
    
    else:
      for ticker in ticker_list:
        try:
          a=web.get_data_yahoo(ticker,start=start_time,end=end_time)
          if ((a.index[0]==start_time) and (a.index[-1]==end_time)):
            
            d[ticker]=a
          else:
            print('first index of',tick,'is', a.index[0])
            print('last index of',tick,'is', a.index[-1])
        except:
          print(ticker,'failed')
          
    return d
    

  def Lag_Feature_Target(sr,lag):
    t=sr.iloc[lag:]
    F=[]
    for i in range(len(t)):
      f=sr.iloc[i:i+lag].tolist()
      F.append(f)
    return np.array(F).reshape(len(t),lag,1),t.to_numpy()
