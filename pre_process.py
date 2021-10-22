import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import argparse

def main():
    # Add arguments
    parser = argparse.ArgumentParser(description='pre-process data to mask certain sections etc.')
    parser.add_argument('filename', help='the numpy (.npy) file to import')
    parser.add_argument('new_filename', help='the numpy (.npy) file to export')
    parser.add_argument('--printargs', action='store_true',
                        help='print arguments and exit')

    args = parser.parse_args()

    alldata = np.load(args.filename,allow_pickle=True)
    print(alldata)

    # Data exclude mask
    DATA_EXCLUDE_MASK = np.zeros((999, 12, 144, 30), dtype=bool)

    # Exlude broken section of the detector (might not be broken in 2021)
    DATA_EXCLUDE_MASK [:,8:12, 0:72,:] = True
    alldata[DATA_EXCLUDE_MASK] = 0

    # Save array as numpy array file
    np.save(args.new_filename, alldata)




if __name__ == "__main__":
    main()

