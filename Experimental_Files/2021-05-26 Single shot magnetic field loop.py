# -*- coding: utf-8 -*-
"""
Created on Wed May 26 14:16:19 2021

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
import Device_Files.MagnetSupplyClassObjects as MO
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


#Make a magnet that we can reset for a series of trials 
Magnet=rm.open_resource('GPIB0::9::INSTR',resource_pyclass=MO.MagnetSupply)
print(Magnet.query('*IDN?'))
Magnet.SetCurrent(0,1)
Magnet.SetState('ON')
Magnet.SetVolts(5,10)
Magnet.close()



#-----------------------------------------------------------------------------

#wavemeter = pyBristolSCPI('1.1.1.6')

#Make sure that the AWG has all the desired waveforms in a sequence
#-----------------------------------------------------------------------------
SR = 25e9 # AWG sampling rate

#Make and Upload first Waveform: READ
D1 = 500*1e-6 # specified waveform duration in sec
P1 = wf.Points(SR,D1)
t1=wf.Times(SR,duration=D1)
WFName1='JHD_Read_149MHz_151MHz_500us'
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

#Make and Upload Second Waveform: BURN
D2 = 1*1e-6 # specified waveform duration in sec
P2 = wf.Points(SR,D2)
t2=wf.Times(SR,duration=D2)
WFName2='JHD_Hole_150MHz_1us'
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

reps=2000 # X 1us
# Make Sequence of the uploaded waveforms
SEQList=[[(WFName2,''), 1, 'BTR', reps, 0],     
         [(WFName1,''), 2, 'BTR', 0, 0],
         [(WFName3,''), 3, 'OFF', 0, 1]
         ]
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
AWG1.write_sequence('Test1',SEQList)
AWG1.ChannelFunc('Test1', 1, 'SEQ')
AWG1.SetON_OFF(1,'ON')
AWG1.SetState('RUN')
AWG1.close()
#-----------------------------------------------------------------------------

high = 5
#Make sure the AFG has the right settings for Hole Burning
#-----------------------------------------------------------------------------
AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
AFG1.SetFunction("1","PULS")
AFG1.SetBurst("1","ON")
AFG1.SetVoltage("1","HIGH",high) #V
AFG1.SetVoltage("1","LOW",0.1)
AFG1.SetPer("1",(D2*reps)*1000+5)
AFG1.SetWidth("1",(D2*reps)*1000)
AFG1.SetNumCyc("1",1)
AFG1.SetState("1","ON")
AFG1.close()
#-----------------------------------------------------------------------------



#Make Scope Capture the correct window of signals
#-----------------------------------------------------------------------------
Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
Scope.SetTrig('C1','SINGLE',-D1/2,0.35)
Scope.SetOffset('C2',-0.053,"VOLTS") #35mV/div
#Scope.SetOffset('C2',-0.271,"VOLTS") #100mV/div
#Scope.SetOffset('C2',-0.50,"VOLTS") #200mV/div
Scope.SetVDiv('C2',0.038)   #20mV/div
Scope.SetSampleRate('C1',100000)
Scope.SetTDiv('C2',200e-6)
Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C2')
Info2=Scope.ReadInfo('C3')
Scope.close()
#-----------------------------------------------------------------------------

#Make the pulseblaster program as we so desire. 
#-----------------------------------------------------------------------------
PulseBlaster1.ViewProg()
PulseBlaster1.WriteCommand([0,1], 0, 1) #SF and AFG
PulseBlaster1.WriteCommand([], 0, D2*reps*1e6) 
PulseBlaster1.WriteCommand([], 0, 15000)  #waiting in us
PulseBlaster1.WriteCommand([0,2], 0, D1*1e6) #SF and Scope
PulseBlaster1.WriteCommand([], 1, 5000)
PulseBlaster1.WriteProg()

#-----------------------------------------------------------------------------

#wl = wavemeter.readWL()
#freq = wavemeter.readFREQ()
# print(wl)
# print(freq)
Holedepths = []
HoleWidths1 = []
HoleWidths2 = []
currstart=0
currend=19.5  # 10Amps 1T
inter=0.5
Fields=np.arange(currstart,currend+inter,inter)
for step,Field in enumerate(Fields):
    Magnet=rm.open_resource('GPIB0::9::INSTR',resource_pyclass=MO.MagnetSupply)
    Magnet.SetCurrent(Field,20) #ramping up in _ secs depending on the intervel
    Magnet.close()
    #print(Magnet.GetLevel())
    time.sleep(10)
    

    PulseBlaster1.Start()
    time.sleep(1)
    PulseBlaster1.Stop()
    Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
    times_out, horiz_unit_out, voltages_out, vertical_unit_out = Scope.ReadWaveform('C2',Info1)
    #times_out2, horiz_unit_out2, voltages_out2, vertical_unit_out2 = Scope.ReadWaveform('C3',Info2)
    freqs_out=(times_out*(sweepWidth1/D1)+ startFreq1)*1e-6
    Scope.WriteData('C2',"{}us_burn_hole_5V_{}Amps.txt".format(D2*1e6*reps,round(Fields[step],3)), freqs_out, 'MHz', voltages_out, vertical_unit_out, voltages_out, vertical_unit_out)
    Scope.close()
    
    voltages_out1=signal.savgol_filter(voltages_out,51,3)
    
    plot1 = plt. figure()
    plt.plot(freqs_out,voltages_out)
    plt.xlabel("Freq")
    plt.ylabel("Voltage/Transmission")
    plt.show()
    plt.savefig("{}us_burn_hole_5V_{}Amps.png".format(D2*1e6*reps,round(Fields[step],3)))
    plt.close()
    
    Freq_noise = freqs_out[-10000:-1]
    Data2_noise = voltages_out1[-10000:-1] 
    
    #plt.plot(Freq_noise, Data2_noise)
    
    indices = [idx for idx,val in enumerate(freqs_out) if val > 149.02]
    
    Freq_new = freqs_out[indices[0]:indices[-1]]
    Data2_new = voltages_out1[indices[0]:indices[-1]]
    
    N = np.true_divide(Data2_new, np.mean(Data2_noise))
    
    OD = -np.log(N)
    
    plot2 = plt. figure()
    plt.plot(Freq_new,OD)
    plt.xlabel("Freq")
    plt.ylabel("OD")
    plt.show()
    plt.savefig("{}us_burn_hole_5V_{}Amps_OD.png".format(D2*1e6*reps,round(Fields[step],3)))
    plt.close()
    
    indices1 = [idx1 for idx1,val1 in enumerate(Freq_new) if (val1 > 149 and val1 < 151)]
    indices2 = [idx2 for idx2,val2 in enumerate(Freq_new) if (val2 > 149.2 and val2 < 149.5)]
    
    HoleOD = np.mean(OD[indices2[0]:indices2[-1]]) - np.amin(OD[indices1[0]:indices1[-1]])
    Holedepths.append(HoleOD)


    


plt.plot(Fields, Holedepths,marker='o')
mean=np.mean(Holedepths)
std=np.std(Holedepths)
plt.plot(Fields, mean*np.ones(len(Holedepths)))
plt.plot(Fields, (mean+std)*np.ones(len(Holedepths)),'-')
plt.plot(Fields, (mean-std)*np.ones(len(Holedepths)),'-')
plt.xlabel("Current (Amp)")
plt.ylabel("Hole OD")
plt.show()
plt.savefig("C:/Users/LocalAdmin/Desktop/data/All Depths.png")
plt.close()



# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
PulseBlaster1.Close()
Magnet=rm.open_resource('GPIB0::9::INSTR',resource_pyclass=MO.MagnetSupply)
Magnet.SetCurrent(0,300) #sec ramping down depends on the final magnetic field
Magnet.SetVolts(0,5)
Magnet.SetState('OFF')
Magnet.close()
rm.close()
#-----------------------------------------------------------------------------
#del wavemeter