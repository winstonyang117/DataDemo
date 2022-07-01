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


def single_cardiac_cycle(duration=10, length=None, sampling_rate=100, heart_rate=60, respiratory_rate=15, systolic=120, diastolic=60):
    # It should generate a sscg signal, which includes the valley, 1st and 2nd peaks, i.e. a full cardiac cycle. 
    cardiac_length = int(10*sampling_rate/heart_rate) #sampling_rate #
    ind = random.randint(17, 34) 
    cardiac_s = scipy.signal.wavelets.daub(ind)
    cardiac_d = scipy.signal.wavelets.daub(ind)*0.3*diastolic/80 # change height to 0.3

    cardiac_s = scipy.signal.resample(cardiac_s, 100) # Same as the sampling rate 
    cardiac_d = scipy.signal.resample(cardiac_d, 100) # length of cardiac_d is fixed to 100
    cardiac_s = cardiac_s[0:40] # length of cardiac_s is fixed to 40

    distance = 180-systolic # systolic 81-180
    # distance = cardiac_length - len(cardiac_s) - len(cardiac_d) - systolic # here 140 = 40 (cardiac_s) + 100 (cardiac_d) as below
    zero_signal = np.zeros(distance)
   
    cardiac = np.concatenate([cardiac_s, zero_signal, cardiac_d]) # cardiac = cardiac_s + cardiac_d + zero_signal
    # print('length of cardiac is '+str(len(cardiac)))

    hr_10s = int(heart_rate*duration/60)
    # desired_single_cardiac_length = int(1000/hr_10s)
    cardiac = scipy.signal.resample(cardiac, 100) 
    
    #cardiac = np.tile(cardiac, hr_10s)
   
    
    # find the 1st peak AO 
    peak_1st = np.max(cardiac)
    peak_1st_index = np.argmax(cardiac)
    # print('1st peak index is: '+str(peak_1st_index))
    # find the 2nd peak - pAC
    half_cardiac_cycle_length = int(len(cardiac)/2)
    half_cardiac_cycle = cardiac[half_cardiac_cycle_length:]
    # print('length of half cardiac cycle is: '+str(len(half_cardiac_cycle)))
    peak_2nd = np.max(half_cardiac_cycle)
    peak_2nd_index = np.argmax(half_cardiac_cycle) + half_cardiac_cycle_length
    # print('2nd peak index is: '+str(peak_2nd_index))

    AO_point_index = peak_1st_index
    pAC_point_index = peak_2nd_index
    sscg_single_withlabel = np.append(cardiac, AO_point_index)
    sscg_single_withlabel = np.append(sscg_single_withlabel, pAC_point_index)
    sscg_single_withlabel = np.append(sscg_single_withlabel, heart_rate)
    sscg_single_withlabel = np.append(sscg_single_withlabel, systolic)
    sscg_single_withlabel = np.append(sscg_single_withlabel, diastolic)
    #print(len(sscg_single_withlabel))

    noise_signal = []
    noise_signal.append(sscg_single_withlabel)
    #print(len(noise_signal[0]))

    # add random noise based on the 1st sscg signal  
    heartbeats = int(heart_rate/6)
    for i in range(1, heartbeats+1):
        noise = random.uniform(0,0.3)
        # print(str(i)+'th noise signal and its noise level is: '+str(noise))
        temp_signal = []
        temp_signal = signal_distort(
                    cardiac,
                    sampling_rate=100,
                    noise_amplitude=noise,
                    noise_frequency=[5, 10, 100],
                    noise_shape="laplace",
                    random_state=100,
                    silent=True,
                )

        # find the 1st peak AO 
        peak_1st = np.max(temp_signal)
        peak_1st_index = np.argmax(temp_signal)
        # print('1st peak index is: '+str(peak_1st_index))
        # find the 2nd peak - pAC
        half_cardiac_cycle_length = int(len(temp_signal)/2)
        half_cardiac_cycle = temp_signal[half_cardiac_cycle_length:]
        # print('length of half cardiac cycle is: '+str(len(half_cardiac_cycle)))
        peak_2nd = np.max(half_cardiac_cycle)
        peak_2nd_index = np.argmax(half_cardiac_cycle) + half_cardiac_cycle_length
        # print('2nd peak index is: '+str(peak_2nd_index))

        AO_point_index = peak_1st_index
        pAC_point_index = peak_2nd_index
        sscg_single_withlabel = np.append(temp_signal, AO_point_index)
        sscg_single_withlabel = np.append(sscg_single_withlabel, pAC_point_index)
        sscg_single_withlabel = np.append(sscg_single_withlabel, heart_rate)
        sscg_single_withlabel = np.append(sscg_single_withlabel, systolic)
        sscg_single_withlabel = np.append(sscg_single_withlabel, diastolic)
        noise_signal.append(sscg_single_withlabel)
        # time.sleep(0.0005)

    return noise_signal


# sscg_base10s = single_cardiac_cycle(heart_rate=60, systolic=120, diastolic=60)
# print('th 10s SSCG signal length is: '+str(len(sscg_base10s[0])))heart_rate = random.randint(55, 120)
# heart_rate = random.randint(55, 120)
# systolic = random.randint(90, 130)
# diastolic = random.randint(50, 85)
# sscg_base10s = single_cardiac_cycle(heart_rate= heart_rate, systolic= systolic, diastolic=diastolic)
# print('th 10s SSCG signal length is: '+str(len(sscg_base10s[0])))


# # data visualization 
# noise_signal = single_cardiac_cycle(heart_rate=60, systolic=100, diastolic=55)

# k = 4
# y_ = noise_signal[k][:-5]
# index_AOpoint = int(noise_signal[k][-5])
# index_pACpoint = int(noise_signal[k][-4])
# y_AOpoint = y_[index_AOpoint]
# y_pACpoint = y_[index_pACpoint]

# print('This 10s SSCG signal has '+str(len(noise_signal))+ ' heartbeats')
# print('Each heartbeat length was resampled to 100')

# plt.figure(figsize = (16,2))
# plt.plot(y_)
# plt.scatter(index_AOpoint,y_AOpoint, c='r', marker='*')
# plt.scatter(index_pACpoint,y_pACpoint, c='r', marker='*')
# plt.show()


'''

All the codes above are based on given ONE specific HR, it can only generate a 10s SSCG signal with labels. And the data was organized as below:
signal + AO_index + pAC_index + HR + S + D

'''



