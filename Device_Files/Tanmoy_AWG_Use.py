# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyvisa
import time
import TekClassObjects as TO
import numpy as np
from scipy import signal 
from matplotlib import pyplot as plt
import WaveformFunctionsUse as wf 
import math



#Example code for accessing the AFG functions

rm=pyvisa.ResourceManager()

print(rm.list_resources())

Thingy1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
Thingy1.query('*IDN?')


# Example code for turning on a channel and running the active wavefrom or sequence
'''
Thingy1.SetON_OFF(1,'ON')
Thingy1.SetState('RUN')
time.sleep(2)
Thingy1.SetState('STOP')
Thingy1.SetON_OFF(1,'OFF')
'''



# Change these based on your signal requirements
SR = 25e9
D = 0.000001
P = wf.Points(SR,D)
t1=wf.Times(SR,duration=D)


#freq=np.linspace(0,100e6,len(t1),dtype=np.float32)
#wfmData = signal.sawtooth(2*np.pi*np.multiply(freq,t1))
#startFreq=380e6
#sweepWidth=40e6
#freq1=wf.chirpedSawtooth(startFreq,sweepWidth,len(t1))
freq1=12e6
#a=math.exp(-(t1-50e-9))
#b=math.exp(-(t1-250e-9))
#wfmData1=a+b


wfmData1 = signal.sawtooth(2*np.pi*np.multiply(freq1,t1))




plt.plot(t1, wfmData1)
plt.show()
MData1= np.ones(len(wfmData1))
MData2= np.ones(len(wfmData1))
MData1[0:9]=0
MData2[0:9]=0

'''
# Example Code for writing a custom waveform to the machine and saving it
WFName='Tanmoys_Timebins_200ns'
start=time.time()
print('Start Tranfser')
Thingy1.write_waveform(WFName,wfmData1,MData1,MData2)
print(time.time()-start)
Thingy1.ChannelFunc(WFName,1,'WAV')
print('Done')
#Thingy1.save_Func(WFName,'WAV')
'''


Thingy1.close()
rm.close()


















