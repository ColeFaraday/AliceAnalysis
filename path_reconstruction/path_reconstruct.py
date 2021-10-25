import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import argparse

PAD_WIDTH= 6 # 6 mm pad width, fill in correct value

def calc_position(adcData, padWidth, )

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

if __name__ == "__main__":
    main()
