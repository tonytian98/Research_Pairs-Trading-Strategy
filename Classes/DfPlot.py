# -*- coding: utf-8 -*-
#
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import figure

class dp():
  ##Plot a list of series data, can add xvlines to the plot
  ## ColorDic is a dictionary mapping xvline labels to colors, xvLabel is a list mapping each xvline to its label
  def SRPlot(listofsr,listoflabel,listofcolor,start='',end='',outside_label=False,label_fontsize=8,xvline=False,listofxvlines=[],xvColor=False,xvColorDic={},xvColorIndex=[]):
    figure(figsize=(18, 6), dpi=300)
    

    
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


    for i in range(len(listofsr)):
      sr=listofsr[i]
      label=listoflabel[i]
      if start=='':
        start1=sr.index[0]
      else:
        start1=start
      if end=='':
        end1=sr.index[-1]
      else:
        end1=end
      plt.plot(np.array(sr[start1:end1].index),sr.loc[start1:end1],label=label,color=listofcolor[i])
      plt.xticks(rotation='vertical')
    
    

    if outside_label==True:
      fontP = FontProperties()
      fontP.set_size('x-small')
      plt.legend( bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=label_fontsize)
    else:
      plt.legend()
    plt.show()
    
  
  
  def SRSCPlot(df,size=10,start='',end=''):
    
    if start=='':
      start=df.index[0]
    if end=='':
      end=df.index[-1]
    s = [size for n in range(len(np.array(df[start:end].index)))]
    plt.scatter(np.array(df[start:end].index),df[df.columns[0]][start:end],s=s)
    plt.show()
  
  def RFPlot(df,default=100):
    r=[]
    for i in range(len(df.values)):
      arr=df.values[:i]
      s=+np.sum(arr)
      r.append(s)
    plt.plot(df.index,np.array(r))
    plt.show()



  
  
  def Culmulative_Histo(sr,numbins=25,ShowGrid=False):

    # specifying figure size
    fig = plt.figure(figsize=(10, 4))  
    # adding sub plots
    ax1 = fig.add_subplot(1, 2, 1) 
    # adding sub plots
    ax2 = fig.add_subplot(1, 2, 2)   
    # getting histogram using hist function
    ax1.hist(sr, bins=numbins, histtype='step',
              color="green")
        
    # setting up the title
    ax1.set_title('Histogram')
        
    # cumulative graph
    n, bins, patches = ax2.hist(sr, numbins,density=True, histtype='step',
                           cumulative=True)
        
    # setting up the title
    ax2.set_title('Cumulative histogram')
    ax1.set_xlim([sr.min(), sr.max()])

    ax2.set_xlim([sr.min(), sr.max()])


    


    if ShowGrid==True:
      ax1.grid(True)
      ax2.grid(True)
    # display hte figure(histogram)
    plt.show()