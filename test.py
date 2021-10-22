import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import seaborn as sns

arr = np.load("../data/processed_0783.npy")
arr = arr - 9.6
arr[arr<=0] = 0
NUM_EVENT, NUM_PAD_ROW, NUM_PADS, NUM_TIME_BINS =  np.shape(arr)

print(np.shape(arr))


mean = np.average(np.average(arr, axis=3), axis=0)
rows = np.arange(0, NUM_PAD_ROW, 1)
pads = np.arange(0, NUM_PADS, 1)

# ax = sns.heatmap(mean)

for i in range(30):
    ax = sns.heatmap(arr[4,:,:,i])
    plt.show()


ax = sns.heatmap(arr[0,6,:,:])
plt.show()
