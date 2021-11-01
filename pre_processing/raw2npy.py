#!/usr/bin/env python3
# Adapted from https://github.com/CalleyRamcharan/ALICE2020Public

#import defaults
import o32reader as rdr
import adcarray as adc
import numpy as np
import itertools
import argparse


#UNSYNCHRONISED NPY WRITER CLASS - for synchronisation with scintillator data use raw2npySync.py
if __name__ == "__main__":

    # ------------------------------------------------------------------------
    # generate a parser for the command line arguments
    parser = argparse.ArgumentParser(description='Generate a pulse-height plot.')
    parser.add_argument('filename', help='the TRD raw data file to process')
    parser.add_argument('filename_out', help='the name of the npy file to produce')
    parser.add_argument('--nevents', '-n' , default=1000, type=int, help='print event number every N events')
    parser.add_argument('--supress', '-s' , default=True, type=bool, help='Zero supress the region of the detector which is broken')
    parser.add_argument('--progress', '-p' , default=-1, type=int, help='print event number every N events')
    parser.add_argument('--printargs', action='store_true', help='print arguments and exit')

    args = parser.parse_args()

    if args.printargs:
        print (args)
        exit(0)

    # ------------------------------------------------------------------------
    # setup the reader
    reader = rdr.o32reader(args.filename)
    analyser = adc.adcarray()


    sumtrkl = np.zeros(30)
    ntrkl = 0


    # ------------------------------------------------------------------------
    # create the histogram

    #hist, bins = np.histogram((), np.linspace(0, 20, 2000))

    alldata = None

    # ------------------------------------------------------------------------
    # event loop
    for evno, raw_data in enumerate(reader):

        # limit number of events to be processed
        if evno >= args.nevents: break

        # skip the first event, which is usually a config event
        if evno == 0: continue

        if args.progress > 0 and evno%args.progress==0:
            print ("###  EVENT %d" % evno )

        # read the data
        try:
            analyser.analyse_event(raw_data)
        except adc.datafmt_error as e:
            print ("data format error in event %d" % evno)
            continue

        data = analyser.data[:12]  # The last four rows are zeros.

        if alldata is None:
            alldata = np.expand_dims(data, axis=0)
        else:
            alldata = np.concatenate( (alldata,np.expand_dims(data, axis=0)), axis=0 )


    print(np.shape(alldata))
    # Zero supression of the broken region of the detector. Note that this region may change and should be worked out using background.py
    if args.supress==True:
        DATA_EXCLUDE_MASK = np.zeros((args.nevents-1, 12, 144, 30), dtype=bool)
        DATA_EXCLUDE_MASK [:,4:8, 72:,:] = True
        alldata[DATA_EXCLUDE_MASK] = 0

    np.save(args.filename_out+'.npy', alldata)
