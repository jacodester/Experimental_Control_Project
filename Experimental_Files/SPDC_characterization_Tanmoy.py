# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 13:55:53 2021

@author: LocalAdmin
"""
# Section for import statements from other modules and classes  
#-----------------------------------------------------------------------------
# Section for import statements from other modules and classes  
#-----------------------------------------------------------------------------
import pyvisa
import time
import sys
#from matplotlib import pyplot as plt
from scipy import signal 
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm



# Works to import the single module I want to have
#sys.path.insert(0,"C:/Users/LocalAdmin/.spyder-py3/Device_Files")
#import ScopeClassObjects as SO

# Works to import the path that I want to have my object from. 
sys.path.insert(0,"C:/Users/LocalAdmin/.spyder-py3/")
import Device_Files.ScopeClassObjects as SO  #import the device object classes
import Device_Files.TekClassObjects as TO
import Device_Files.PulseblasterClassObjects as pb
import Device_Files.WaveformFunctionsUse as wf # import useful waveform functions
import Device_Files.AnalysisFunctionsUse as af # import useful waveform functions
#from Device_Files.WavemeterClassObject import *
#-----------------------------------------------------------------------------


#Section establishing connection to a series of device objects
#-----------------------------------------------------------------------------
rm=pyvisa.ResourceManager() # Open a resource manager


#Make a digital AFG object from the tektronix object class
AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
print(AFG1.query('*IDN?')) # Print ddentification string
AFG1.close()

#Make a digital Scope object from the Lecroy object class
Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
print(Scope.query("*IDN?"))
Scope.timeout=2000000
Scope.close()

#Make a digital AWG object from the tektronix object class
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print(AWG1.query('*IDN?'))
AWG1.close()

#Make a digital Pulseblaster object from the pulse blaster class definition
PulseBlaster1=pb.PulseBlaster()
PulseBlaster1.ResetProg()
#-----------------------------------------------------------------------------

#wavemeter = pyBristolSCPI('1.1.1.6')

#Make sure that the AWG has all the desired waveforms in a sequence
#-----------------------------------------------------------------------------
SR = 25e9 # AWG sampling rate

#Make and Upload first Waveform: READ
D1 = 2000*1e-6 # specified waveform duration in sec
P1 = wf.Points(SR,D1)
t1=wf.Times(SR,duration=D1)
WFName1='JHD_Read_149MHz_151MHz_2ms'
startFreq1=149e6
sweepWidth1=2e6
freq1=wf.chirpedSawtooth(startFreq1,sweepWidth1,len(t1))
wfmData1 = signal.sawtooth(2*np.pi*np.multiply(freq1,t1))
wfmData1 = wf.OptimiseWaveform(wfmData1,freq1,7)
MData1= np.ones(len(wfmData1))
MData2= np.ones(len(wfmData1))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform')
#AWG1.write_waveform(WFName1,wfmData1,MData1,MData2)
print(time.time()-start)
print('Waveform HOT  from the oven...MMMM')
#AWG1.save_Func(WFName1,'WAV')
AWG1.close()

#Make and Upload Second Waveform: BURN/TRENCH
D2 = 100*1e-6 # specified waveform duration in sec
P2 = wf.Points(SR,D2)
t2=wf.Times(SR,duration=D2)
WFName2='JHD_Hole_150MHz_100us'
freq2= 150e6
wfmData2 = signal.sawtooth(2*np.pi*np.multiply(freq2,t2))
wfmData2 = wf.OptimiseWaveform(wfmData2,freq2,7)
MData1= np.ones(len(wfmData2))
MData2= np.ones(len(wfmData2))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform.')
#AWG1.write_waveform(WFName2,wfmData2,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName2,'WAV')
AWG1.close()

#Make and Upload Second Waveform: BURN with sechyp
# D4 = 100*1e-6 # specified waveform duration in sec
# P4 = wf.Points(SR,D2)
# t4=wf.Times(SR,duration=D4)
# WFName4='JHD_Hole_SecHype_100us'
# freq4= wf.tanHypeSawtooth(2, 40e6, 150e6, len(t4),1)
# wfmData4 = signal.sawtooth(2*np.pi*np.multiply(freq4,t4))
# wfmData4 = wf.OptimiseWaveform(wfmData4,freq4,7)
# MData1= np.ones(len(wfmData4))
# MData2= np.ones(len(wfmData4))
# MData1[0:9]=0
# MData2[0:9]=0
# start=time.time()
# AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
# print('Keep Calm. I am uploading your waveform.')
# AWG1.write_waveform(WFName4,wfmData4,MData1,MData2)
# print(time.time()-start)
# print('Waveform HOT from the oven...MMMM')
# AWG1.save_Func(WFName2,'WAV')
# AWG1.close()

# specified the DC delay
D3 =1000*1e-6 # specified waveform duration in sec 
P3 = wf.Points(SR,D3)
t3=wf.Times(SR,duration=D3)
WFName3='JHD_Delay_1ms'
wfmData3 = np.ones(len(t3))
MData1= np.ones(len(wfmData3))
MData2= np.ones(len(wfmData3))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform.')
#AWG1.write_waveform(WFName3,wfmData3,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName3,'WAV')
AWG1.close()


# Make Sequence of the uploaded waveforms
SEQList=[[(WFName2,''), 1, 'BTR', 1000, 1]
         ]
# SEQList=[[(WFName2,''), 1, 'BTR', 1000, 0],
#          [(WFName1,''), 2, 'BTR', 0, 1]
#          ]
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
AWG1.write_sequence('Test1',SEQList)
AWG1.ChannelFunc('Test1', 1, 'SEQ')
AWG1.SetON_OFF(1,'ON')
AWG1.SetState('RUN')
AWG1.close()
#-----------------------------------------------------------------------------


#Make sure the AFG has the right settings for Hole Burning
#-----------------------------------------------------------------------------
waiting_time = 50000 #in us
BurnDur=0.001 #Seconds (Light ON)
reps=int(BurnDur/D2)
experimental_time = 15*1e6 # 15[sec]*1e6
#-----------------------------------------------------------------------------
#Make sure the AFG has the right settings for Hole Burning
#-----------------------------------------------------------------------------
AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
AFG1.SetFunction("1","ARB")
AFG1.SetFunction("1","USER2")
AFG1.SetBurst("1","OFF")
AFG1.SetVoltage("1","HIGH",5) #V
AFG1.SetVoltage("1","LOW",5)
AFG1.SetPer("1",(D2*reps)*1000+((D2*reps)*1000)*0.01)
AFG1.SetWidth("1",(D2*reps)*1000)
AFG1.SetNumCyc("1",1)
AFG1.SetState("1","ON")
AFG1.close()

#-----------------------------------------------------------------------------
#For SecHyp burning AFG has the right settings for Hole Burning
#-----------------------------------------------------------------------------
# AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
# z=wf.SecHypePulse(value,2000,600,400,(100, 10))
# #plt.plot(z)
# AFG1.set_custom_waveform(z,memory_num=4,normalise=True, print_progress=False)
# AFG1.SetFunction("1","ARB")
# AFG1.SetFunction("1","USER4")
# AFG1.SetBurst("1","ON")
# AFG1.SetVoltage("1","HIGH",high) #V
# AFG1.SetVoltage("1","LOW",0.1)
# AFG1.SetPer("1",(D2)*1000)#+ 0.01*(D2*reps)*1000)
# AFG1.SetNumCyc("1",1)
# AFG1.SetState("1","ON")
# AFG1.close()

#-----------------------------------------------------------------------------
#Make Scope Capture the correct window of signals
Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
Scope.SetTrig('C1','SINGLE',-D1/2,0.35)
Scope.SetOffset('C2',-0.100,"VOLTS") #35mV/div
#Scope.SetOffset('C2',-0.271,"VOLTS") #100mV/div
#Scope.SetOffset('C2',-0.50,"VOLTS") #200mV/div
Scope.SetVDiv('C2',0.040)   #25mV/div
Scope.SetSampleRate('C1',100000)
Scope.SetTDiv('C2',500e-6)
Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C2')
Info2=Scope.ReadInfo('C3')
Scope.close()
#-----------------------------------------------------------------------------



#Make Scope Capture the correct window of signals
#-----------------------------------------------------------------------------
Scope.SetTrig('C1','NORM',-D1/2,0.35)
Scope.SetOffset('C2',-0.10,"VOLTS")
Scope.SetVDiv('C2',0.050)
Scope.SetSampleRate('C1',100000)
Scope.SetTDiv('C2',50e-6)
Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C2')
Info2=Scope.ReadInfo('C3')
#-----------------------------------------------------------------------------

#Make the pulseblaster program as we so desire. 
#-----------------------------------------------------------------------------PulseBlaster1.ViewProg()
PulseBlaster1.ResetProg()
PulseBlaster1.WriteCommand([0,1], 0, 1) #TRIG SF and FG
PulseBlaster1.WriteCommand([], 0, D2*reps*1e6) #BURN the trench
PulseBlaster1.WriteCommand([], 0, waiting_time) #waiting time
PulseBlaster1.WriteCommand([3], 0, 1000) # trigger the switch 1 to bar (1) ---> switch 1 is placed before the cryo
PulseBlaster1.WriteCommand([4], 0, 1000) # trigger the switch 2 to bar (1)  ---> switch 2 is placed after the cryo
PulseBlaster1.WriteCommand([], 0, experimental_time) #Experimental time
PulseBlaster1.WriteCommand([4], 0, 1000) # trigger the switch 2 to cross (2)  ---> switch 2 is placed after the cryo
PulseBlaster1.WriteCommand([3], 0, 1000) # trigger the switch 1 to cross (2) ---> switch 1 is placed before the cryo
PulseBlaster1.WriteCommand([], 6, 5000) #recycling
PulseBlaster1.ViewProg()

#-----------------------------------------------------------------------------



PulseBlaster1.Start()
Scope. ClearSweeps()
print("Continuing will stop program execution\n");
input("Please press a key to continue.")
#time.sleep(10)
PulseBlaster1.Stop()
# times_out, horiz_unit_out, voltages_out, vertical_unit_out = Scope.ReadWaveform('C2',Info1)
# times_out2, horiz_unit_out2, voltages_out2, vertical_unit_out2 = Scope.ReadWaveform('C3',Info2)
# freqs_out=(times_out*(sweepWidth1/D1)+ startFreq1)*1e-6
# Scope.WriteData('C2',"Read {} Duration.txt".format(D1), freqs_out, 'MHz', voltages_out, vertical_unit_out, voltages_out2, vertical_unit_out2)


# plt.plot(freqs_out,voltages_out)
# plt.show()


# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
PulseBlaster1.Close()
AFG1.close()
Scope.close()
AWG1.close()
rm.close()
#-----------------------------------------------------------------------------