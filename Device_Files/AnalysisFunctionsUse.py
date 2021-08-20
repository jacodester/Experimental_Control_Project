# -*- coding: utf-8 -*-
"""
Created on Thu May 27 10:19:22 2021

@author: LocalAdmin
"""


import time
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal,interpolate 
import csv


def JakeTestFunction():
    print('hi')
    return

def SavgolSmooth(data, ptwidth, power):
    """
    Smooths Noisy Data from an oscilloscope trace using the savgol filter
    function of scipy

    Parameters
    ----------
    data : numpy array of ints or floats or some numeric
        data to be smoothed
    ptwidth : int
        an odd number of points over which to smooth. this will depend on the 
        length in points that compromises the data
    power : int
        degree of poly nomial to smooth with

    Returns
    -------
    same data type as data parameter
        the smoothed data

    """
    return signal.savgol_filter(data,ptwidth,power)

def MakeBaseFig(fignum, x_data, y_data, x_label=None, y_label=None,title=None,Filename=None,close=0):
    """
    Single line function to generate a figure with the input data and naming

    Parameters
    ----------
    fignum : int
        number the figure if generating multiple ones to have separate plots
        i.e. 1,2,3...
    x_data : numpy array or list
        the x data to be plotted, must match in length with the y data
    y_data : numoy array or list
        the y data to be plotted, must match in length with the x data
    x_label : str
        text for x axis label
    y_label : str
        text for y axis label
    Filename : str
        text of the filename, possibly including the file extension for a given 
        location
    close : bool
        Either 0 or 1, if you want to leave the fig open for another function use 1
        to close the fig immediately use 0.

    Returns
    -------
    None.

    """
    plt.figure(fignum)
    plt.plot(x_data,y_data)
    if (not (x_label is None)):
        plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
    if (Filename is None):
        return
    plt.savefig(Filename)
    if (not close):
        plt.close()
    return
def CalcODRegion(x_data, y_data, num_points, startFreq, endFreq):
    """
    Calculate OD of a transmitted pulse given the frequency and voltage data
    from an oscilloscope trace

    Parameters
    ----------
    x_data : array
        the x data in frequency from a scope trace
    y_data : array
        the y data in voltage from a scope trace
    num_points : int
        number of points on the end of the trailing pulse to get perfect
        transmission
    startFreq : int 
        a start frequency that must appear in the trace of frequencies spanned
        by the x data
    endFreq : int
        and end frequency for which to stop calculating the OD. If the number
        is greater than the total swept frequncy range, then the whole trace
        will be converted.

    Returns
    -------
    x_ODRegion : array
        an array of frequency data that spans the defined frequency region
        in between startFreq and endFreq. The points will match with the OD Y
        data points from the other return
    OD : array 
        an array of OD data that matches the returned x data 

    """
    
    
    x_transmitted = x_data[-num_points:-1]
    y_transmitted = y_data[-num_points:-1]

    #plt.plot(Freq_noise, Data2_noise)

    indices = [idx for idx,val in enumerate(x_data) if (val > (startFreq +.02) and val < endFreq)]
    x_ODRegion = x_data[indices[0]:indices[-1]]
    y_ODRegion = y_data[indices[0]:indices[-1]]

    OD = -np.log(np.true_divide(y_ODRegion, np.mean(y_transmitted)))
    
    return x_ODRegion, OD
    

def CalcHoleParam(x_data,y_data,startFreq,endFreq,ODStartFreq,ODEndFreq):
    """
    Calculate the hole depth in a defined region of Optical depth points

    Parameters
    ----------
    x_data : array
        Frequency array gathered from an oscilloscope trace. 
    y_data : array
        Optical depth array gathered from an oscilloscope trace.
    startFreq : float
        starting frequency of the range to look for a hole
    endFreq : float
        ending frequency of the range to look for a hole
    ODStartFreq : float
        starting frequency of the background OD region
    ODEndFreq : float
        ending frequency of the background OD region

    Returns
    -------
    HoleDepth : float
        rough depth of the hole. Essentially the minima in the total region
        subtracted from the average OD in the other defined region

    """
    
    
    indices1 = [idx1 for idx1,val1 in enumerate(x_data) if (val1 > startFreq and val1 < endFreq)]
    indices2 = [idx2 for idx2,val2 in enumerate(x_data) if (val2 > ODStartFreq and val2 < ODEndFreq)]
    HoleMin = np.amin(y_data[indices1[0]:indices1[-1]])
    ODMean = np.mean(y_data[indices2[0]:indices2[-1]])
    HoleDepth = ODMean - HoleMin
    FWHMOD=HoleMin+(HoleDepth/2)
    IndexHoleMin=np.where(y_data[indices1[0]:indices1[-1]] == HoleMin)    
    IndicesFWHM=np.where(y_data[indices1[0]:indices1[-1]] < FWHMOD)
    #Width Method 1
    startInd=IndicesFWHM[0][0]
    endInd=IndicesFWHM[0][-1]
    HoleWidth1=x_data[endInd]-x_data[startInd]
    #Width Method 2
    #diffs=np.diff(IndicesFWHM[0])
    #lowInd=int(np.where(diffs[0:IndexHoleMin[0][0]] > 1)[0][-1]+IndicesFWHM[0][0])
    #highInd=IndexHoleMin[0][0]+(IndexHoleMin[0][0]-lowInd)
    #HoleWidth2=x_data[highInd]-x_data[lowInd]

    #MakeBaseFig(3, x_data[lowInd:highInd], y_data[lowInd:highInd])
    
    return HoleDepth, HoleWidth1, IndicesFWHM, IndexHoleMin #HoleWidth2,

    










