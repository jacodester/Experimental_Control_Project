# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 11:26:53 2021

@author: LocalAdmin
"""

import time
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal,interpolate 
import csv




def Duration(sampleRate,points):
    return points/sampleRate


def Points(sampleRate,duration):
    return int(duration*sampleRate)


def Times(sampleRate, duration=None, recordLength=None):
    """
    Make a time array of the correct data type for a waveform based on the 
    device sampling rate, and either a supplied duration or number of waveform
    points

    Parameters
    ----------
    sampleRate : float
        AWG sampling rate. This shouldnt change much, but for different devices
        it can. 
    duration : TYPE, optional
        DESCRIPTION. The default is None.
    recordLength : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
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

def OptimiseWaveform(wfmData,freqs,NormWaveform=1):
    """
    Uses the known PM calibrations to optimise shifted optical power at a series
    of wavelengths for a given shifting waveform. 

    Parameters
    ----------
    wfmData : array of float64
        the waveform to be optimized
    freqs : array of float32
        defines the frequency range over which the waveform data is being optimized
    NormWaveform : int, optional
        which premade optimization case to use. The default is 1.

    Returns
    -------
    wfmDataOUT : array of float64
        the waveform data after it has been amplitude scaled to produce the best shifting

    """
    if (NormWaveform == 1):
        NormVals = np.ones(len(wfmData))
    if (NormWaveform == 5):
        NormVals = np.multiply([0.160, 0.170, 0.190, 0.200, 0.200, 0.210, 0.210, 0.210, 0.220, 0.240, 0.260, 0.270, 0.280, 0.290, 0.310, 0.310, 0.310, 0.330, 0.330, .330, 0.350, 0.360, 0.380, 0.400, 0.400, 0.400, 0.400, 0.420, 0.420, 0.430, 0.430, 0.430, 0.430, 0.430, 0.430],2)
        NormFreqs=np.concatenate((np.arange(100e6,2.1e9,100e6), np.arange(2.2e9,5.2e9,200e6)),0)
    if (NormWaveform == 6):
        NormVals = np.multiply([1.2, 1.25, 1.36, 1.38, 1.42, 1.42, 1.55, 1.39, 1.39, 1.55, 1.73, 1.74, 2.18, 2.18, 2.2, 2.3, 2.3, 2.5, 2.4, 2.5],1)
        NormFreqs=np.arange(100e6,2.1e9,100e6)
    if (NormWaveform == 7):
        NormVals = np.multiply([1.2, 1.25, 1.36, 1.38, 1.42, 1.42, 1.55, 1.39, 1.39, 1.55, 1.73, 1.74, 2.18, 2.18, 2.2, 2.3, 2.3, 2.5, 2.4, 2.5],1)
        NormFreqs=np.arange(100e6,2.1e9,100e6)
    f = interpolate.interp1d(NormFreqs,NormVals,fill_value='extrapolate')
    intnormvals=f(abs(freqs))
    #plt.plot(NormFreqs, NormVals,'o',freqs,intnormvals,'-')
    wfmDataOUT = np.multiply(intnormvals,wfmData)
    return wfmDataOUT

def chirpedSawtooth(startFreq,sweepWidth,length):
    """
    Makes a sawtooth waveform of the specified number of points with the given
    start frequency, and sweep width. 

    Parameters
    ----------
    startFreq : float
        Frequency specified in Hz to start the chirp
    sweepWidth : float
        range of frequencies over which to chirp the waveform
    length : int
        integer number of points that defines the number of points in the
        produced frequency array

    Returns
    -------
    freqs : numpy array
        array of frequencies coresponding to the input parameters. 

    """
    freqs=np.linspace(startFreq,startFreq+sweepWidth/2,length,dtype=np.float32)
    return freqs

