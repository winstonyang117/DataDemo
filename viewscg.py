#!/usr/bin/env python3

# %%
import warnings
warnings.filterwarnings('ignore')
# Load NeuroKit and other useful packages
import sys
import time
sys.path.insert(1, './')
# import datasim as nk
import numpy as np
# import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
import random
# from scipy import signal
# #%matplotlib inline
# from tslearn.clustering import KShape
# from tslearn.datasets import CachedDatasets
# from tslearn.preprocessing import TimeSeriesScalerMeanVariance

plt.rcParams['figure.figsize'] = [20, 7]  # Bigger images

pause = False

def onclick(event):
    global pause 
    if event.dblclick:
        quit()
    else:
        pause = not pause
        # print(pause)


if(len(sys.argv) > 1):
    file = sys.argv[1] #http
    file_list = [ [file] ]
else:
    file_list = [
            ['./data/classifier_train_data.npy'],
            # ['./data/training_set.npy'], #5000
            # ['./data/good_set.npy'], #1500
            # ['./data/bad_set.npy'], #1500
            # ['./data/mixed_set.npy'],
            ]

for file in file_list:
    data_set = np.load(file[0])
    print(data_set.shape)
    N = data_set.shape[0]
    M = 10

    data = data_set[:,0:1000]
    labels = data_set[:,1000:]

    fig, ax = plt.subplots()
    # ax.plot(np.random.rand(10))

    for k in range(int(N/(2*M))): 
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
            # plt.text(0, 0, "Single click to pause/unpause, double click to quit")
        fig.text(0.3, 0.95, "Single click to pause/unpause, double click to quit. Do not click on window close icon", size=10, rotation=0,
            ha="center", va="center",
            bbox=dict(boxstyle="round",
                    ec=(1., 0.5, 0.5),
                    fc=(1., 0.8, 0.8),
                    )
            )
        for ind in range(M):
            # plt.figure(figsize=(20, 4))
            # fig, ax = plt.subplot(M,2,2*ind+1)
            # ax.cla()   # clear previous plot
            # ax.plot(data[k*2*M + 2*ind])
            # ax.title(f'index: [{k*2*M + 2*ind}] Parameters: {parameters[k*2*M + 2*ind]}')
            # ax.ylabel('Amplitude')
            # ax.xlabel('Number of Samples')
            # cid = fig.canvas.mpl_connect('button_press_event', onclick)

            index = k*2*M + 2*ind
            if labels[index][-1] == 1:
                color = 'k-' # bad data
            else:
                color = 'g-' # good data
            plt.subplot(M,2,2*ind+1)
            plt.cla()   # clear previous plot
            plt.plot(data[index], color)
            plt.title(f'index: [{index}] labels: {labels[index].astype(int)}')
            plt.ylabel('Amplitude')
            plt.xlabel('Number of Samples')

            index = k*2*M + 2*ind + 1
            if labels[index][-1] == 1: 
                color = 'k-' # bad data
            else:
                color = 'g-' # good data            
            plt.subplot(M,2,2*ind+2)
            plt.cla()   # clear previous plot
            plt.plot(data[index], color)
            plt.title(f'index: [{index}] labels: {labels[index].astype(int)}')
            plt.ylabel('Amplitude')
            plt.xlabel('Number of Samples')
        plt.pause(0.05)
        while(pause):
            plt.pause(0.05)

    plt.show()
