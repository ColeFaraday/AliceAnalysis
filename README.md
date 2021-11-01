# AliceAnalysis

Repository for the analysis code for the ALICE practical 2021 at UCT.

# Instructions 

1. The binary `o32` data files are located in the `data` directory
2. This data can be converted into a `.npy` file using`raw2npy.py` and can be told to zero supress the broken region of the detector. The following command will output a `.npy` file and will zero supress the broken region of the detector (if you are in the directory of `raw2npy.py` and the input data file has 5 events).
```sh
python3 raw2npy.py ../data/trigger_data/daq-30Oct2021-152917321808-trigger.o32 ../data/daq-30Oct2021.npy --supress=True -n 5
```
.3. This is a numpy array file which can be imported into a numpy array using the
   following python code `np.load("FILENAME.npy")`
5. The data in the npy file can be used for further analysis and is a 
   four dimensional numpy array with columns of "Event number", "Pad Row", "Pad
   Column", "Time Bin". The value of each element in the array represents an ADC
   count which relates to whether a particle was detected there.