def tanHypeSawtooth(beta,amp,center,length,coupling=1):
    """
    Generate a hyperbolic tangent frequency modulated sawtooth waveform for 
    use with hyperbolic secant amplitude modulated pulses

    Parameters
    ----------
    width : float
        Parameter describing the sharpness of the hyperbolic tangent that
        modulates the sawtooth frequency. From Literature, should match with 
        the duration of the hyperbolic secant pulse
    amp : float
        defines the total amplitude of swept frequency range around the center.
    center : float
        center frequency of the pulse
    length : int
        integer number of points that defines the number of points in the
        produced frequency array

    Returns
    -------
    freqs : numpy array
        array of frequencies coresponding to the input parameters.

    """
    x=np.linspace(-1,1,length,dtype=np.float32)
    if coupling == 1:
        freqs=(amp*beta)/(2*np.pi)*np.tanh(beta*x) + center
    if coupling == 0:
        freqs=amp/(2)*np.tanh(beta*x) + center
    return freqs

def SecHypePulse(width,length,amp,offset, padding, typeset=0):
    """
    Make Hyperbolic secant pulse for an arb waveform device

    Parameters
    ----------
    width : float
        width parameter of the hyperbolic secant function
    length : int
        length of the waveform in points
    amp : float
        total amplitude of the peak for the hyperbolic secant function
    offset : float
        verticle offset of the pulse
    padding : tuple
        a number of padding points on either side of the pulse itself. Amplitude
        of these points is zero. eg. (10, 1000) is 10 and then 1000 points on
        the beginning and end. 
    typeset : Bool, optional
        Either 1 or 0. Likely this waveform will be used in the AFG to set an
        arbitrary function. If that is the case the type needs to be an integer 
        for upload to the device. This is the automatic case.
        The default is 0.

    Returns
    -------
    numpy array
         an array of specified length that holds the function values
    """
    x=np.linspace(-1, 1, length)
    y=amp*(1/np.cosh(width*x))+offset
    y=np.concatenate((np.zeros(padding[0]),y,np.zeros(padding[1])))
    if not(typeset):
        z=y.astype(np.int32)
        return z
    return y
def ManyHoleWaveform(freqs,widths,shape,times):
    """
    Generates wavefor of simultaneous frequencies using sinusoidal modulation
    and hyperrbolic secant pulses to create many holes at once according to the
    supplied lists and shapes

    Parameters
    ----------
    freqs : list of floats
        Should be a list frequncies that represent the center frequency of all
        holes in the spectrum.
        i.e. [150e6, 160e6] is a pair of holes 150 MHz, 160 MHz
    widths : list of floats
        Should be a list spectral widths that represent the width in frequency
        of each hole in the spectrum.  
        i.e. [0.5e6, 0.5e6] make the burn pulses 0.5MHz in width for supplied frequencies.
    shape : int
        specifies the shape parameter of the SecHype Pulses. Changes TanHype Slope
    times : Array of np.float32
        Arracy of times that define the waveform. 

    Returns
    -------
    waveform : Array of np.float64
        optimized waveform for different frequencies as in other functions above

    """
    waveform=np.zeros([len(times)])
    for i in range(len(freqs)):
        freqArray= tanHypeSawtooth(shape, widths[i], freqs[i], len(times),1)
        wfmDataI = np.sin(2*np.pi*np.multiply(freqArray,times))
        wfmDataI = OptimiseWaveform(wfmDataI,freqArray,7)
        waveform=np.add(waveform,wfmDataI)
    waveform=np.multiply(waveform,1/len(freqs))
       
    return waveform

    
def ViewPlot(FileName):
    
    #F=open(FileName,'r')
    with open(FileName,newline='') as file:
        readarray = csv.reader(file,delimiter=';')
        Time=[]
        Data=[]
        for i in range(5):
            next(readarray)
            for row in readarray:
                Time.append(float(row[0]))
                Data.append(float(row[1]))
    plt.plot(Time, Data)
    plt.show()

