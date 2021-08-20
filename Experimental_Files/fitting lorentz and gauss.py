# -*- coding: utf-8 -*-
"""
Created on Mon May 10 13:48:43 2021

@author: LocalAdmin
"""
"""
Created on Tue Apr  6 17:35:44 2021

@author: LocalAdmin
"""
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import csv
import Device_Files.AnalysisFunctionsUse as af # import useful waveform functions
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

FileName="1000us_burn_hole_2cycle.txt"
#F=open(FileName,'r')
with open(FileName,newline='') as file:
    readarray = csv.reader(file,delimiter=';')
    Time=[]
    Data1=[]
    Data2=[]
    for i in range(5):
        next(readarray)
    for row in readarray:
        Time.append(float(row[0]))
        Data1.append(float(row[1]))
        Data2.append(float(row[2]))
indices1 = [idx1 for idx1,val1 in enumerate(Time) if (val1 > 149.4 and val1 < 150.6)]
start_index = indices1[0]
stop_index = indices1[-1] 

Time1 = Time[start_index:stop_index]
Data3 = Data1[start_index:stop_index]
Data3=af.SavgolSmooth(Data3,71,3)   
plt.plot(Time , Data1)        
plt.plot(Time1 , (Data3))
#plt.plot(Time1 , smooth(Data3,59))
#plt.plot(Time, Data2)
plt.show()
#%%
def lorentzian( x, x0, a, gam , o):
    return a * gam**2 / ( gam**2 + ( x - x0 )**2) + o

def gaussian(x, a, b, c):
    return a*np.exp(-np.power(x - b, 2)/(2*np.power(c, 2))) + 0.45

# Generate dummy dataset
x_dummy = Time1
#x_dummy = np.linspace(start=-10, stop=10, num=100)
#y_dummy = gaussian(x_dummy, 8, -1, 3)
y_dummy = Data3
# Add noise from a Gaussian distribution
# noise = 0.5*np.random.normal(size=y_dummy.size)
# y_dummy = y_dummy + noise


# Fit the dummy Gaussian data

pars, cov = curve_fit(f=lorentzian, xdata=x_dummy, ydata=y_dummy, p0=[150.90, 0.6, 0.1, 0.45], bounds=(-np.inf, np.inf))
# Get the standard deviations of the parameters (square roots of the # diagonal of the covariance)
stdevs = np.sqrt(np.diag(cov))


# Plot the fit data as an overlay on the scatter data
plt.plot(x_dummy, y_dummy, label='Data')
plt.plot(x_dummy, lorentzian(x_dummy, *pars), linestyle='--', linewidth=2, color='red', label="fitted width: "+str(pars[3]) + " MHz")
plt.legend()
plt.show()
#%%
def lorentzian( x, amp1, cen1, wid1, amp2,cen2,wid2, amp3,cen3,wid3):
    return (amp1*wid1**2/((x-cen1)**2+wid1**2)) + (amp2*wid2**2/((x-cen2)**2+wid2**2))+ (amp3*wid3**2/((x-cen3)**2+wid3**2))

x_dummy = Time1
y_dummy = Data3

amp1_0= 0.0105
cen1_0= 150
wid1_0= 0.5

amp2_0= 0.078
cen2_0=149.65
wid2_0= 1

amp3_0= 0.078
cen3_0=150.4
wid3_0= 1

# amp1_0= 0.12
# cen1_0= 150
# wid1_0= 0.5

# amp2_0= 0.085
# cen2_0=149.7
# wid2_0= 1

# amp3_0= 0.085
# cen3_0=150.4
# wid3_0= 1

popt_2gauss, pcov_2gauss = curve_fit(lorentzian, x_dummy, y_dummy, p0=[amp1_0, cen1_0, wid1_0, amp2_0, cen2_0, wid2_0, amp3_0, cen3_0, wid3_0])
perr_2gauss = np.sqrt(np.diag(pcov_2gauss))

linewidth = float("{:.2f}".format(popt_2gauss[2])) *1000

plt.plot(x_dummy, y_dummy, label='Data')
plt.plot(x_dummy, lorentzian(x_dummy, *popt_2gauss), linestyle='--', linewidth=2, color='red', label="fitted width: "+str(linewidth) + " KHz")
plt.legend()
plt.show()
