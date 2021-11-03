import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit


#Function definition to read in scintillator files into a numpy array
def readFile(fD):
    all_data_arr = np.genfromtxt(fD, delimiter = ",", skip_header = 1)
    ##Add code to read data and get time
    return all_data_arr

##Arrays

peakPosA1 = []
peakPosA2 = []

peakPosB1 = []
peakPosB2 = []

peakPosC1 =[]
peakPosC2=[]

bad_data=0

## Function for finding roots of linear fit done later
def solve_for_y(poly_coeffs, y):
    pc = poly_coeffs.copy()
    pc[-1] -= y
    return np.roots(pc)

## For loop
for filename in os.listdir("/'C:\Users\aweso\Documents\Alice Prac\run_1'".format(run)):
    if(filename != "timeTaken.txt"):
        pulse = readFile("/Users/antoniagrindrod/ALICE2020Public/Optimisation/{0}/{1}".format(run, filename))
        
        ## Splitting the Pulses
        
        pulse1 = np.array(pulse[0,])
        pulse2 = np.array(pulse[1,])
        
        ##Time array as time-step of 4 ns
        t=np.arange(0,len(pulse1)*4,4)
        
        ##Isolating signal Peak Areas
        
        reduced_pulse1=pulse1[350:450]
        reduced_pulse2=pulse2[350:450]
        
        ## Reducing Time arrray to help with indexing
        
        reduced_t=t[350:450]
        
        ## Turning Points of Signals
        
        peak_1 = np.amin(reduced_pulse_1)
        index_1 = np.where(reduced_pulse_1 == peak_1)
        
        peak_2 = np.amin(reduced_pulse_2)
        index_2 = np.where(reduced_pulse_2 == peak_2)
        
        ## Finding small fluctuations away from the zero line
        signal_fluctuations_1 = pulse1[0:350]
        signal_fluctuations_2 = pulse2[0:350]
        
        for i in range (len(signal_fluctuations_1)):
            if (signal_fluctuations_1[i] != 0) & (signal_fluctuations_1[i] > 0):
                signal_fluctuations_1 = -signal_fluctuations_1[i]
                break
            
            elif (signal_fluctuations_1[i] != 0) & (signal_fluctuations_1[i] < 0):
                signal_fluctuations_1 = signal_fluctuations_1[i]
                break
        
        if np.isscalar(signal_fluctuations_1)==False:
            signal_fluctuations_1=0

        for i in range (len(signal_fluctuations_2)):
            if (signal_fluctuations_2[i] != 0) & (signal_fluctuations_2[i] > 0):
                signal_fluctuations_2 = -signal_fluctuations_2[i]
                break
            
            elif (signal_fluctuations_2[i] != 0) & (signal_fluctuations_2[i] < 0):
                signal_fluctuations_2 = signal_fluctuations_2[i]
                break
        
        if np.isscalar(signal_fluctuations_2)==False:
            signal_fluctuations_2=0
                
        ## Checking to see if there are any "bad" data sets
        pulse_test_1 = pulse1
        pulse_test_2 = pulse2
        
        for i in range(len(pulse_test_1)):
            if (np.abs(pulse_test_1[i])==np.abs(signal_fluctuations_1)):
                pusle_test_1[i]=0
            elif(np.abs(pulse_test_1[i])==2*np.abs(signal_fluctuations_1):
                pulse_test_1[i]=0
        
        for i in range(len(pulse_test_2)):
            if (np.abs(pulse_test_2[i])==np.abs(signal_fluctuations_2)):
                pusle_test_2[i]=0
            elif(np.abs(pulse_test_2[i])==2*np.abs(signal_fluctuations_2):
                pulse_tes_2[i]=0
                
        if (np.all(pulse_test_1==0)==True) or (np.all(pulse_test_2==0)==True):
            peakPosA1.append('NaN')
            peakPosA2.append('NaN')
            
            peakPosB1.append('NaN')
            peakPosB2.append('NaN')
            
            peakPosC1.append('NaN')
            peakPosC2.append('NaN')
            
            bad_data=1
        
        else:
            
            ##Method 1: measuring time difference between the minima
            if (len(reduced_t[index_1]) > 1):
                time_1=sum(reduced_t[index_1])/len(reduced_t[index_1])
            else:
                time_1=reduced_t[index_1][0]
            peakPosA1.append(time_1)
        
            if (len(reduced_t[index_2]) >1):
                time_2=sum(reduced_t[index_2])/len(reduced_t[index_2])
            else:
                time_2=reduced_t[index_2][0]
            peakPosA2.append(time_2)
    
            ## Method 2: Threshold value done in 2020 (this method did not work for us at all we couldn't even analyse the output as it was all zero but
                                                        #keeping it in here for future years)
            diff_1 = peak_1/2
            count = 0

            for i in range(2,len(reduced_t)):
                if np.abs(reduced_pulse1[i-2] - reduced_pulse1[i]) > diff_1:
                    count = i-2
                    pos = reduced_t[count]
                    peakPosB1.append(pos)  
                    break
                    
            diff_2 = peak_2/2
            count = 0

            for i in range(2,len(reduced_t)):
                if np.abs(reduced_pulse2[i-2] - reduced_pulse2[i]) > diff_2:
                    count = i-2
                    pos = reduced_t[count]
                    peakPosB2.append(pos)  
                    break
            
            ## Method 3: Dunno what to call it? Linear fit for non-discrete starting value of the pulse
            
            ## Preliminary set-up of arrays
            fit_data1=[]
            fit_t1=[]
            
            for i in range (len(reduced_pulse1)):
                if ((reduced_pulse1[i] < signal_fluctuations_1) & (reduced_pulse1[i] >= peak_1)):
                    fit_data1.append(reduced_pulse1[i-1])
                    fit_t1.append(reduced_t[i-1])
                    
                    if (reduced_pulse1[i] == peak_1):
                        fit_data1.append(reduced_pulse1[i])
                        fit_t1.append(reduced_t[i])
                        break
            
            fit_data2=[]
            fit_t2=[]
            for i in range (len(reduced_pulse2)):
                if ((reduced_pulse2[i] < signal_fluctuations_2) & (reduced_pulse2[i] >= peak_2)):
                    fit_data2.append(reduced_pulse2[i-1])
                    fit_t2.append(reduced_t[i-1])
                    
                    if (reduced_pulse2[i] == peak_2):
                        fit_data2.append(reduced_pulse2[i])
                        fit_t2.append(reduced_t[i])
                        break
            
            ## Fit of the linear function
            fit_1 = np.polyfit(fit_t1,fit_data1,1)
            fit_2 = np.polyfit(fit_t2,fit_data2,1)
            
            if signal_fluctuations_1 >= signal_fluctuations_2:
                eval = signal_fluctuations_2
            else:
                eval = signal_fluctuations_1
            
            peakPosC1.append(solve_for_y(fit_1,2*eval)[0].astype(float))
            peakPosC2.append(solve_for_y(fit_2,2*eval)[0].astype(float))
            


## Converting to numpy arrays for ease of use
peakPosA1=np.array(peakPosA1)
peakPosA2=np.array(peakPosA2)

peakPosB1=np.array(peakPosB1)
peakPosB2=np.array(peakPosB2)

peakPosC1=np.array(peakPosC1)
pealPosC2=np.array(peakPosC2)

##Removing any points from "bad" data sets
if (bad_data == 1):
    peakPosA1 = np.delete(peakPosA1,np.where(peakPosA1 == 'NaN')).astype(float)
    peakPosA2 = np.delete(peakPosA2,np.where(peakPosA2 == 'NaN')).astype(float)
    peakPosA1=peakPosA1[~np.isnan(peakPosA1)]
    peakPosA2=peakPosA2[~np.isnan(peakPosA2)]

    peakPosB1 = np.delete(peakPosB1,np.where(peakPosB1 == 'NaN')).astype(float)
    peakPosB2 = np.delete(peakPosB2,np.where(peakPosB2 == 'NaN')).astype(float)
    peakPosB1=peakPosB1[~np.isnan(peakPosB1)]
    peakPosB2=peakPosB2[~np.isnan(peakPosB2)]

    peakPosC1 = np.delete(peakPosC1,np.where(peakPosC1 == 'NaN')).astype(float)
    peakPosC2 = np.delete(peakPosC2,np.where(peakPosC2 == 'NaN')).astype(float)
    peakPosC1=peakPosC1[~np.isnan(peakPosC1)]
    peakPosC2=peakPosC2[~np.isnan(peakPosC2)]
    

##Time difference from method 1
tdArr1 = np.abs(peakPosA1 - peakPosA2)

##Time difference from method 2
tdArr2 = np.abs(peakPosB1 - peakPosB2)

##Time difference from method 3
tdArr3 = np.abs(peakPosC1 - peakPosC2)

#Saving to csv file format with channel 1 and 2 integrals as well as the two methods of calculating time difference

header = ['EventID', 'TD (Method 1)', 'TD (Method 2)','TD(Method 3)']
rows = []

for i in range(len(tdArr1)):
    rows.append([i,tdArr1[i],tdArr2[i],tdArr3[i]])# set the zero value to the timestamp from timestampArr[i]

with open('Event_Log_{0}.csv'.format(run), 'wt') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header) 
    csv_writer.writerows(rows)