'''
# Must have 2 of these 3 to determine all
SR=25e9  # in Samples/Sec
D=2.00128e-05 # Seconds
P=500320    # number of points for this duration at this sampling rate

# All waveforms start with a Time Array. Sample Rate will be given by the AWG
# User will supply either the number of points to have, or the needed duration
# Min Number of points should be based on device limitations, and needed 
# Duration should be based on the Fourier transform of the data in Freq Space.
 
t1=Times(SR,duration=D)
t2=Times(SR,recordLength=P)
print((t1 == t2).all())
'''
'''
F=open("Read_2GHz_20us.txt",'r')
with open('Read_2GHz_20us.txt',newline='') as file:
    readarray = csv.reader(file,delimiter=',')
    analog=[]
    mk1=[]
    mk2=[]
    for row in readarray:
        analog.append(float(row[0]))
        mk1.append(int(row[1]))
        mk2.append(int(row[2]))



freq=np.linspace(0,2e9,len(t1),dtype=np.float32)
wfmData = signal.sawtooth(2*np.pi*np.multiply(freq,t1))
wfmData1 = NormWaveform(wfmData,freq,7)


#normfreqs=np.arange(100,2100,100)
#normfreqsfine=np.linspace(0,2000,len(freq))
#normvals=np.multiply([1.2, 1.25, 1.36, 1.38, 1.42, 1.42, 1.55, 1.39, 1.39, 1.55, 1.73, 1.74, 2.18, 2.18, 2.2, 2.3, 2.3, 2.5, 2.4, 2.5],0.5)
#f = interpolate.interp1d(normfreqs,normvals,fill_value='extrapolate')
#normvalsfine=f(normfreqsfine)
#wfmData = normvalsfine*signal.sawtooth(2*np.pi*np.multiply(freq,t1))
plt.plot(t1, analog)
#plt.plot(t1, wfmData)
plt.plot(t1, wfmData1)
plt.show()
'''

# For a Simple Sine wave Numpy has what we need. Just specify a frequency and
# you can quickly define the waveform data and markers
'''
#----------------------------------------------------------------------------
freq=100e6 # 100MHz 
wfmData = np.sin(2*np.pi*freq*t1)
# Markers
MData1= np.ones(len(wfmData))
MData2= np.ones(len(wfmData))
MData1[0:9]=0
MData2[0:9]=0
plt.plot(t1[1:1000], wfmData[1:1000])
#plt.show()
#----------------------------------------------------------------------------
'''

# For a sawtooth wave Scipy has what we need. Just specify a frequency and
# you can quickly define the waveform data and markers

#----------------------------------------------------------------------------
#freq=100e6 # 100MHz 
#wfmData = signal.sawtooth(2*np.pi*freq*t1)
#plt.plot(t1[0:1000], wfmData[0:1000])
#plt.show()
#----------------------------------------------------------------------------



#Now We can add an envelope or chirp fuction as well. Just specify what it should be

#freq=np.linspace(0,100e6,len(t1),dtype=np.float32)
#env= np.ones(len(freq))
#env[0:10000]=2
#env[10000:20000]=0.5
#A1=np.multiply(freq,env)
#wfmData = signal.sawtooth(2*np.pi*np.multiply(freq,t1))
#plt.plot(t1[0:50000], wfmData[0:50000])
#plt.show()



#Make a hyperbolic tangent modulated chirp function in frequency
'''
#freq=np.linspace(0,2e6,len(t1),dtype=np.float32)
y1=tanHypeSawtooth(10,1e6,1e6,len(t1),1)
y2=tanHypeSawtooth(10,1e6,1e6,len(t1),0)
#wfmData1 = signal.sawtooth(2*np.pi*np.multiply(freq,t1))
wfmData1 = signal.sawtooth(2*np.pi*np.multiply(y1,t1))
wfmData2 = signal.sawtooth(2*np.pi*np.multiply(y2,t1))


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(t1, wfmData1, 'r-')
ax2.plot(t1, y1, 'b-')
ax1.plot(t1, wfmData2)
ax2.plot(t1, y2)
plt.show()
'''

# Make a hyperbolic secant pulse for the arbitrary function generator
#z=SecHypePulse(7,2000,600,400,1000)
#plt.plot(z)








