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

    alldata = np.genfromtxt(args.filename, float, "#", ",", skip_header=1, usecols=(0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36))
    print(alldata)
    # test = np.reshape(alldata, (int(np.max(alldata[:,0])-1), 12, 144, 30))
    # print(test)
    # print(np.shape(test))
    print(np.shape(alldata))
    eventNum = alldata[:,0]
    padrow = alldata[:,1]
    padcol = alldata[:,2]
    timeBins = alldata[:,3:]
    print(len(eventNum)/5)
    with np.printoptions(threshold=np.inf):
        print(np.sort(np.unique(padrow)))
        print(len(padrow)/len(np.unique(padrow)))
        print(len(np.unique(padrow)))
        print(np.sort(np.unique(padcol)))

    data = np.concatenate((eventNum, padrow, padcol, timeBins))


    # # Data exclude mask
    # DATA_EXCLUDE_MASK = np.zeros((999, 12, 144, 30), dtype=bool)

    # # Exlude broken section of the detector (might not be broken in 2021)
    # DATA_EXCLUDE_MASK [:,8:12, 0:72,:] = True
    # alldata[DATA_EXCLUDE_MASK] = 0

    
    #contour plot of means of ADC values of TRD - finding baseline of TRD
    plt.pcolor(padcol,padrow,np.mean(np.mean(data, 3), 0))
    plt.colorbar(label="$\mu$")
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.title("Baseline across the TRD")
    plt.show()

    # Save array as numpy array file
    # np.save(args.new_filename, alldata)




if __name__ == "__main__":
    main()

