# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 13:55:53 2021

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
WFName1='JHD_Read_149MHz_159MHz_2ms'
startFreq1=149e6
sweepWidth1=10e6
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
AWG1.save_Func(WFName1,'WAV')
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
AWG1.save_Func(WFName3,'WAV')
AWG1.close()

#Make and Upload Pulse that you would like to store: PULSE
# D4 = 1*1e-6 # specified waveform duration in sec
# P4 = wf.Points(SR,D4)
# t4=wf.Times(SR,duration=D4)
# WFName4='JHD_Pulse_151MHz_1us'
# freq4= 151e6
# wfmData4 = signal.sawtooth(2*np.pi*np.multiply(freq4,t4))
# wfmData4 = wf.OptimiseWaveform(wfmData4,freq4,7)
# MData1= np.ones(len(wfmData4))
# MData2= np.ones(len(wfmData4))
# MData1[0:9]=0
# MData2[0:9]=0
# start=time.time()
# AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
# print('Keep Calm. I am uploading your waveform.')
# #AWG1.write_waveform(WFName4,wfmData4,MData1,MData2)
# print(time.time()-start)
# print('Waveform HOT from the oven...MMMM')
# AWG1.save_Func(WFName4,'WAV')
# AWG1.close()

#Make and Upload first Waveform: Tanmoy freq pulse
D5 = 2000*1e-6 # specified waveform duration in sec
P5 = wf.Points(SR,D5)
t5=wf.Times(SR,duration=D5)
WFName5='Tanmoy_pulse_120MHz_100MHzBW_2ms'
startFreq5=150e6
sweepWidth5=100e6
freq5=wf.chirpedSawtooth(startFreq5,sweepWidth5,len(t5))
wfmData5 = signal.sawtooth(2*np.pi*np.multiply(freq5,t5))
wfmData5 = wf.OptimiseWaveform(wfmData5,freq5,7)
MData1= np.ones(len(wfmData5))
MData2= np.ones(len(wfmData5))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform')
AWG1.write_waveform(WFName5,wfmData5,MData1,MData2)
print(time.time()-start)
print('Waveform HOT  from the oven...MMMM')
AWG1.save_Func(WFName5,'WAV')
AWG1.close()




waiting_time = 10000 #in us
BurnDur=0.1 #Seconds (Light ON) 0.1 = 100ms of burn duration
D2 = 100*1e-6 # specified waveform duration in sec
reps=int(BurnDur/D2)
experimental_time = 10000# 15[sec]*1e6

#startFreq2 = [450,500,550,600,650,700,750,800,850,900]
#startFreq2 = [150]
startFreq2 = [150,155,160,165,170,175,180,185,190,195,200,205,210,215,220,225,230,235,240,245,250]

sweepWidth2=2e6
#-----------------------------------------------------------------------------
#Make Scope Capture the correct window of signals
Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
Scope.SetVDiv('C1',1)   #1V/div
Scope.SetTrig('C1','NORM',-D1/2,1.35)
Scope.SetOffset('C2',-0.100,"VOLTS") #35mV/div
#Scope.SetOffset('C2',-0.271,"VOLTS") #100mV/div
#Scope.SetOffset('C2',-0.50,"VOLTS") #200mV/div
Scope.SetVDiv('C2',0.2)   #25mV/div
#Scope.SetVDiv('C2',1)   #25mV/div
Scope.SetSampleRate('C1',100000)
Scope.SetTDiv('C2',2e-3)
Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C2')
Info2=Scope.ReadInfo('C3')
Scope.close()
#Make sure the AFG has the right settings for Hole Burning
# def gaussian(A,x, mu, sig):
#     return A*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
# A = 1
# mu = 7875
# sig = 100
#-----------------------------------------------------------------------------
AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
z = np.zeros(7000) #burn + wait + pulse (7,000 pts to start with)
z[0:5000] = 10000 # burn 100ms 5000 pts HIGH
#z[5001:5751]=0 #wait 15 ms LOW 750pts
z[5001:5501] = 0 # wait 10 ms 500pts
z[5502:-1] = 4000*signal.gaussian(len(z[5502:-1]),17)
#z[5752:-1]=4000*signal.gaussian(len(z[5752:-1]),17) #2ms pulse corresponds 17std dev around 100pts 

#z[5752:-1]= gaussian(A,z[5752:-1],mu,sig)
#---------
AFG1.set_custom_waveform(z,memory_num=3,normalise=True, print_progress=False)
AFG1.SetPolarity("1","NORM")
AFG1.SetPer("1",(D2*reps)*1000*(len(z)/len(z[0:5000]))) #FG Period
AFG1.SetPer("1",124) #FG Period
AFG1.SetFunction("1","ARB")
AFG1.SetFunction("1","USER3")
AFG1.SetVoltage("1","HIGH",4.5) #V
AFG1.SetVoltage("1","LOW",0.1)
AFG1.SetNumCyc("1",1)
#AFG1.SetState("1","ON")
#plt.plot(z)
AFG1.close()

# AFG1.SetFunction("1","PULS")
# AFG1.SetBurst("1","ON")
#%% 

WaveformName=[]


