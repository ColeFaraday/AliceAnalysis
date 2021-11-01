import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import argparse

PAD_WIDTH= 6 # 6 mm pad width, fill in correct value

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
    roiArr = np.genfromtxt(args.data, float, "#", " ", skip_header=1)
    show_test_event(roiArr, 0)

def show_test_event(roiArr, evNum):
    print(roiArr[evNum])


if __name__ == "__main__":
    main()
