from SSCG import single_cardiac_cycle 

import math
import random
import numpy as np
import scipy
import time
from datasim.signal import signal_distort
from datasim.signal import signal_resample
import matplotlib.pyplot as plt
from scipy import signal
from tqdm import tqdm

'''
This code was used to generate at least 1 hour SSCG data with labels based on the 'single signal(10s) generation' function in SSCG.py.
10s -> AO_index, pAC_index, HR, S, D
1 hour = 3600s -> 360 AO_index, pAC_index, HR, S, D
'''
sscg_long = []
for i in tqdm(range(0, 360)):
    heart_rate = random.randint(55, 120)
    systolic = random.randint(90, 130)
    diastolic = random.randint(50, 85)
    print(str(i)+'th 10s SSCG signal -> '+'HR: '+str(heart_rate)+' Systolic: '+str(systolic)+' Diastolic: '+str(diastolic))

    sscg_base10s = single_cardiac_cycle(heart_rate= heart_rate, systolic= systolic, diastolic=diastolic)
    print(str(i)+'th 10s SSCG signal size is: '+str(len(sscg_base10s))+' * '+str(len(sscg_base10s[5])))
    if i == 0:
        sscg_long = sscg_base10s
    else: 
        sscg_long = np.vstack((sscg_long, sscg_base10s))
    
    time.sleep(0.0005)

print('Final size of long SSCG signal is: '+str(sscg_long.shape))
print(str(sscg_long.shape[0])+'heartbeat (cardiac cycles) are generated!!')


sscg_long_visual = sscg_long[:, :-5] # exclude the labels
sscg_long_visual = sscg_long_visual.flatten()
print('Total length of long SSCG signal is: '+str(sscg_long_visual.shape[0]))


# data visualization 
desired_visual_range = 1000 # minmum = 100 equals to 1 heartbeat
x = list(range(desired_visual_range))
x = np.array(x)/100
plt.figure(figsize = (16,2))
plt.xlabel('Heartbeats')
plt.ylabel('Amplitude')
plt.title('Synthetic-SCG data for a long period')
plt.plot(x, sscg_long_visual[:desired_visual_range])
plt.show()