# DataDemo
Time Series Data Simulation and Analytics Demo

## Data simulations (general use)

The SCG data simulation is built on the top of NeuroKit2: https://github.com/neuropsychology/NeuroKit

Generate the simulated SCG data:
```
  python3 simscg.py
```

Visualize the saved SCG data npy file:
```
  python3 view_data.py [xxx.npy] [num_labels]
```

Perform clustering of the simulated data on quality evaluation:
```
  python3 evalscg.py
```

## Synthetic data generation (specific use)
Take a look at these two python files. **SSCG.py** and **sscg_long.py**.

1. SSCG.py can generate a 10s SSCG signal with labels. Given specific HR, systolic and diastolic, it will first generate one cardiac signal, then add noise 
based on it. Repeating this process until we get all the cardiac cycles(= HR/6). And the data is organized as below: 
```
signal + AO_index + pAC_index + HR + S + D
```
It should be noted that for each cardiac cycle, the signal is resampled to length of 100. So, the total length is 105 for each row.

2. sscg_long.py can generate at least 1 hour SSCG data with labels based on the 'single signal(10s) generation' function in SSCG.py.
```
10s -> AO_index, pAC_index, HR, S, D
1 hour = 3600s -> 360 AO_index, pAC_index, HR, S, D
```
