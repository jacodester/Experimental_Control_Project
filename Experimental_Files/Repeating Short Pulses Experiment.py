# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 13:25:10 2021

@author: LocalAdmin
"""
# Section for import statements from other modules and classes  
#-----------------------------------------------------------------------------
import pyvisa
import time
import sys
#from matplotlib import pyplot as plt
from scipy import signal 
import numpy as np


# Works to import the single module I want to have
#sys.path.insert(0,"C:/Users/LocalAdmin/.spyder-py3/Device_Files")
#import ScopeClassObjects as SO

# Works to import the path that I want to have my object from. 
sys.path.insert(0,"C:/Users/LocalAdmin/.spyder-py3/")
import Device_Files.ScopeClassObjects as SO  #import the device object classes
import Device_Files.TekClassObjects as TO
import Device_Files.PulseblasterClassObjects as pb
import Device_Files.WaveformFunctionsUse as wf # import useful waveform functions
from Device_Files.WavemeterClassObject import *
#-----------------------------------------------------------------------------


#Section establishing connection to a series of device objects
#-----------------------------------------------------------------------------
rm=pyvisa.ResourceManager() # Open a resource manager

#Make a digital AFG object from the tektronix object class
AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
print(AFG1.query('*IDN?')) # Print ddentification string

#Make a digital Scope object from the Lecroy object class
Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
print(Scope.query("*IDN?"))

#Make a digital AWG object from the tektronix object class
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print(AWG1.query('*IDN?'))

wavemeter = pyBristolSCPI('1.1.1.6')


#-----------------------------------------------------------------------------


#Make sure that the AWG has all the desired waveforms in a sequence
#-----------------------------------------------------------------------------
SR = 25e9 # AWG sampling rate

#Make and Upload first Waveform
D1 = 0.0001 # specified waveform duration
P1 = wf.Points(SR,D1)
t1=wf.Times(SR,duration=D1)
WFName1='JHD_DC_100us'
wfmData1 = 0*np.ones(len(t1))
MData1= 0*np.ones(len(wfmData1))
MData2= 0*np.ones(len(wfmData1))
MData1[0:300000]=1
MData2[0:300000]=1
start=time.time()
print('Keep Calm. I am uploading your waveform')
AWG1.write_waveform(WFName1,wfmData1,MData1,MData2)
print(time.time()-start)
print('Waveform HOT  from the oven...MMMM')
AWG1.save_Func(WFName1,'WAV')



AWG1.ChannelFunc(WFName1, 1, 'WAV')
AWG1.SetON_OFF(1,'ON')
AWG1.SetState('RUN')
#-----------------------------------------------------------------------------


#Make sure the AFG has the right settings for Hole Burning
#-----------------------------------------------------------------------------
AFG1.SetBurst("1","OFF")
AFG1.SetFunction("1","ARB")
AFG1.SetVoltage("1","HIGH",4.9)
AFG1.SetVoltage("1","LOW",4.8)
AFG1.SetState("1","ON")
#-----------------------------------------------------------------------------



#Make Scope Capture the correct window of signals
#-----------------------------------------------------------------------------
Scope.SetTrig('C3','NORM',0,0.0065)
#Scope.SetOffset('C2',-0.153,"VOLTS")
Scope.SetVDiv('C2',0.010)
Scope.SetVDiv('C3',0.010)
Scope.SetSampleRate('C1',1000)
#Scope.SetTDiv('C2',50e-6)
Scope.SetNotes("Short Pulses to measure Inhomogeneous broadening at 750mK 1% Tm:YGG")
Info2=Scope.ReadInfo('C2')
Info3=Scope.ReadInfo('C3')
#-----------------------------------------------------------------------------





Scope. ClearSweeps()
wl = wavemeter.readWL()
freq = wavemeter.readFREQ()
print(wl)
print(freq)
print("Continuing will stop program execution\n");
input("Please press a key to continue.")

#time.sleep(10)
times_out2, horiz_unit_out2, voltages_out2, vertical_unit_out2 = Scope.ReadWaveform('C2',Info2)
times_out3, horiz_unit_out3, voltages_out3, vertical_unit_out3 = Scope.ReadWaveform('C3',Info3)
Scope.WriteData('C2 & C3',"IN_OUT_At_{}nm_{}THz.txt".format(wl,freq), times_out2, horiz_unit_out2,voltages_out2, vertical_unit_out2, voltages_out3, vertical_unit_out3)


AWG1.SetState('STOP')
AWG1.SetON_OFF(1,'OFF')



# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
del wavemeter
AFG1.close()
Scope.close()
AWG1.close()
rm.close()
#-----------------------------------------------------------------------------