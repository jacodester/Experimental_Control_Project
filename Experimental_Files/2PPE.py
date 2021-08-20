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
from matplotlib import pyplot as plt


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

#Make and Upload first pi/2 pulse

D1 = 0.15*1e-6  # specified waveform duration in sec
P1 = wf.Points(SR,D1)
t1=wf.Times(SR,duration=D1)
WFName1='ARD_Pulse_1us'
wfmData1 = np.zeros(len(t1))
MData1= np.ones(len(wfmData1))
MData2= np.ones(len(wfmData1))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
print('Keep Calm. I am uploading your waveform Master.')
AWG1.write_waveform(WFName1,wfmData1,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
AWG1.save_Func(WFName1,'WAV')

#Make and Upload second pi pulse

D2 = 0.15*1e-6 # specified waveform duration in sec
P2 = wf.Points(SR,D2)
t2=wf.Times(SR,duration=D2)
WFName2='ARD_Pulse_2us'
wfmData2 = np.zeros(len(t2))
MData11= np.ones(len(wfmData2))
MData22= np.ones(len(wfmData2))
MData11[0:9]=0
MData22[0:9]=0
start=time.time()
print('Keep Calm. I am uploading your waveform Master.')
AWG1.write_waveform(WFName2,wfmData2,MData11,MData22)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
AWG1.save_Func(WFName2,'WAV')



# Make Sequence of the uploaded waveforms
SEQList=[[(WFName1,''), 1, 'BTR', 1, 0],
         [(WFName2,''), 2, 'BTR', 1, 1]
         ]
AWG1.write_sequence('2PPE_ARD',SEQList)
AWG1.ChannelFunc('2PPE_ARD', 1, 'SEQ')
AWG1.SetON_OFF(1,'ON')
AWG1.SetState('RUN')
#-----------------------------------------------------------------------------

waiting_time = 0.5; #in us

#Make sure the AFG has the right settings for 2PPE
#-----------------------------------------------------------------------------
AFG1.SetFunction("1","PULS")
AFG1.SetBurst("1","ON")
AFG1.SetPolarity("1","NORM")
AFG1.SetVoltage("1","HIGH",5)
AFG1.SetVoltage("1","LOW",4.9)
AFG1.SetPer("1",(D1*1000+5))  #in ms
#AFG1.SetWidth("1",(D1*1000)*1000)
AFG1.SetNumCyc("1",1)
AFG1.SetState("1","ON")
#-----------------------------------------------------------------------------



#Make Scope Capture the correct window of signals
#-----------------------------------------------------------------------------
Scope.SetTrig('C1','NORM',-waiting_time*1e-6,0.35) #PB trigger scale in scope
Scope.SetOffset('C3',-0.002,"VOLTS") # scope offset
Scope.SetVDiv('C3',0.002)   #in V/div
Scope.SetSampleRate('C1',200000)
#Scope.SetTDiv('C2',D2) # us*1e-6/div
#Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C3')
#-----------------------------------------------------------------------------

#Make the pulseblaster program as we so desire. 
#-----------------------------------------------------------------------------
PulseBlaster1.ViewProg()
PulseBlaster1.WriteCommand([0], 0, 0.1)  # trigger the superfast for the first pi/2 pulse 
PulseBlaster1.WriteCommand([], 0, D1*1e6)    # for the first pi/2
PulseBlaster1.WriteCommand([], 0, waiting_time)   # Waiting time t12 in us
PulseBlaster1.WriteCommand([1], 0, 0.1)   # Trig FG to high
PulseBlaster1.WriteCommand([0,2], 0, D2*1e6)  # second pi
PulseBlaster1.WriteCommand([], 6, 5000)  # recycling in us
PulseBlaster1.WriteProg()

#-----------------------------------------------------------------------------



PulseBlaster1.Start()
Scope. ClearSweeps()
print("Continuing will stop program execution\n");
input("Please press a key to continue.")
#time.sleep(10)
PulseBlaster1.Stop()

# Scope.ReadWaveform('C2',Info1)
#Scope.WriteData('C2',"5V4V.txt")

times_out, horiz_unit_out, voltages_out, vertical_unit_out=Scope.ReadWaveform('C3',Info1)
Scope.WriteData('C3',"F3_4.5V_4V.txt")

voltages_out=signal.savgol_filter(voltages_out,9,3)
newmax=max(voltages_out[int(6*len(voltages_out)/10):-1])



# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
PulseBlaster1.Close()
AFG1.close()
Scope.close()
AWG1.close()
rm.close()
#-----------------------------------------------------------------------------