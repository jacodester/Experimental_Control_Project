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
D4 = 1*1e-6 # specified waveform duration in sec
P4 = wf.Points(SR,D4)
t4=wf.Times(SR,duration=D4)
WFName4='JHD_Pulse_151MHz_1us'
freq4= 151e6
wfmData4 = signal.sawtooth(2*np.pi*np.multiply(freq4,t4))
wfmData4 = wf.OptimiseWaveform(wfmData4,freq4,7)
MData1= np.ones(len(wfmData4))
MData2= np.ones(len(wfmData4))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform.')
#AWG1.write_waveform(WFName4,wfmData4,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
AWG1.save_Func(WFName4,'WAV')
AWG1.close()




waiting_time = 10000 #in us
BurnDur=0.1 #Seconds (Light ON) 0.1 = 100ms of burn duration
D2 = 100*1e-6 # specified waveform duration in sec
reps=int(BurnDur/D2)
experimental_time = 10000# 15[sec]*1e6

startFreq2 = [650,700,750,800,850,900,950,1000]
#startFreq2 = [150]
#startFreq2 = [150,200,250,300,350,400,450,500,550,600,650]

sweepWidth2=2e6
#-----------------------------------------------------------------------------
#Make Scope Capture the correct window of signals
Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
Scope.SetVDiv('C1',1)   #1V/div
Scope.SetTrig('C1','NORM',-D1/2,1.35)
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
#Make sure the AFG has the right settings for Hole Burning
#-----------------------------------------------------------------------------
# AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
# AFG1.SetFunction("1","ARB")
# AFG1.SetFunction("1","USER2")
# AFG1.SetBurst("1","OFF")
# AFG1.SetVoltage("1","HIGH",5) #V
# AFG1.SetVoltage("1","LOW",5)
# AFG1.SetPer("1",(D2*reps)*1000+((D2*reps)*1000)*0.01)
# AFG1.SetWidth("1",(D2*reps)*1000)
# AFG1.SetNumCyc("1",1)
# AFG1.SetState("1","ON")
# AFG1.close()
AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
# AFG1.SetFunction("1","PULS")
# AFG1.SetBurst("1","ON")
# AFG1.SetPolarity("1","NORM")
# #AFG1.SetPolarity("1","INV")
# AFG1.SetVoltage("1","HIGH",5) #V
# #AFG1.SetVoltage("1","HIGH",2.5) #V
# AFG1.SetVoltage("1","LOW",0.1)
# #AFG1.SetVoltage("1","LOW",0.98)
# AFG1.SetPer("1",(D2*reps)*1000+((D2*reps)*1000)*0.02) #FG Period
# AFG1.SetWidth("1",(D2*reps)*1000)
# AFG1.SetNumCyc("1",1)
# AFG1.SetState("1","ON")
# AFG1.close()
AFG1.SetFunction("1","ARB")
AFG1.SetFunction("1","USER2")
AFG1.SetPolarity("1","NORM")
AFG1.SetVoltage("1","OFFSET",5)
AFG1.SetPer("1",(D2*reps)*1000+((D2*reps)*1000)*0.02)
AFG1.SetNumCyc("1",1)
AFG1.SetState("1","ON")
AFG1.close()

#%% 

WaveformName=[]
SEQList = []



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
    AWG1.write_waveform(WFName2,wfmData2,MData1,MData2)
    print(time.time()-start)
    print('Waveform HOT  from the oven...MMMM')
    AWG1.save_Func(WFName2,'WAV')
    AWG1.close()
    WaveformName.append(WFName2)
    SEQList.append([(WFName2,''), 1, 'BTR', reps, 0])
