# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:59:13 2021

@author: LocalAdmin
"""
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
from Device_Files.WavemeterClassObject import *
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
Scope.close()

#Make a digital AWG object from the tektronix object class
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print(AWG1.query('*IDN?'))
AWG1.close()

#Make a digital Pulseblaster object from the pulse blaster class definition
PulseBlaster1=pb.PulseBlaster()
PulseBlaster1.ResetProg()

#Make a digital Wavemeter object from the class definition
wavemeter = pyBristolSCPI('1.1.1.6')
#-----------------------------------------------------------------------------



#Make sure that the AWG has all the desired waveforms in a sequence
#-----------------------------------------------------------------------------
SR = 25e9 # AWG sampling rate

#Make and Upload first Waveform: READ
D1 = 1000*1e-6 # specified waveform duration in sec
P1 = wf.Points(SR,D1)
t1=wf.Times(SR,duration=D1)
WFName1='JHD_Read_148MHz_152MHz_1ms'
startFreq1=148e6
sweepWidth1=4e6
freq1=wf.chirpedSawtooth(startFreq1,sweepWidth1,len(t1))
wfmData1 = signal.sawtooth(2*np.pi*np.multiply(freq1,t1))
wfmData1 = wf.OptimiseWaveform(wfmData1,freq1,7)
MData1= np.ones(len(wfmData1))
MData2= np.ones(len(wfmData1))
MData1[0:1]=0
MData2[0:1]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform')
AWG1.write_waveform(WFName1,wfmData1,MData1,MData2)
print(time.time()-start)
print('Waveform HOT  from the oven...MMMM')
#AWG1.save_Func(WFName1,'WAV')
AWG1.close()

#Make and Upload Second Waveform: BURN1
D2 = 1*1e-5 # specified waveform duration in sec
P2 = wf.Points(SR,D2)
t2=wf.Times(SR,duration=D2)
WFName2='JHD_Hole_149MHz_1us'
freq2= 149e6
wfmData2 = signal.sawtooth(2*np.pi*np.multiply(freq2,t2))
wfmData2 = wf.OptimiseWaveform(wfmData2,freq2,7)
MData1= np.ones(len(wfmData2))
MData2= np.ones(len(wfmData2))
MData1[0:1]=0
MData2[0:1]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform.')
AWG1.write_waveform(WFName2,wfmData2,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName2,'WAV')
AWG1.close()

#Make and Upload Second Waveform: BURN2
D3 = 1*1e-5 # specified waveform duration in sec
P3 = wf.Points(SR,D3)
t3=wf.Times(SR,duration=D3)
WFName3='JHD_Hole_151MHz_1us'
freq3= 151e6
wfmData3 = signal.sawtooth(2*np.pi*np.multiply(freq3,t3))
wfmData3 = wf.OptimiseWaveform(wfmData3,freq3,7)
MData1= np.ones(len(wfmData3))
MData2= np.ones(len(wfmData3))
MData1[0:1]=0
MData2[0:1]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform.')
AWG1.write_waveform(WFName3,wfmData3,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName2,'WAV')
AWG1.close()

# specified the DC delay
D4 =10*1e-6 # specified waveform duration in sec 
P4 = wf.Points(SR,D4)
t4=wf.Times(SR,duration=D4)
WFName4='JHD_Delay_1ms'
wfmData4 = np.ones(len(t4))
MData1= np.ones(len(wfmData4))
MData2= np.ones(len(wfmData4))
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform Master.')
AWG1.write_waveform(WFName4,wfmData4,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName3,'WAV')
AWG1.close()


D5=D2#+D3
#wfmData5=np.concatenate([wfmData2,wfmData3])
#wfmData5=np.multiply(wfmData2,wfmData3)
wfmData5=np.multiply(np.add(wfmData2,wfmData3),0.25)
#wfmData5=np.zeros(len(wfmData2))
#for step,val in enumerate(wfmData2):
#    if (wfmData2[step]+wfmData3[step] < 0) :
#        wfmData5[step]=(wfmData2[step]+wfmData3[step]) % -max(wfmData2)
#    else:
#        wfmData5[step]=(wfmData2[step]+wfmData3[step]) % max(wfmData2)
#wfmData5=np.mod(np.add(wfmData2,wfmData3),-max(wfmData2))
MData1= np.ones(len(wfmData5))
MData2= np.ones(len(wfmData5))
MData1[0:9]=0
MData2[0:9]=0
WFName5='JHD_Hole_product_Xus'
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform.')
AWG1.write_waveform(WFName5,wfmData5,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName5,'WAV')
AWG1.close()


total=2e-3
reps=total/D2#(D2+D3)
# Make Sequence of the uploaded waveforms
SEQList=[[(WFName5,''), 1, 'BTR', round(reps), 0],
         [(WFName1,''), 2, 'BTR', 0, 0],
         [(WFName4,''), 3, 'OFF', 200, 1]
         ]
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
AWG1.timeout=20000
AWG1.write_sequence('Test1',SEQList)
AWG1.ChannelFunc('Test1', 1, 'SEQ')
AWG1.SetON_OFF(1,'ON')
time.sleep(1)
AWG1.SetState('RUN')
AWG1.close()
#-----------------------------------------------------------------------------


#Make sure the AFG has the right settings for Hole Burning
#-----------------------------------------------------------------------------
AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
AFG1.SetFunction("1","PULS")
AFG1.SetBurst("1","ON")
AFG1.SetVoltage("1","HIGH",5) #V
AFG1.SetVoltage("1","LOW",0.7)
AFG1.SetPer("1",(D5*reps)*1000+5)
AFG1.SetWidth("1",(D5*reps)*1000)
AFG1.SetNumCyc("1",1)
AFG1.SetState("1","ON")
AFG1.close()
#-----------------------------------------------------------------------------



#Make Scope Capture the correct window of signals
#-----------------------------------------------------------------------------
Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
Scope.timeout=200000
Scope.SetTrig('C1','SINGLE',-D1/2,0.35)
Scope.SetOffset('C2',-0.10,"VOLTS")
Scope.SetVDiv('C2',0.1)
Scope.SetSampleRate('C1',100000)
Scope.SetTDiv('C2',500e-6)
Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C2')
Info2=Scope.ReadInfo('C3')
Scope.close()
#-----------------------------------------------------------------------------

#Make the pulseblaster program as we so desire. 
#-----------------------------------------------------------------------------
PulseBlaster1.ViewProg()
PulseBlaster1.WriteCommand([0,1], 0, 1) #SF and AFG
PulseBlaster1.WriteCommand([], 0, D5*reps*1e6) 
PulseBlaster1.WriteCommand([], 0, 15000)  #waiting in us
PulseBlaster1.WriteCommand([0,2], 0, D1*1e6) #SF and Scope
PulseBlaster1.WriteCommand([], 1, 5000)
PulseBlaster1.WriteProg()

#-----------------------------------------------------------------------------

wl = wavemeter.readWL()
freq = wavemeter.readFREQ()
print(wl)
print(freq)

FileName="{}usEach_2_Holes_0G".format(round(D2*1e6,2))
Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
Scope.timeout=200000
PulseBlaster1.Start()
time.sleep(1)
PulseBlaster1.Stop()
times_out, horiz_unit_out, voltages_out, vertical_unit_out = Scope.ReadWaveform('C2',Info1)
#times_out2, horiz_unit_out2, voltages_out2, vertical_unit_out2 = Scope.ReadWaveform('C3',Info2)
freqs_out=(times_out*(sweepWidth1/D1)+ startFreq1)*1e-6
Scope.WriteData('C2',FileName +".txt", freqs_out, 'MHz', voltages_out, vertical_unit_out, voltages_out, vertical_unit_out)




# Section of Analysis for the signal
#-----------------------------------------------------------------------------
voltages_out1=signal.savgol_filter(voltages_out,51,3)

plot1 = plt. figure(1)
plt.plot(freqs_out,voltages_out)
plt.title("Transmission vs Scan Frequency")
plt.xlabel("Freq")
plt.ylabel("Voltage/Transmission")
plt.show()
plt.savefig("C:/Users/LocalAdmin/Desktop/data/" + FileName + ".png")

Freq_noise = freqs_out[-10000:-1]
Data2_noise = voltages_out1[-10000:-1] 

#plt.plot(Freq_noise, Data2_noise)

indices = [idx for idx,val in enumerate(freqs_out) if val > (((startFreq1*1e-6)+0.02))]

Freq_new = freqs_out[indices[0]:indices[-1]]
Data2_new = voltages_out1[indices[0]:indices[-1]]

N = np.true_divide(Data2_new, np.mean(Data2_noise))

OD = -np.log(N)

plot2 = plt. figure(2)
plt.plot(Freq_new,OD)
plt.title("OD vs Scan Frequency")
plt.xlabel("Freq")
plt.ylabel("OD")
plt.show()
plt.savefig("C:/Users/LocalAdmin/Desktop/data/" + FileName + "_OD.png")




# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
del wavemeter
PulseBlaster1.Close()
Scope.close()
rm.close()
#-----------------------------------------------------------------------------
