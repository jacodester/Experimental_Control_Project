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

#Make a digital Pulseblaster object from the pulse blaster class definition
PulseBlaster1=pb.PulseBlaster()
PulseBlaster1.ResetProg()
#-----------------------------------------------------------------------------


#Make sure that the AWG has all the desired waveforms in a sequence
#-----------------------------------------------------------------------------
SR = 25e9 # AWG sampling rate

#Make and Upload first Waveform
D1 = 0.0005 # specified waveform duration
P1 = wf.Points(SR,D1)
t1=wf.Times(SR,duration=D1)
WFName1='JHD_Read_380MHz_420MHz_500us'
startFreq1=380e6
sweepWidth1=40e6
freq1=wf.chirpedSawtooth(startFreq1,sweepWidth1,len(t1))
wfmData1 = signal.sawtooth(2*np.pi*np.multiply(freq1,t1))
wfmData1 = wf.OptimiseWaveform(wfmData1,freq1,7)
MData1= np.ones(len(wfmData1))
MData2= np.ones(len(wfmData1))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
print('Keep Calm. I am uploading your waveform.')
AWG1.write_waveform(WFName1,wfmData1,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
AWG1.save_Func(WFName1,'WAV')

#Make and Upload Second Waveform
D2 = 0.00005 # specified waveform duration
P2 = wf.Points(SR,D2)
t2=wf.Times(SR,duration=D2)
WFName2='JHD_Hole_410MHz_100us'
freq2= 410e6
wfmData2 = signal.sawtooth(2*np.pi*np.multiply(freq2,t2))
wfmData2 = wf.OptimiseWaveform(wfmData2,freq2,7)
MData1= np.ones(len(wfmData2))
MData2= np.ones(len(wfmData2))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
print('Keep Calm. I am uploading your waveform.')
AWG1.write_waveform(WFName2,wfmData2,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
AWG1.save_Func(WFName2,'WAV')

#Make and Upload Second Waveform
D3 = 0.00005 # specified waveform duration
P3 = wf.Points(SR,D3)
t3=wf.Times(SR,duration=D3)
WFName3='JHD_Hole_390MHz_100us'
freq3= 390e6
wfmData3 = signal.sawtooth(2*np.pi*np.multiply(freq3,t3))
wfmData3 = wf.OptimiseWaveform(wfmData3,freq3,7)
MData1= np.ones(len(wfmData3))
MData2= np.ones(len(wfmData3))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
print('Keep Calm. I am uploading your waveform.')
AWG1.write_waveform(WFName3,wfmData3,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
AWG1.save_Func(WFName2,'WAV')

D4=D3+D2
wfmData4=np.concatenate([wfmData2,wfmData3])
MData1= np.ones(len(wfmData4))
MData2= np.ones(len(wfmData4))
MData1[0:9]=0
MData2[0:9]=0
WFName4='JHD_Hole_390MHz_and_410MHz_100us'
start=time.time()
print('Keep Calm. I am uploading your waveform.')
AWG1.write_waveform(WFName4,wfmData4,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
AWG1.save_Func(WFName2,'WAV')


# Make Sequence of the uploaded waveforms
SEQList=[[(WFName4,''), 1, 'BTR', 999, 0],
         [(WFName1,''), 2, 'BTR', 0, 1]
         ]
AWG1.write_sequence('Test1',SEQList)
AWG1.ChannelFunc('Test1', 1, 'SEQ')
AWG1.SetON_OFF(1,'ON')
AWG1.SetState('RUN')
#-----------------------------------------------------------------------------


#Make sure the AFG has the right settings for Hole Burning
#-----------------------------------------------------------------------------
AFG1.SetFunction("1","PULS")
AFG1.SetBurst("1","ON")
AFG1.SetVoltage("1","HIGH",5)
AFG1.SetVoltage("1","LOW",0.7)
AFG1.SetPer("1",(D4*1000)*1000+5)
AFG1.SetWidth("1",(D4*1000)*1000)
AFG1.SetNumCyc("1",1)
AFG1.SetState("1","ON")
#-----------------------------------------------------------------------------



#Make Scope Capture the correct window of signals
#-----------------------------------------------------------------------------
Scope.SetTrig('C1','NORM',-D1/2,0.6)
Scope.SetOffset('C2',-1.2,"VOLTS")
Scope.SetVDiv('C2',0.5)
Scope.SetSampleRate('C1',100000)
Scope.SetTDiv('C2',50e-6)
Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C2')
#-----------------------------------------------------------------------------

#Make the pulseblaster program as we so desire. 
#-----------------------------------------------------------------------------
PulseBlaster1.ViewProg()
PulseBlaster1.WriteCommand([0,1], 0, 1)
PulseBlaster1.WriteCommand([], 0, D4*1000*1e6) 
PulseBlaster1.WriteCommand([], 0, 15000)
PulseBlaster1.WriteCommand([0,2], 0, D1*1e6) #
PulseBlaster1.WriteCommand([], 6, 5000)
PulseBlaster1.WriteProg()

#-----------------------------------------------------------------------------



PulseBlaster1.Start()
Scope. ClearSweeps()
print("Continuing will stop program execution\n");
input("Please press a key to continue.")
#time.sleep(10)
PulseBlaster1.Stop()
Scope.ReadWaveform('C2',Info1)
Scope.WriteData('C2',"TrialFull2.txt")





# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
PulseBlaster1.Close()
AFG1.close()
Scope.close()
AWG1.close()
rm.close()
#-----------------------------------------------------------------------------