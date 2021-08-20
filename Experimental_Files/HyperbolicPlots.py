# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 11:15:06 2021

@author: LocalAdmin
"""

import numpy as np
from scipy import signal 
from matplotlib import pyplot as plt

def Duration(sampleRate,points):
    return points/sampleRate


def Points(sampleRate,duration):
    return int(duration*sampleRate)


def Times(sampleRate, duration=None, recordLength=None):
    
    if (duration is None):
        duration=Duration(sampleRate,recordLength)
        return  np.linspace(0, recordLength/sampleRate, recordLength, dtype=np.float32)
    elif (recordLength is None):
        numPoints=Points(sampleRate,duration)
        return  np.linspace(0, numPoints/sampleRate, numPoints, dtype=np.float32)
    else:
        print('You need to supply either a number of Points or a duration')
        return 0
    return 0



def chirpedSawtooth(startFreq,sweepWidth,length):
    
    freqs=np.linspace(startFreq,startFreq+sweepWidth/2,length,dtype=np.float32)
    return freqs

def tanHypeSawtooth(beta,amp,center,length,coupling=1):
    
    x=np.linspace(-1,1,length,dtype=np.float32)
    if coupling == 1:
        freqs=(amp*beta)/(2*np.pi)*np.tanh(beta*x) + center
    if coupling == 0:
        freqs=amp/(2)*np.tanh(beta*x) + center
    return freqs

def SecHypePulse(width,length,amp,offset, padding, typeset=0):
    
    x=np.linspace(-1, 1, length)
    y=amp*(1/np.cosh(width*x))+offset
    y=np.concatenate((np.zeros(padding[0]),y,np.zeros(padding[1])))
    if not(typeset):
        z=y.astype(np.int32)
        return z
    return y


    



# Must have 2 of these 3 to determine all
SR=25e9  # in Samples/Sec
D=100e-06 # Seconds

t1=Times(SR,duration=D)



# For a Simple Sine wave Numpy has what we need. Just specify a frequency and
#----------------------------------------------------------------------------
# freq=100e6 # 100MHz 
# wfmData1 = np.sin(2*np.pi*freq*t1)

# fig1, ax1 = plt.subplots()
# ax1.plot(t1[1:2000], wfmData1[1:2000])
# ax1.set_title("Sine modulation")
# ax1.set_xlabel("Time")
# #----------------------------------------------------------------------------


# # For a sawtooth wave Scipy has what we need. Just specify a frequency and

# #----------------------------------------------------------------------------
# freq=100e6 # 100MHz 
# wfmData2 = signal.sawtooth(2*np.pi*freq*t1)
# fig2, ax2 = plt.subplots()
# ax2.plot(t1[1:2000], wfmData2[1:2000])
# ax2.set_title("Sawtooth/Serrodyne modulation")
# ax2.set_xlabel("Time")
#----------------------------------------------------------------------------



#Now We can add an envelope or chirp fuction as well. Just specify what it should be

# freq=np.linspace(0,100e6,len(t1),dtype=np.float32)
# env= np.ones(len(freq))
# env[0:10000]=2
# env[10000:20000]=0.5
# A1=np.multiply(freq,env)
# wfmData = signal.sawtooth(2*np.pi*np.multiply(freq,t1))
# plt.plot(t1[0:500000], wfmData[0:500000])
# plt.title("Chirped sawtooth from 0MHz to 100MHz")
# plt.show()



#Make a hyperbolic tangent modulated chirp function in frequency

freq=np.linspace(0,1e6,len(t1),dtype=np.float32)
beta = 10
mu = 1e6
center = 0.5e6
y1=tanHypeSawtooth(beta,mu,center,len(t1),1) #Beta, amp (\mu), center
wfmData2 = signal.sawtooth(2*np.pi*np.multiply(freq,t1))
wfmData1 = signal.sawtooth(2*np.pi*np.multiply(y1,t1))
offset = 0
amp = 600
a = amp*(1/np.cosh(beta*t1))+ offset
# plt.plot(t1, a)
# plt.title("Amplitude modulation")
# plt.show()

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(t1, wfmData1, 'r-',label = "tanhyp modulated")
ax2.plot(t1, wfmData2, 'b-', label = "chirped sawtooth")
ax1.set_xlabel("Time",fontsize=14)
ax1.plot(t1, wfmData2)
ax1.set_title("tanhyp modulated chirped sawtooth vs chirped sawtooth")
ax1.legend(loc="upper left")
ax2.legend(loc="lower right")
plt.show()



'''
# create figure and axis objects with subplots()
fig,ax = plt.subplots()
# make a plot
ax.plot(t1, wfmData1,'r-',label= "modulated sawtooth")
ax.set_ylabel("Signal amplitude",color="red",fontsize=14)
ax.set_title("tanhyp modulated chirped waveform")


# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(t1, y1, 'b-', label=r'$(\frac{\mu \beta}{2\pi}) \tanh \beta t$' "\n"
        r'$\mu = 1MHz; \beta = 4; center = 1MHz $')
# set x-axis label

# set y-axis label
ax2.set_ylabel("Frequency",color="blue",fontsize=14)
ax2.legend(loc="lower right")
plt.tight_layout() 
plt.show()
'''
#Make a hyperbolic secant pulse for the arbitrary function generator
# z=SecHypePulse(7,2000,600,400,(1000, 1000))
# plt.plot(z)

# save the plot as a file
# fig.savefig('two_different_y_axis_for_single_python_plot_with_twinx.jpg',
#             format='jpeg',
#             dpi=100,
#             bbox_inches='tight')






