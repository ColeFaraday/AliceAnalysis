import matplotlib.pyplot as plt
import numpy as np
import os
import scipy
from scipy.optimize import curve_fit
from scipy.stats import norm
from scipy.special import gamma

## Definining Useful Functions
def gaus(x,a,x0,sigma):
    return (a/(sigma*np.sqrt(2*np.pi))*exp(-((x-x0)**2)/(2*sigma**2)))

def gam(x,A,beta,alpha):
    return A/gamma(alpha)*beta**alpha*x**(alpha-1)*np.exp(-beta*x)


Time_differences = np.genfromtxt('Data generated TimeDifference.py',delimiter=',',skipheader=1)
Method_1=Time_differences[,1]
Method_2=Time_differences[,2] ##Honestly this was useless for us as mentioned in Time_Difference but just here for completeness
Method_3=Time_differences[,3]

## Comparison of methods

plt.figure()
##Method 1
if np.all(Method_1==0)==True: ##Done purely because method 2 was giving very unusable values
    pass
else:
    noBins1 = ##Define a number of bins here i tried to find a way to automate it but honestly it's so dependent on the data set
    plt.hist(Method_1,bins = noBins1,color="deepskyblue") ##Use this to see whether the number of bins you've chosen is sufficient. You've probably learnt this in the Poisson 
                                                                ##lab but in case not you essentially just want to see some shape that relates to a distribution (it will most probably  
                                                                ## be one of the functions described above) and you want a decent number of observations in each bin 
    counts, edges = np.histogram(Method_1,bins = noBins1)
    centres = (edges[1:] + edges[:-1]) / 2
    mu, sigma = scipy.stats.norm.fit(Method_1) ##Rough estimate of mean and standard deviation
    
    ##Here you'll need to just uncomment the distribution you want. It should be noted that the gamma might give a warning - dont worry about this too much it's essetially just
    ##that the exponential becomes functionally zero it shoudlnt chnage the values of the fit
    
    ##popt1,pcov1=curve_fit(gaus,centres,counts,p0=[60,mu,sigma]) 
    ##popt1,pcov1 = curve_fit(gam,centres,counts,p0=[60,0.4,0.4*mu]) Tip for choosing p0 for this, choose a beta value and make the alpha value mu*beta.
    
    x = np.linspace(0,30,1000)
    
    ##Similarly just uncomment which you would like to plot
    ## plt.plot(x,gam(x,*popt1),'r--',label='Fit of Gaussian Distribution',markersize=1)
    ## plt.plot(x,gaus(x,*popt1),'r--',label='Fit of Gamma Distribution',markersize=1)
    plt.title("Method 1: Minimums")
    plt.ylabel("Number of counts")
    plt.xlabel("Time(ns)")
    plt.xlim(0,30)

plt.figure()
##Method 2
if np.all(Method_2==0)==True:
    pass
else:
    noBins2 = ## Arbitrary Number
    plt.hist(Method_2,bins = noBins2,color="deepskyblue")
    counts, edges = np.histogram(Method_2,bins = noBins2)
    centres = (edges[1:] + edges[:-1]) / 2
    mu, sigma = scipy.stats.norm.fit(Method_2)
    
    ##Here you'll need to just uncomment the distribution you want. It should be noted that the gamma might give a warning - dont worry about this too much it's essetially just
    ##that the exponential becomes functionally zero it shoudlnt chnage the values of the fit
    
    ##popt2,pcov2=curve_fit(gaus,centres,counts,p0=[60,mu,sigma]) 
    ##popt2,pcov2 = curve_fit(gam,centres,counts,p0=[60,0.4,0.4*mu]) Tip for choosing p0 for this, choose a beta value and make the alpha value mu*beta.
    
    x = np.linspace(0,30,1000)
    
    ##Similarly just uncomment which you would like to plot
    ## plt.plot(x,gam(x,*popt2),'r--',label='Fit of Gaussian Distribution',markersize=1)
    ## plt.plot(x,gaus(x,*popt2),'r--',label='Fit of Gamma Distribution',markersize=1)
    plt.title("Method 2: Threshold")
    plt.ylabel("Number of counts")
    plt.xlabel("Time(ns)")
    plt.xlim(0,30)

plt.figure()

##Method 3
if np.all(Method_3==0)==True:
    pass
else:
    noBins3 = 1000 ##An upside for this method is that it was very analysis friendly working with 1000 bins pretty much every time (obviously we need a large number of data sets)
    plt.hist(Method_3,bins = noBins3,color="deepskyblue") ##Still useful to check
    counts, edges = np.histogram(Method_2,bins = noBins2)
    centres = (edges[1:] + edges[:-1]) / 2
    mu, sigma = scipy.stats.norm.fit(Method_3) ##Rough estimate of mean and standard deviation
    
    ##popt3,pcov3=curve_fit(gaus,centres,counts,p0=[60,mu,sigma]) 
    ##popt3,pcov3 = curve_fit(gam,centres,counts,p0=[60,0.4,0.4*mu]) Tip for choosing p0 for this, choose a beta value and make the alpha value mu*beta.
    
    x = np.linspace(0,30,1000)
    
    ##Similarly just uncomment which you would like to plot
    ## plt.plot(x,gam(x,*popt3),'r--',label='Fit of Gaussian Distribution',markersize=1)
    ## plt.plot(x,gaus(x,*popt3),'r--',label='Fit of Gamma Distribution',markersize=1)
    plt.title("Method 3: Start of the Signal")
    plt.ylabel("Number of counts")
    plt.xlabel("Time(ns)")
    plt.xlim(0,30)
    
##Value of Time resolution:

##If Gaussian Distribution used
##Time_Resolution_Method_1 = popt1[1]
## Uncertainty_Method_1 = np.sqrt(popt1[2]+pcov1[1,1]) 

##Time_Resolution_Method_2 = popt2[1]
## Uncertainty_Method_2 = np.sqrt(popt2[2]+pcov2[1,1])

##Time_Resolution_Method_3 = popt3[1]
## Uncertainty_Method_3 = np.sqrt(popt3[2]+pcov3[1,1])

##If Gamma Distribution used (The variance can be checked on wikipedia or any other source for statistical distributions and then there's a simple uncertainty propagation)
##Time_Resolution_Method_1 = popt1[2]/popt1[1]
## Uncertainty_Method_1 = np.sqrt(popt1[2]/popt1[1]**2 + (popt1[2]/popt1[1]*np.sqrt((pcov1[1,1]/popt1[1])**2+(pcov1[2,2]/popt1[2])**2))**2)

##Time_Resolution_Method_2 = popt2[2]/popt2[1]
## Uncertainty_Method_2 = np.sqrt(popt2[2]/popt2[1]**2 + (popt2[2]/popt2[1]*np.sqrt((pcov2[1,1]/popt2[1])**2+(pcov2[2,2]/popt2[2])**2))**2)

##Time_Resolution_Method_3 = popt3[2]/popt3[1]
## Uncertainty_Method_3 = np.sqrt(popt3[2]/popt3[1]**2 + (popt3[2]/popt3[1]*np.sqrt((pcov3[1,1]/popt3[1])**2+(pcov3[2,2]/popt3[2])**2))**2)