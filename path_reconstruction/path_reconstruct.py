import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import argparse
import helper as h
from matplotlib import cm
from matplotlib.colors import Normalize

PAD_WIDTH= 7.55 # pad width in the column direction

BACKGROUND = 9.6
SIGMA = 1/20 # 1/20th of the pad width, see 2021 report for details
fig = plt.figure(figsize=(8, 8))

def find_sub_pad_position(before, center, after):
    y = PAD_WIDTH/2 * np.log(after/before)/np.log(np.square(center)/(before*after))
    return y

def remove_background(arr):
    temp = arr + np.full(np.shape(arr), -1* BACKGROUND)
    temp[temp<0] = 0
    return temp

def plot_specific(regions, data, n):
    ''' Plot a specific tract (region n) in 3d'''
    ax = fig.add_subplot(111, projection='3d')


    print(regions[n,0], regions[n,1], regions[n,2], regions[n,3])
    bigTrack = data[regions[n,0], regions[n,1], regions[n,2]-3:regions[n,3]+4, :]
    # bigTrack = data[62, 11, 102:106, :]
    bigTrack = bigTrack[1:,:]
    bigTrack = np.swapaxes(bigTrack, 0,1)

    x_data, y_data = np.meshgrid( np.arange(bigTrack.shape[1]), np.arange(bigTrack.shape[0]) )
    
    x_data = x_data.flatten() + np.full(np.shape(x_data.flatten()), regions[n,2]-4)
    y_data = y_data.flatten()
    z_data = bigTrack.flatten()

    cmap = cm.get_cmap('winter')
    norm = Normalize(vmin=min(z_data), vmax=max(z_data))
    colors = cmap(norm(z_data))

    sc = cm.ScalarMappable(cmap=cmap,norm=norm)
    sc.set_array([])
    plt.colorbar(sc,fraction=0.046, pad=0.14) 

    ax.bar3d( x_data, y_data, np.zeros(len(z_data)), 1, 1, z_data, color=colors)
    ax.set_xlabel("Pad columns")
    ax.set_ylabel("Time bins")
    ax.set_zlabel("ADC count")
    plt.savefig("examplePath3D.pdf", bbox_inches="tight")

    plt.show()

def calc_three_pad_adc(centerColumnIndex, trackColumns):
    '''Takes in an array of indices of the center column of a particle hit (centerColumnIndex) and 2D array column vs time bin containing ADC data (trackColumns). Returns before center and after arrays which contain ADC data of the three pads surrounding and including the center pad for each time bin'''

    center = []
    before = []
    after = []
    
    for i,col in enumerate(centerColumnIndex):
        center.append(trackColumns[col-1, i]) # We need to pick out the ADC value located in the col'th column and the ith time bin
        before.append(trackColumns[col-2, i]) # same thing but column before
        after.append(trackColumns[col, i]) # same thing but column after

    before = np.array(before)
    center = np.array(center)
    after = np.array(after)
    return before, center, after

def main():


    # generate a parser for the command line arguments
    parser = argparse.ArgumentParser(description='Generate a pulse-height plot.')
    parser.add_argument('data', help='the TRD npy file (output from raw2npy.py)')
    parser.add_argument('regions', help='the TRD regions file (output from roi.py)')
    parser.add_argument('--plot', default=-1, help='Region number (zero indexed) to plot')
    parser.add_argument('--printargs', action='store_true', help='print arguments and exit')
    args = parser.parse_args()

    if args.printargs:
        print (args)
        exit(0)



    # Load file specified as argument
    regions = np.load(args.regions)
    data = np.load(args.data)
    data = data[1:,:,:,:] # remove first data file, as it is zero mostly


    regions = regions[np.where(np.logical_and(regions[:,3] <= 143-2, regions[:,4] <= 143-2))]
    
    angles = []
    angles_error = []

    print(len(np.where(np.sum(data,1)!=0))/len(data))
    maxIndex = np.unravel_index(np.argmax(data), np.shape(data))
    print(maxIndex, data[maxIndex])


    # Remove background data
    data = remove_background(data)
    print(regions)

    # Plot specified region
    if args.plot != -1: plot_specific(regions, data, int(args.plot))

    # Loop through the regions
    for i, region in enumerate(regions):
        trackColumns = data[region[0], region[1], region[2]-1:region[3]+2, :] # track of adc values in the specific pad we're looking at
        centerColumnIndex = np.argmax(trackColumns, 0) # array of columns which are the "center" of the collision, i.e. they have the highest ADC count

        before, center, after = calc_three_pad_adc(centerColumnIndex, trackColumns)
        deltaYArr = find_sub_pad_position(before, center, after)
        yArr = np.full(np.shape(deltaYArr), region[2]) + deltaYArr/PAD_WIDTH # in pad units
        try: 
            nanRemover = np.logical_not(np.isnan(yArr))
            yArr = yArr[nanRemover]
            x = np.arange(30)
            x = x[nanRemover]
            m, error_m, c, error_c = h.weighted_linear_least_squares(x,yArr,np.full(np.shape(x), SIGMA))

            fit = m*x + c

            # Plot the line of best fit
            if int(args.plot) == i:
                print(yArr)
                plt.errorbar(x, yArr, yerr=SIGMA, fmt=".", label="Pad hit positions")
                labelFit = "Linear least squares fit\n$m = " + str(h.uncertainty_sig_figs(m, error_m)) + "$\n$c = " + str(h.uncertainty_sig_figs(c,error_c)) + "$"
                plt.plot(x, fit, label=labelFit)
                plt.ylabel("Column number")
                plt.xlabel("Time bin")
                plt.legend()
                plt.savefig("bestfit.pdf", bbox_inches='tight')
                plt.show()

            if ((np.square(np.cos(m)) >1e-4) and (np.arctan(m) != np.NaN)):
                angles.append(np.abs(np.arctan(m)))
                angles_error.append(1/np.square(np.cos(m)) * error_m)

        except: 
            print("An error occured in region", i, ". Defaulting angle to NaN")
            angles.append(np.NaN)


    angles = np.array(angles)
    print(len(angles))
    angles = angles[np.logical_not(np.isnan(angles))]
    print(len(angles))
    angles = angles * 360/(2 * np.pi) # convert to degrees

    y,binEdges = np.histogram(angles,bins=10)
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    width      = 2
    yerr = np.sqrt(y)
    plt.bar(bincenters, y, width=width, yerr=yerr, label="Binned angle data with\nPoissonian error $\sqrt{n}$")
    plt.xlabel("Zenith incidence angle of cosmic ray (degrees)")
    plt.ylabel("Counts")
    plt.legend()
    plt.savefig("histogramAngles.pdf", bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
