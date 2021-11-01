import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import argparse


def main():
    # Argument parser
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('data', help='the TRD processed data file (output from pre_process.py)')
    parser.add_argument('--printargs', action='store_true',
                        help='print arguments and exit')

    args = parser.parse_args()

    if args.printargs:
        print (args)
        exit(0)

    # Load file specified as argument
    arr = np.load(args.data)
    print(np.shape(arr))
    NUM_EVENTS, NUM_ROWS, NUM_COLUMNS, NUM_TIME_BINS = np.shape(arr)


    DATA_EXCLUDE_MASK = np.zeros((4, 12, 144, 30), dtype=bool)
    DATA_EXCLUDE_MASK [:,4:8, 72:,:] = True
    arr[DATA_EXCLUDE_MASK] = 0

    # Average along time and event dimensions
    mean = np.average(np.average(arr, axis=3), axis=0)
    columns = np.arange(0, NUM_COLUMNS, 1)
    rows = np.arange(0, NUM_ROWS, 1)
    print(np.shape(columns), np.shape(rows), np.shape(mean))

    #contour plot of means of ADC values of TRD - finding baseline of TRD
    plt.pcolor(columns,rows,mean)
    plt.colorbar(label="$\mu$")
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.title("Baseline across the TRD")
    plt.show()

if __name__ == "__main__":
    main()
