# -*- coding: utf-8 -*-
#
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
class dp():

  ###Plot a list of Series object from start date to end date,
  ###Can add xvlines with customed color and labels
  def DfPlot(listofdf,listoflabel,start='',end='',xvline=False,listofxvlines=[],xvColor=False,xvColorDic={},xvColorIndex=[]):
    for i in range(len(listofdf)):
      df=listofdf[i]
      label=listoflabel[i]
      if start=='':
        start1=df.index[0]
      else:
        start1=start
      if end=='':
        end1=df.index[-1]
      else:
        end1=end
      plt.plot(np.array(df[start1:end1].index),df.loc[start1:end1],label=label)

    
    if xvline==True and xvColor==False:
      
      for i in listofxvlines:
        plt.axvline(x=i)
    elif xvline==True and xvColor==True:
      uniqueI=list(set(xvColorIndex))
      indicator=np.zeros(len(uniqueI))
      for i in range(len(listofxvlines)):
        name=xvColorIndex[i]
        loc=uniqueI.index(name)
        
        if indicator[loc]==0:
          plt.axvline(x=listofxvlines[i],color=xvColorDic[name],label=name)
          
        else:
          plt.axvline(x=listofxvlines[i],color=xvColorDic[name])
        indicator[loc]+=1
        plt.xticks( rotation='vertical')


        
    plt.legend()
    plt.show()
    
  ###Show Scatter Plot of a pd.DataFrame Object
  def DfSCPlot(df,size=10,start='',end=''):
    
    if start=='':
      start=df.index[0]
    if end=='':
      end=df.index[-1]
    s = [size for n in range(len(np.array(df[start:end].index)))]
    plt.scatter(np.array(df[start:end].index),df[df.columns[0]][start:end],s=s)
    plt.show()

  ###Plot the cummulative value of a pd.DataFrame Object
  def RFPlot(df,default=100):
    r=[]
    for i in range(len(df.values)):
      arr=df.values[:i]
      s=+np.sum(arr)
      r.append(s)
    plt.plot(df.index,np.array(r))
    plt.show()