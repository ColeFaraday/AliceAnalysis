import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import argparse
import subprocess

def main():
    # Add arguments
    parser = argparse.ArgumentParser(description='pre-process data to mask certain sections etc.')
    parser.add_argument('filename', help='the raw data file to import')
    parser.add_argument('--nevents', '-n' , default=1000, type=int, help='number of events to analyse')
    parser.add_argument('new_filename', help='the numpy (.npy) file to export')
    parser.add_argument('--printargs', action='store_true',
                        help='print arguments and exit')
    args = parser.parse_args()
    fileNoExt = args.filename[:-4]
    subprocess.run(["python3", "raw2npy.py", str(args.filename), str(fileNoExt+"_raw"), str(args.nevents)])

    arr = np.load(args.filename+"_raw.npy")

    # Zero supression of the broken region of the detector. Note that this region may change and should be worked out using background.py
    DATA_EXCLUDE_MASK = np.zeros((args.nevents, 12, 144, 30), dtype=bool)
    DATA_EXCLUDE_MASK [:,4:8, 72:,:] = True
    arr[DATA_EXCLUDE_MASK] = 0

    
    
    print(arr)
    # Save array as numpy array file
    # np.save(args.new_filename, alldata)




if __name__ == "__main__":
    main()

