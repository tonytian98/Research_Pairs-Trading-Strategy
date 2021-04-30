# -*- coding: utf-8 -*-
"""OU Process.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A_WeAkkn8LF-lYjPKVxrGHQQR5sMAZ7b
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###generate n values from probability density function for random variable X (theoretically continuous, actually discrete given computational limitation)
###variable x is the the range of function X, assuming constant spacing in variable x, x=np.linspace() is recommended
###variable pdf is the range of probability density function, it should be of the same shape as x.  recommend to define a function as the pdf and pass pdf(x) to this variable
def GenFromDist(x, pdf, n):
    
    # get cumulative distribution from 0 to 1
    cumpdf = np.cumsum(pdf)
    cumpdf *= 1/cumpdf[-1]
    
    ###get the indeces of random values
    randv = np.random.uniform(size=n)
    idx1 = np.searchsorted(cumpdf, randv)
    
    # get previous index (except if idx1[i]==0, idx1[i] becomes 1 and idx0[i] is assigned by 0 to aviod negative index) 
    idx0 = np.where(idx1==0, 0, idx1-1)
    idx1[idx0==0] = 1

    # do linear interpolation in x
    frac = (randv - cumpdf[idx0]) / (cumpdf[idx1] - cumpdf[idx0])
    values = x[idx0]*(1-frac) + x[idx1]*frac

    return values

###pdf of Ornstein–Uhlenbeck process
def OU_pdf(x1,x0,theta,mu,sigma,t_incre=1):
  exp_inc=np.exp(-mu*t_incre)
  sigma1_sq=(sigma**2)*(1.0-np.exp(-2*mu*t_incre))/2.0/mu
  numerator=(x1-x0*exp_inc-theta*(1-exp_inc))**2
  inside_exp=-0.5*numerator/sigma1_sq
  p=1/np.sqrt(np.pi*2*sigma1_sq)*np.exp(inside_exp)
  return p

### Generate a Ornstein–Uhlenbeck process from time 0 to time t
### variable x is the union of range of random variable Xt, t=0,1,2,...,t. (theoretically continuous, actually discrete given computational limitation) assuming constant spacing in variable x, x=np.linspace() is recommended
### x0 is the initial value of the process
### other variables see paper for specifics
### intuitivelly theta is close to E(Xt), 
### mu is called the speed of reversion, it is invertly related to Var(Xt), and it can't be zero otherwise the process becomes a Brownian motion
### sigma is the variation(size) the noise, it is positively relative to Var(Xt)
def OU_Gen(x,x0,t,theta,mu,sigma,t_incre=1):
  y=[x0]
  for i in range(t):
    pdf=OU_pdf(x,y[i],theta=theta,mu=mu,sigma=sigma,t_incre=t_incre)
    y.append(GenFromDist(x,pdf,1)[0])

  return np.array(y)


### maximum (average) log-likelihood estimation of OU_process
### ar should be a 1D numpy array 
def OU_MLE(ar,t_incre=1):
  n=ar[1:].shape[0]
  X=ar[:-1].sum()
  Y=ar[1:].sum()
  XX=(ar[:-1]**2).sum()
  XY=(ar[:-1]*ar[1:]).sum()
  YY=(ar[1:]**2).sum()
  theta=(Y*XX-X*XY)/(n*(XX-XY)-(X**2-X*Y))
  mu=-1/t_incre*np.log((XY-theta*X-theta*Y+n*theta**2)/(XX-2*theta*X+n*theta**2))
  exp_inc=np.exp(-mu*t_incre)
  exp_inc2=np.exp(-2*mu*t_incre)
  sigma_sq=2*mu/n/(1-exp_inc2)*(YY-2*exp_inc*XY+exp_inc2*XX-2*theta*(1-exp_inc)*(Y-exp_inc*X)+n*(theta**2)*(1-exp_inc)**2)
  return theta,mu,sigma_sq


### return the average log likelihood
def Ave_Log_Likelihood(ar,theta,mu,sigma,t_incre=1):
  n=ar[1:].shape[0]
  sum=0
  for i in range(n):
    x1=ar[i+1]
    x0=ar[i]
    p=OU_pdf(x1,x0,theta,mu,sigma,t_incre=t_incre)
    sum+=np.log(p)
  
  return sum/n

###OLS Estimation of an OU process

def OU_OLSE(ar,t_incre=1):
  n=ar[1:].shape[0]
  X=ar[:-1].sum()
  Y=ar[1:].sum()
  XX=(ar[:-1]**2).sum()
  XY=(ar[:-1]*ar[1:]).sum()
  YY=(ar[1:]**2).sum()
  a=(n*XY-X*Y)/(n*XX-X**2)
  b=(Y-a*X)/n
  std_e=np.sqrt((n*YY-Y**2-a*(n*XY-X*Y))/n/(n-2))
  theta=b/(1-a)
  mu=-np.log(a)/t_incre
  sigma=std_e*np.sqrt((-2*np.log(a)/t_incre*(1-a**2)))
  return theta, mu, sigma**2


### Return the expectation of Xt in an OU process
### time is t-t0 
def OU_Mean(time,x0,theta, mu):
  return theta+(x0-theta)*np.exp(-mu*time)


### Return the variance of Xt in an OU process

def OU_Var(time,x0,mu,sigma):
  return sigma**2*(1-np.exp(-2*mu*time))/2/mu


### Return the half life of mean reversion of an OU process
from sklearn.linear_model import LinearRegression as OLS
def OU_Halflife(ar,mu=None):
  if mu==None:
    ar_ret = ar[1:] - ar[:-1] 
    model = OLS().fit( ar[:-1].reshape(-1,1),ar_ret)
    halflife = -np.log(2) / model.coef_[0]
    return halflife
  
  return np.log(2)/mu


def OU_HL(ar):
  mu=OU_MLE(ar)[1]
  print(mu)
  return np.log(2)/mu

x=np.linspace(-50,50,1000)
t=300
mean=0
xaxis=np.arange(0,t+1)

y=OU_Gen(x,mean,t,mean,1,10)
plt.plot(xaxis,y)

OU_MLE(y)

Ave_Log_Likelihood(y,mean,1,1)

test(y,mean,1,1)

OU_Halflife(y)

OU_HL(y)

for i in range(1,100,5):
  print(OU_Var(i,-1000000,1,36))

np.roll(np.array([1,2,3]),1)

np.log(2)

