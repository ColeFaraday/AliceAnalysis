import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import argparse

def main():

    # generate a parser for the command line arguments
    parser = argparse.ArgumentParser(description='Generate a pulse-height plot.')
    parser.add_argument('data', help='the TRD processed data file (output from pre_process.py)')
    parser.add_argument('--printargs', action='store_true',
                        help='print arguments and exit')
    args = parser.parse_args()

    if args.printargs:
        print (args)
        exit(0)

    # Load file specified as argument
    arr = np.load(args.data)
    NUM_EVENTS, NUM_ROWS, NUM_COLUMNS, NUM_TIME_BINS = np.shape(arr)
    columns = np.arange(0, NUM_COLUMNS, 1)
    bins = np.arange(0, NUM_TIME_BINS, 1)

    # Remove background
    arrNoBackground = arr - 9.6
    arrNoBackground[arrNoBackground<=0] = 0

    #contour plot of means of ADC values of TRD - finding baseline of TRD
    print(np.shape(arrNoBackground[0,6,:,:]))
    plt.pcolor(bins,columns,arrNoBackground[0,6,:,:])
    plt.colorbar(label="$\mu$")
    plt.xlabel('Time bins')
    plt.ylabel('Columns')
    plt.title("Event 0, Row 6 - demo of possible traces")
    plt.show()



if __name__ == "__main__":
    main()
