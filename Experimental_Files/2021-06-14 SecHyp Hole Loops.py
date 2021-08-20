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




#-----------------------------------------------------------------------------

#wavemeter = pyBristolSCPI('1.1.1.6')

#Make sure that the AWG has all the desired waveforms in a sequence
#-----------------------------------------------------------------------------
SR = 25e9 # AWG sampling rate


#Make and Upload first Waveform: READ
D1 = 1000*1e-6 # specified waveform duration in sec
P1 = wf.Points(SR,D1)
t1=wf.Times(SR,duration=D1)
WFName1='JHD_Read_149_75MHz_150_25MHz_1000us'
startFreq1=149.75e6
sweepWidth1=0.5e6
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
AWG1.write_waveform(WFName1,wfmData1,MData1,MData2)
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
#AWG1.save_Func(WFName3,'WAV')
AWG1.close()



Holedepths = []
HoleWidths1 = []
Betas= np.concatenate((np.arange(0.1,1.1,0.1),np.arange(1,11,1),np.arange(10,110,10)))
for step,value in enumerate(Betas):
    time.sleep(1)
    #Make and Upload Second Waveform: BURN
    D2 = 100*1e-6 # specified waveform duration in sec
    P2 = wf.Points(SR,D2)
    t2=wf.Times(SR,duration=D2)
    WFName2='JHD_Hole_SecHype_100us'
    freq2= wf.tanHypeSawtooth(value, 0.001e6, 150e6, len(t2),1)
    wfmData2 = signal.sawtooth(2*np.pi*np.multiply(freq2,t2))
    wfmData2 = wf.OptimiseWaveform(wfmData2,freq2,7)
    MData1= np.ones(len(wfmData2))
    MData2= np.ones(len(wfmData2))
    MData1[0:9]=0
    MData2[0:9]=0
    start=time.time()
    AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
    print('Keep Calm. I am uploading your waveform.')
    AWG1.write_waveform(WFName2,wfmData2,MData1,MData2)
    print(time.time()-start)
    print('Waveform HOT from the oven...MMMM')
    #AWG1.save_Func(WFName2,'WAV')
    AWG1.close()
    
    
    TotalDur=0.003 #Seconds
    reps=int(TotalDur/D2);
    waiting_time=30000
    # Make Sequence of the uploaded waveforms
    
    SEQList=[]
    for i in range(reps):
        SEQList.append([(WFName2,''), i+1, 'BTR', 1, 0])
    SEQList.append([(WFName1,''), reps+1, 'ATR', 0, 0])
    SEQList.append([(WFName3,''), reps+2, 'OFF', 2, 1])  
    
    AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
    AWG1.write_sequence('Test1',SEQList)
    AWG1.ChannelFunc('Test1', 1, 'SEQ')
    AWG1.SetON_OFF(1,'ON')
    AWG1.SetState('RUN')
    AWG1.close()
    #-----------------------------------------------------------------------------
    
    
    #Make sure the AFG has the right settings for Hole Burning
    #-----------------------------------------------------------------------------
    high = 5
    shape= 'SecHype'
    AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
    z=wf.SecHypePulse(value,2000,600,400,(100, 10))
    #plt.plot(z)
    AFG1.set_custom_waveform(z,memory_num=4,normalise=True, print_progress=False)
    AFG1.SetFunction("1","ARB")
    AFG1.SetFunction("1","USER4")
    AFG1.SetBurst("1","ON")
    AFG1.SetVoltage("1","HIGH",high) #V
    AFG1.SetVoltage("1","LOW",0.1)
    AFG1.SetPer("1",(D2)*1000)#+ 0.01*(D2*reps)*1000)
    AFG1.SetNumCyc("1",1)
    AFG1.SetState("1","ON")
    AFG1.close()
    
    
    #Make Scope Capture the correct window of signals
    #-----------------------------------------------------------------------------
    Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
    Scope.SetTrig('C1','SINGLE',-D1*2/3,0.35)
    Scope.SetOffset('C2',-0.135,"VOLTS") #35mV/div
    Scope.SetVDiv('C2',0.038)   #20mV/div
    Scope.SetSampleRate('C1',1000000)
    Scope.SetTDiv('C2',200e-6)
    Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
    Info1=Scope.ReadInfo('C2')
    Scope.close()
    #-----------------------------------------------------------------------------
    
    
    #Make the pulseblaster program as we so desire. 
    #-----------------------------------------------------------------------------
    PulseBlaster1.ResetProg()
    PulseBlaster1.WriteCommand([0,1], 2, 1, reps) # 1us Trigger for AFG and AWG and Loop
    PulseBlaster1.WriteCommand([], 0, D2*1e6) # Do nothing for duration of Burn
    PulseBlaster1.WriteCommand([], 3, waiting_time,0)  # waiting in us and end the loop
    PulseBlaster1.WriteCommand([6,2], 0, D1*1e6) # Trigger 6 AWG (TrigA) for read, and 2 scope for the duration of the read pulse
    PulseBlaster1.WriteCommand([], 1, 5000) # Do Nothing. 
    PulseBlaster1.ViewProg()
    
    #-----------------------------------------------------------------------------
    
    #wl = wavemeter.readWL()
    #freq = wavemeter.readFREQ()
    # print(wl)
    # print(freq)

    
    PulseBlaster1.Start()
    time.sleep((reps*waiting_time*1e-6) + 1)
    #print("Continuing will stop program execution\n");
    #input("Please press a key to continue.")
    PulseBlaster1.Stop()
    Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
    times_out, horiz_unit_out, voltages_out, vertical_unit_out = Scope.ReadWaveform('C2',Info1)
    freqs_out=(times_out*(sweepWidth1/D1)+ startFreq1)*1e-6
    Scope.WriteData('C2',"{}us_Beta {}_{}V.txt".format(round(D2*1e6*reps,3),value,high), freqs_out, 'MHz', voltages_out, vertical_unit_out, voltages_out, vertical_unit_out)
    Scope.close()
     
    
     
    
    voltages_out1=af.SavgolSmooth(voltages_out,51,3)
    #af.MakeBaseFig(1,freqs_out, voltages_out, "Freq", "Voltage/Transmission",Filename="C:/Users/LocalAdmin/Desktop/data/{}us_Beta {}_{}V.png".format(round(D2*1e6*reps,3),value,high))
    Freq_new,OD=af.CalcODRegion(freqs_out,voltages_out1,10000,149.75,160)
    
    af.MakeBaseFig(2,Freq_new, OD, "Freq", "OD",close=1)
    Depth,Width1,Inds,minInd=af.CalcHoleParam(Freq_new, OD, 149.75, 150.25, 149.80, 149.90)
    
    af.MakeBaseFig(2, Freq_new[Inds[0][0]:Inds[0][-1]], OD[Inds[0][0]:Inds[0][-1]],title='{} MHz'.format(round(Width1,3)),Filename='C:/Users/LocalAdmin/Desktop/data/Duration {}_Width_Beta {}_{}V_OD.png'.format(round(D2*1e6*reps,3),value,high))
    
    Holedepths.append(Depth)
    HoleWidths1.append(Width1)
    
        
    

# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
PulseBlaster1.Close()
rm.close()
#-----------------------------------------------------------------------------
#del wavemeter