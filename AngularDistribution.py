# Angular Distribution of Cosmic Events
# Duncan Torbet (ALICE)
# 10/2021

from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d
import matplotlib.gridspec as gridspec


## Appending Data
filepath = 'D:/Users/dunca/Desktop/2021/PHY3004W/TRD/coordinates.txt' ##Path to coordinate file that contains 2 angles
f = open(filepath,'r')

#### This code is dependent on the file format; it removes unnecessary characters
for line in f:
    data = line.strip(" ").split(" ")

f.close()

counter = 0
for i in data:
    data[counter] = i.strip("[]").split(",")
    counter += 1
####

## Location and Time

# Location of the TRD (Latitude, Longitude, Elevation above sea level)
trd = EarthLocation(lat=-33.9553325*u.degree,lon=18.4616939*u.degree,height=100*u.m)

# Local Sidereal Time (LST)
GMT_2 = 2*u.hour #The TRD is located in the timezone GMT+2:00.
t = Time('2021-11-01 17:00:00') - GMT_2 #Date and time of observation.


## Changing muon coordinates from Altitude-Azimuth to Right Ascension (RA) and Declination (DEC)

results = []
for i in data:
    results.append(SkyCoord(az=float(i[0])*u.degree,alt=float(i[1])*u.degree,frame='altaz',obstime=t,location=trd).transform_to('icrs'))
    # This takes in the Azimuth (i[0]) and Altitude (i[1]) relative to the TRD and then transforms them to RA and DEC


## Cleaning the results from ther conversion

resultsclean = []
for i in results:
    resultsclean.append(str(i)[39:].strip(">").strip("()").split(",")) #Removing SkyCoord Text and useless characters


## Plotting the (polar (2D)) angular distribution in our sky

ra = []
dec = []
for i in resultsclean:
    ra.append(float(i[0])) # Right Ascension values
    dec.append(float(i[1])) # Declination values

plt.polar(ra,dec,'ko',ms=2) # Producing a polar plot
plt.yticks([]) # Removing 'r' labels

plt.show()


## Converting from Right Ascension and Declination into cartesian coordinates

r = 1 # Setting the distance to be constant so that we can see a distribution within an even sphere

def x(r,RA,DEC):
    return r*np.cos(RA)*np.cos(DEC) # Cartesian x in terms of RA and DEC

def y(r,RA,DEC):
    return r*np.sin(RA)*np.cos(DEC)# Cartesian y in terms of RA and DEC

def z(r,RA,DEC):
    return r*np.sin(DEC) # Cartesian z in terms of RA and DEC


xc,yc,zc = [],[],[]
for i in resultsclean: # Arrays of each cartesian coordinate
    xc.append(x(r,float(i[0]),float(i[1])))
    yc.append(y(r,float(i[0]),float(i[1])))
    zc.append(z(r,float(i[0]),float(i[1])))


fig = plt.figure() # Plotting the figure
ax = plt.axes(projection='3d') # 3-Dimensional plot
ax.scatter3D(xc, yc, zc, c=zc, cmap='RdGy')
ax.scatter3D(0, 0, 0, 'ko', s=25) #Centre dot


plt.axis('on')
ax.set_xticks([0]) # Removing tick values because they are arbitrary
ax.set_yticks([0]) #
ax.set_zticks([0]) #

plt.show()







#
