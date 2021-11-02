import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import argparse
from matplotlib import cm
from matplotlib.colors import Normalize

PAD_WIDTH= 7.55 # pad width in the column direction

BACKGROUND = 9.6

def find_sub_pad_position(before, center, after):
    y = PAD_WIDTH/2 * np.log(after/before)/np.log(np.square(center)/(before*after))
    return y

def remove_background(arr):
    temp = arr + np.full(np.shape(arr), -1* BACKGROUND)
    temp[temp<0] = 0
    return temp

def plot_specific(regions, data, n):
    ''' Plot a specific tract (region n) in 3d'''
    fig = plt.figure(figsize=(8, 3))
    ax = fig.add_subplot(121, projection='3d')

    bigTrack = data[regions[n,0], regions[n,1], regions[n,2]:regions[n,3], :]
    bigTrack = bigTrack[1:,:]
    bigTrack = np.swapaxes(bigTrack, 0,1)

    x_data, y_data = np.meshgrid( np.arange(bigTrack.shape[1]), np.arange(bigTrack.shape[0]) )
    
    x_data = x_data.flatten()
    y_data = y_data.flatten()
    z_data = bigTrack.flatten()

    cmap = cm.get_cmap('winter')
    norm = Normalize(vmin=min(z_data), vmax=max(z_data))
    colors = cmap(norm(z_data))

    sc = cm.ScalarMappable(cmap=cmap,norm=norm)
    sc.set_array([])
    plt.colorbar(sc,fraction=0.046, pad=0.04) 

    ax.bar3d( x_data, y_data, np.zeros(len(z_data)), 1, 1, z_data, color=colors)
    ax.set_xlabel("Pad columns")
    ax.set_ylabel("Time bins")
    ax.set_zlabel("ADC count")

    plt.show()

def calc_three_pad_adc(centerColumnIndex, trackColumns):
    '''Takes in an array of indices of the center column of a particle hit (centerColumnIndex) and 2D array column vs time bin containing ADC data (trackColumns). Returns before center and after arrays which contain ADC data of the three pads surrounding and including the center pad for each time bin'''

    center = []
    before = []
    after = []
    
    for i,col in enumerate(centerColumnIndex):
        center.append(trackColumns[col, i]) # We need to pick out the ADC value located in the col'th column and the ith time bin
        before.append(trackColumns[col-1, i]) # same thing but column before
        after.append(trackColumns[col+1, i]) # same thing but column after

    before = np.array(before)
    center = np.array(center)
    after = np.array(after)
    return before, center, after

def main():

    # generate a parser for the command line arguments
    parser = argparse.ArgumentParser(description='Generate a pulse-height plot.')
    parser.add_argument('data', help='the TRD npy file (output from raw2npy.py)')
    parser.add_argument('regions', help='the TRD regions file (output from roi.py)')
    parser.add_argument('--printargs', action='store_true',
                        help='print arguments and exit')
    args = parser.parse_args()

    if args.printargs:
        print (args)
        exit(0)

    # Load file specified as argument
    regions = np.load(args.regions)
    data = np.load(args.data)
    print(regions)

    data = remove_background(data)

    plot_specific(regions, data, 14)

    for region in [regions[18]]: # change later
        trackColumns = data[region[0], region[1], region[2]:region[3], :] # track of adc values in the specific pad we're looking at
        centerColumnIndex = np.argmax(trackColumns, 0) # array of columns which are the "center" of the collision, i.e. they have the highest ADC count

        before, center, after = calc_three_pad_adc(centerColumnIndex, trackColumns)
        deltaYArr = find_sub_pad_position(before, center, after)
        yArr = centerColumnIndex + deltaYArr/PAD_WIDTH # in pad units
        nanRemover = np.logical_not(np.isnan(yArr))
        yArr = yArr[nanRemover]
        x = np.arange(30)
        x = x[nanRemover]
        m,c = np.polyfit(x,yArr,1)
        fit = m*x + c
        plt.plot(x, yArr, ".")
        plt.plot(x, fit)
        plt.ylim(ymin=0, ymax=6)
        print("Angle:", np.arctan(m))
        plt.show()
        print(yArr)

if __name__ == "__main__":
    main()
