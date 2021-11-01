#!/usr/bin/env python3
# Modifed version of https://github.com/CalleyRamcharan/ALICE2020Public/blob/main/roi.py

# Finds the regions of interest (i.e. where we expect to see tracklets) and saves them as a csv file

import o32reader as rdr
import adcarray as adc
import numpy as np
import matplotlib.pyplot as plt
import itertools
import argparse

# CONSTANTS
BACKGROUND = 9.6 # TODO: fill in the real value

finalROIArr = None

class regions_of_interest:

    def __init__ ( self, adcdata ):

        self.data = adcdata
        self.tbsum = np.sum(self.data, 2) # sum over time dimension (total number of hits per pad)

        # find points of interest - 2D array of hits = fired pads
        self.poi = np.argwhere(self.tbsum > 350) # TODO: This value seems arbitrary?
        print(self.poi)

        # create list for regions of interest
        self.roi = []

        # find continuous regions of interest
        for r in sorted(set(self.poi[:,0])): # loop through the rows containing points of interest

            # pad columns with hits
            pads = [x[1] for x in self.poi if x[0]==r]

            start = False
            current = False
            for p in pads+[999]:
                if not start:
                    start=p
                    current=p-1

                if p==(current+1):
                    current = p
                else:
                    npad = current-start+1
                    self.roi.append( {
                        'row': r,
                        'start': start,
                        'end': start+npad-1,
                        'npad': npad
                    } )

        #print (self.roi)

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
    parser = argparse.ArgumentParser(description='Generate a pulse-height plot.')
    parser.add_argument('filename', help='the TRD raw data file to process')
    parser.add_argument('out_file', help='the output data file for ROI')
    parser.add_argument('--nevents', '-n' , default=1000, type=int,
                        help='number of events to analyse')
    parser.add_argument('--allplots', action='store_true',
                        help='draw a crowded plot with all tracklets')
    parser.add_argument('--printargs', action='store_true',
                        help='print arguments and exit')
    
    args = parser.parse_args()

    if args.printargs:
        print (args)
        exit(0)
    
    # ------------------------------------------------------------------------
    # setup the reader
    reader = rdr.o32reader(args.filename)
    analyser = adc.adcarray()

    # ------------------------------------------------------------------------
    # some default settings
    DATA_EXCLUDE_MASK = np.zeros((12, 144, 30), dtype=bool)
    DATA_EXCLUDE_MASK[4:8,0:72,:] = True

    sumtracklet = np.zeros(30)
    ntracklet = 0


    # ------------------------------------------------------------------------
    # event loop
    for evno, raw_data in enumerate(reader):

        # limit number of events to be processed
        if evno >= args.nevents: break

        # skip the first event, which is usually a config event
        if evno == 0: continue
        
        # read the data
        try:
            analyser.analyse_event(raw_data)
        except adc.datafmt_error as e:
            continue

        data = analyser.data[:12]  # The last four rows are zeros.
        data[DATA_EXCLUDE_MASK] = 0


        for roi in regions_of_interest(data):

            roi['event'] = evno
        
            tracklet = data[roi['row'], roi['start']:roi['end'], :]-BACKGROUND
            print(roi['start'])

             # add tracklet to ROI arr
            if type(finalROIArr) == type(None):
                finalROIArr = tracklet
            else:
                finalROIArr = np.vstack([finalROIArr,tracklet])
 
            # skip roi if data in first bins
            if ( np.sum(tracklet[:,0:6]) > 50 ): continue

            # fill pulseheight sum and plot tracklets
            sumtracklet += np.sum(tracklet, 0)
            ntracklet += 1
            plt.plot(np.sum(tracklet,0))
        
    finalROIArr = np.array(finalROIArr)
    print(finalROIArr)
    np.save(args.out_file, finalROIArr)

if __name__ == "__main__":
    main()

