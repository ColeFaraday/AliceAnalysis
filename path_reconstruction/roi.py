#!/usr/bin/env python3
# Modifed version of https://github.com/CalleyRamcharan/ALICE2020Public/blob/main/roi.py

# Finds the regions of interest (i.e. where we expect to see tracklets) and saves them as a csv file

import itertools
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import colors
from matplotlib.ticker import MultipleLocator

# CONSTANTS
BACKGROUND = 9.6 # TODO: fill in the real value
THRESHOLD = 200

finalROIArr = []


# For latex output, have to set figsize=(x, y) in plot creation

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})


class regions_of_interest:

    def __init__ ( self, adcdata ):
        ''' Takes in adcdata array which is a three dimensional array of the adcdata for a specific event'''

        self.data = adcdata
        self.tbsum = np.sum(self.data, 2) # sum over time dimension (total number of hits per pad)

        # find points of interest - 2D array of hits = fired pads
        self.poi = np.argwhere(self.tbsum > THRESHOLD) # TODO: This value seems arbitrary?

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
                    start=False # new code, unsure how it worked without this

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


    data = np.load(args.filename, allow_pickle=True)
    print(np.shape(data))
    data = data[1:,:,:,:] # remove first event which is just zeros

    sumtracklet = np.zeros(30)
    ntracklet = 0

    # ------------------------------------------------------------------------
    # event loop
    for evno, d in enumerate(data):
            

        # Loop through regions of interest 
        for roi in regions_of_interest(d):

            # tracklet = d[roi[0], roi[1]:roi[2], :]-BACKGROUND
            # Only look for regions with length greater than 1
            if roi[3] <= 1: continue
            entry = [evno, roi[0], roi[1], roi[2], roi[3]]

            finalROIArr.append(entry)

 
            # skip roi if data in first bins, (TODO: why?)
            # if ( np.sum(tracklet[:,0:6]) > 50 ): continue

            # fill pulseheight sum and plot tracklets
            # sumtracklet += np.sum(tracklet, 0)
            # ntracklet += 1

    finalROIArr = np.array(finalROIArr)
    print(finalROIArr)



    # create discrete colormap
    cmap = colors.ListedColormap(['grey', 'blue'])
    # bounds = [0,10,20]
    # norm = colors.BoundaryNorm(bounds, cmap.N)
    eventNum = 2
    data2d = np.sum(data[eventNum, :, :, :], 2)

    regions2D = finalROIArr[np.argwhere(finalROIArr[:,0] == eventNum)]
    regionsInData = np.zeros((12,50))

    for x in regions2D:
        x = x[0]
        regionsInData[ x[1], x[2]:x[3]] = 1


    print("regions", regions2D)

    fig, ax = plt.subplots(figsize=(8,3))
    ax.imshow(regionsInData, cmap=cmap)
    plt.xlim([0, 49])
    plt.ylim([0, 11])


    # draw gridlines
    # ax.grid(which='both', axis='both', linestyle='-', color='k', linewidth=1)
    # ax.minorticks_on()
    # ax.xaxis.set_minor_locator(MultipleLocator(1))
    # ax.yaxis.set_minor_locator(MultipleLocator(1))
    # ax.set_xticks(np.arange(0, 144, 1));
    # ax.set_yticks(np.arange(0, 12, 1));
    ax.set_xlabel("Pad columns")
    ax.set_ylabel("Pad rows")

    # plt.show()

    finalROIArr = np.array(finalROIArr)
    np.save(args.out_file, finalROIArr)

    plt.savefig('../../tex/regions.pgf', bbox_inches='tight')

if __name__ == "__main__":
    main()
