# AliceAnalysis

Repository for the analysis code for the ALICE practical 2021 at UCT.

# Instructions 

1. Get the binary test data located on the TRD computer at `/data/raw/0783.o32`
2. Convert this data to a numpy array by running `python3 raw2npy.py 0783.o32`
3. This is a numpy array file which can be imported into a numpy array using the
   following python code `np.load("FILENAME.npy")`
4. The `pre_process.py` script takes in the input filename (of the raw data
   numpy file) and the output filename (to write to) and goes through some basic
   pre processing
5. The data in the output file can then be used for further analysis and is a 
   four dimensional numpy array with columns of "Event number", "Pad Row", "Pad
   Column", "Time Bin". The value of each element in the array represents an ADC
   count which relates to whether a particle was detected there.