SEQList[-1][-1]=1
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
#AWG1.timeout = 5000
AWG1.write_sequence('Test1',SEQList)
AWG1.ChannelFunc('Test1', 1, 'SEQ')
AWG1.SetON_OFF(1,'ON')
AWG1.SetState('RUN')
AWG1.close()
    
    
#%%  
for i in range(100):
    PulseBlaster1.ResetProg()
    PulseBlaster1.WriteCommand([7], 1, 1) #TRIG SF and FG
    PulseBlaster1.ViewProg()
    PulseBlaster1.Start()
    time.sleep(0.2)
    PulseBlaster1.Stop()
    #Make the pulseblaster program as we so desire. PB3 SW1; PB4 SW2; PB6 Trig A AWG; PB7 Tanmoy Trigger
    #-----------------------------------------------------------------------------PulseBlaster1.ViewProg()
    start=time.time()
    PulseBlaster1.ResetProg()
    PulseBlaster1.WriteCommand([0], 0, 1) #TRIG SF and FG
    PulseBlaster1.WriteCommand([], 0, D2*reps*1e6) #BURN the trench
    PulseBlaster1.WriteCommand([], 0, waiting_time) #waiting time
    PulseBlaster1.WriteCommand([3], 0, 1000) # trigger the switch 1 to bar (1) ---> switch 1 is placed before the cryo
    PulseBlaster1.WriteCommand([4], 0, 1000) # trigger the switch 2 to bar (1)  ---> switch 2 is placed after the cryo
    PulseBlaster1.WriteCommand([], 0, experimental_time) #Experimental time
    PulseBlaster1.WriteCommand([4], 0, 1000) # trigger the switch 2 to cross (2)  ---> switch 2 is placed after the cryo
    PulseBlaster1.WriteCommand([3], 0, 1000) # trigger the switch 1 to cross (2) ---> switch 1 is placed before the cryo
    PulseBlaster1.WriteCommand([], 1, 2000) #recycling
    PulseBlaster1.ViewProg()
    end=time.time()
    print(end-start)
 
    
    for step,number in enumerate (WaveformName):
        
        # Make Sequence of the uploaded waveforms
        SEQList=[[(WaveformName[step],''), 1, 'BTR', reps, 1]
          ]
        #SEQList=[[(WaveformName[step],''), 1, 'BTR', reps, 0],[(WFName1,''), 2, 'BTR', 0, 0],[(WFName3,''), 3, 'OFF', 2, 1]]  # For reading Trench/hole
        
        #SEQList=[[(WaveformName[step],''), 1, 'BTR', reps, 0],[(WFName4,''), 2, 'BTR', 0, 1]] # For storing pulse (FG: INVERTED)
        
        AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
        #AWG1.timeout = 5000
        AWG1.write_sequence('Test1',SEQList)
        AWG1.ChannelFunc('Test1', 1, 'SEQ')
        AWG1.SetON_OFF(1,'ON')
        AWG1.SetState('RUN')
        AWG1.close()
        
    
        print(step)
        PulseBlaster1.Start()
        #print("Continuing will stop loop execution\n");
        #input("Please press a key to continue.")
        #time.sleep((reps*waiting_time*1e-6) + 1)
        time.sleep(0.2)
        PulseBlaster1.Stop()
        # Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
        # times_out, horiz_unit_out, voltages_out, vertical_unit_out = Scope.ReadWaveform('C2',Info1)
        # freqs_out=(times_out*(sweepWidth1/D1)+ startFreq1)*1e-6
        # Scope.WriteData('C2',"{}MHz_2MHz_trench.txt".format(startFreq2[step]), freqs_out, 'MHz', voltages_out, vertical_unit_out, voltages_out, vertical_unit_out)
        # Scope.close()
        # # Start Analysis on the data from this trace sweep
        # #-----------------------------------------------------------------------------
        # voltages_out1=af.SavgolSmooth(voltages_out,51,3)
        # af.MakeBaseFig(1,freqs_out, voltages_out, "Freq", "Voltage/Transmission","2MHz trench start at:{}MHz".format(startFreq2[step]),
        #                 "C:/Users/LocalAdmin/Desktop/data/2MHz_trench_{}MHz.png".format(startFreq2[step])) 
        # Freq_new,OD=af.CalcODRegion(freqs_out,voltages_out1,10000,149,165)
        # # Freq_new2,OD2=af.CalcODRegion(freqs_out,voltages_out1,10000,149.5,160.5)
        # af.MakeBaseFig(2,Freq_new, OD, "Freq", "OD","2MHz trench at:{}MHz".format(startFreq2[step]),
        #                 "C:/Users/LocalAdmin/Desktop/data/2MHz_trench_{}MHz_OD.png".format(startFreq2[step]))
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

# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
#%% 
PulseBlaster1.Close()
rm.close()
#-----------------------------------------------------------------------------