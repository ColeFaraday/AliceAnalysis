#!/usr/bin/env python3
# Modifed version of https://github.com/CalleyRamcharan/ALICE2020Public/blob/main/roi.py

# Finds the regions of interest (i.e. where we expect to see tracklets) and saves them as a csv file

import numpy as np
import matplotlib.pyplot as plt
import itertools
import argparse

# CONSTANTS
BACKGROUND = 9.6 # TODO: fill in the real value

finalROIArr = None

class regions_of_interest:

    def __init__ ( self, adcdata ):
        ''' Takes in adcdata array which is a three dimensional array of the adcdata for a specific event'''

        self.data = adcdata
        self.tbsum = np.sum(self.data, 2) # sum over time dimension (total number of hits per pad)k

        # find points of interest - 2D array of hits = fired pads
        self.poi = np.argwhere(self.tbsum > 350) # TODO: This value seems arbitrary?

        # create list for regions of interest
        self.roi = []

        # find continuous regions of interest
        for r in sorted(set(self.poi[:,0])): # loop through the rows containing points of interest

            # pad columns with hits
            pads = [x[1] for x in self.poi if x[0]==r]

            start = False
            current = False
            for p in pads+[999]: #unsure why there is a +[999] here (legacy)
                if not start:
                    start=p
                    current=p-1

                # If the next pad is the one after the current pad, continue creating the region, otherwise the region is complete.
                if p==(current+1):
                    current = p
                else:
                    npad = current-start+1
                    self.roi.append([r, start, current, npad]) # row, start, end, number of pads
                    # start=False # new code, unsure how it worked without this

        self.roi = np.array(self.roi)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.roi):
            self.i += 1
            return self.roi[ self.i-1 ]
        else:
            raise StopIteration
        



def main():
    global finalROIArr

    # generate a parser for the command line arguments
    parser = argparse.ArgumentParser(description='Generate a .npy file of the continuous regions of interest which could correspond to tracklets')
    parser.add_argument('filename', help='The processed, zero-supressed .npy file (output from raw2npy.py)')
    parser.add_argument('out_file', help='The output .npy file to save the regions to')
    parser.add_argument('--nevents', '-n' , default=1000, type=int,
                        help='number of events to analyse')
    parser.add_argument('--printargs', action='store_true',
                        help='print arguments and exit')
    
    args = parser.parse_args()


    data = np.load(args.filename)
    print(np.shape(data))
    data = data[1:,:,:,:] # remove first event which is just zeros

    sumtracklet = np.zeros(30)
    ntracklet = 0

    # ------------------------------------------------------------------------
    # event loop
    for evno, d in enumerate(data):
            
        # Loop through regions of interest 
        for roi in regions_of_interest(d):

            tracklet = d[roi[0], roi[1]:roi[2], :]-BACKGROUND

             # add tracklet to ROI arr
            if type(finalROIArr) == type(None):
                finalROIArr = tracklet
            else:
                finalROIArr = np.vstack([finalROIArr,tracklet])
 
            # skip roi if data in first bins, (TODO: why?)
            # if ( np.sum(tracklet[:,0:6]) > 50 ): continue

            # fill pulseheight sum and plot tracklets
            sumtracklet += np.sum(tracklet, 0)
            ntracklet += 1
            # plt.plot(np.sum(tracklet,0))
        
    plt.show()
    finalROIArr = np.array(finalROIArr)
    np.save(args.out_file, finalROIArr)

if __name__ == "__main__":
    main()