for stepp,value in enumerate(startFreq2):
    #Make and Upload Waveform: TRENCH
    
    P2 = wf.Points(SR,D2)
    t2=wf.Times(SR,duration=D2)
    WFName2='AJ_Trench_{}MHz_{}BW_MHz_2ms'.format(startFreq2[stepp],startFreq2[stepp]+2)
    
    freq2=wf.chirpedSawtooth(startFreq2[stepp]*1e6,sweepWidth2,len(t2))
    wfmData2 = signal.sawtooth(2*np.pi*np.multiply(freq2,t2))
    wfmData2 = wf.OptimiseWaveform(wfmData2,freq2,7)
    MData1= np.ones(len(wfmData2))
    MData2= np.ones(len(wfmData2))
    MData1[0:9]=0
    MData2[0:9]=0
    start=time.time()
    AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
    print('Keep Calm. I am uploading your waveform')
    #AWG1.write_waveform(WFName2,wfmData2,MData1,MData2)
    print(time.time()-start)
    print('Waveform HOT  from the oven...MMMM')
    AWG1.save_Func(WFName2,'WAV')
    AWG1.close()
    WaveformName.append(WFName2)
    
#%%
freq_responses = np.zeros([len(startFreq2),99802])  
for i in range(1):
    # PulseBlaster1.ResetProg()
    # PulseBlaster1.WriteCommand([2], 1, 1) #TRIG Scope
    # PulseBlaster1.ViewProg()
    # PulseBlaster1.Start()
    # time.sleep(0.1)
    
    start=time.time()
    PulseBlaster1.ResetProg()
    PulseBlaster1.WriteCommand([0,1], 0, 1) #TRIG SF and FG
    PulseBlaster1.WriteCommand([], 0, D2*reps*1e6) #BURN the trench
    PulseBlaster1.WriteCommand([], 0, waiting_time) #waiting time
    PulseBlaster1.WriteCommand([0,2], 0, D5*1e6) #Read and trigger the AWG and Scope
    PulseBlaster1.WriteCommand([], 6, 30000) #recycling
    PulseBlaster1.ViewProg()
    end=time.time()
    print(end-start)
 
    j = np.empty([len(startFreq2),99802])
    for step,number in enumerate (WaveformName):    
        # Make Sequence of the uploaded waveforms
        #SEQList=[[(WaveformName[step],''), 1, 'BTR', reps, 1]
        #  ]
        SEQList=[[(WaveformName[step],''), 1, 'BTR', reps, 0],[(WFName5,''), 2, 'BTR', 1, 1]]  # For reading Trench/hole
        
        
        AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
        #AWG1.timeout = 5000
        AWG1.write_sequence('Test1',SEQList)
        AWG1.ChannelFunc('Test1', 1, 'SEQ')
        AWG1.SetON_OFF(1,'ON')
        AWG1.SetState('RUN')
        AWG1.close()
        
        
    
        print(step)
        PulseBlaster1.Start()
        print("Continuing will stop loop execution\n");
        input("Please press a key to continue.")
        #time.sleep((reps*waiting_time*1e-6) + 1)
        #time.sleep(2)
        
        PulseBlaster1.Stop()
        Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
        times_out, horiz_unit_out, voltages_out, vertical_unit_out = Scope.ReadWaveform('C2',Info1)
        freqs_out=(times_out*(sweepWidth1/D1)+ startFreq1)*1e-6
        voltages_out=af.SavgolSmooth(voltages_out,51,3)
        Scope.WriteData('C2',"{}MHz_2MHz_trench.txt".format(startFreq2[step]), times_out, 'Sec', voltages_out, vertical_unit_out, voltages_out, vertical_unit_out)
        Scope.close()
        j[step,:]= voltages_out
        # Start Analysis on the data from this trace sweep
        #-----------------------------------------------------------------------------
        #voltages_out1=af.SavgolSmooth(voltages_out,51,3)
        af.MakeBaseFig(1,times_out, voltages_out, "Time", "Voltage/Transmission","2MHz trench start at:{}MHz".format(startFreq2[step]),
                        "C:/Users/LocalAdmin/Desktop/data/2MHz_trench_{}MHz.png".format(startFreq2[step])) 
        #Freq_new,OD=af.CalcODRegion(freqs_out,voltages_out1,10000,149,165)
        # Freq_new2,OD2=af.CalcODRegion(freqs_out,voltages_out1,10000,149.5,160.5)
        # af.MakeBaseFig(2,Freq_new, OD, "Freq", "OD","2MHz trench at:{}MHz".format(startFreq2[step]),
        #                 "C:/Users/LocalAdmin/Desktop/data/2MHz_trench_{}MHz_OD.png".format(startFreq2[step]))
    freq_responses = np.add(j,freq_responses)  #-----------------------------------------------------------------------------
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

# Section of graceful disconnection from different device objects
freq_response_new = np.divide(freq_responses,4)  #-----------------------------------------------------------------------------
# b =np.load("C:/Users/LocalAdmin/Desktop/data/2cycles.npy")
np.save("C:/Users/LocalAdmin/Desktop/data/150MHzFiltering",freq_response_new)
# plt.plot(b[20,:])
#%% 
PulseBlaster1.Close()
rm.close()
#-----------------------------------------------------------------------------
# amp = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# for i in amp:
#     plt.plot(freq_response_new[i,:]-freq_response_new[1,:])