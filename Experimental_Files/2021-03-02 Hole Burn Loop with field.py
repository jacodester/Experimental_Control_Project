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
import Device_Files.MagnetSupplyClassObjects as MO
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

#Make a magnet that we can reset for a series of trials 
Magnet=rm.open_resource('GPIB0::9::INSTR',resource_pyclass=MO.MagnetSupply)
print(Magnet.query('*IDN?'))
Magnet.SetCurrent(0,1)
Magnet.SetState('ON')
Magnet.SetVolts(5,10)





#-----------------------------------------------------------------------------


#Make sure that the AWG has all the desired waveforms in a sequence
#-----------------------------------------------------------------------------
SR = 25e9 # AWG sampling rate

#Make and Upload first Waveform
D1 = 0.0005 # specified waveform duration
P1 = wf.Points(SR,D1)
t1=wf.Times(SR,duration=D1)
WFName1='JHD_Read_380MHz_420MHz_500us'
startFreq1=375e6
sweepWidth1=50e6
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



Dur= 0.0001
#powers=np.arange(1,5.25,0.25)


P = wf.Points(SR,Dur)
t=wf.Times(SR,duration=Dur)
freq= 400e6
WFName='JHD_Hole_{}MHz_100us_Volts'.format(int(freq))
wfmData = signal.sawtooth(2*np.pi*np.multiply(freq,t))
wfmData = wf.OptimiseWaveform(wfmData,freq,7)
MData1= np.ones(len(wfmData))
MData2= np.ones(len(wfmData))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
print('Keep Calm. I am uploading waveform.')
AWG1.write_waveform(WFName,wfmData,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName2,'WAV')



#Make Scope Capture the correct window of signals
#-----------------------------------------------------------------------------
Scope.SetTrig('C1','NORM',-D1/2,0.35)
Scope.SetOffset('C2',-0.153,"VOLTS")
Scope.SetVDiv('C2',0.035)
Scope.SetSampleRate('C1',100000)
Scope.SetTDiv('C2',50e-6)
Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C2')
#-----------------------------------------------------------------------------


Reps=[]
TotDur=[]
currstart=2
Magnet.SetCurrent(currstart,100)
currend=10
inter=0.5
Fields=np.arange(currstart,currend+inter,inter)
for step,Field in enumerate(Fields):
    # Make Sequence of the uploaded waveforms
    Reps.append(int(0.1/Dur))
    TotDur.append(Dur*Reps[step])
    SEQList=[[(WFName,''), 1, 'BTR', Reps[step], 0],
             [(WFName1,''), 2, 'BTR', 1, 1]
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
    AFG1.SetPer("1",(TotDur[step])*1000+5)
    AFG1.SetWidth("1",(TotDur[step])*1000)
    AFG1.SetNumCyc("1",1)
    AFG1.SetState("1","ON")
    #-----------------------------------------------------------------------------
    



    #Make the pulseblaster program as we so desire. 
    #-----------------------------------------------------------------------------
    
    PulseBlaster1.ResetProg()
    PulseBlaster1.WriteCommand([0,1], 0, 1)
    PulseBlaster1.WriteCommand([], 0, TotDur[step]*1e6) 
    PulseBlaster1.WriteCommand([], 0, 15000)
    PulseBlaster1.WriteCommand([0,2], 0, D1*1e6) #
    PulseBlaster1.WriteCommand([], 6, 5000)
    PulseBlaster1.ViewProg()

    #-----------------------------------------------------------------------------


    Magnet.SetCurrent(Field,10)
    print(Magnet.GetLevel())
    time.sleep(10)
    PulseBlaster1.Start()
    Scope. ClearSweeps()
    print("Continuing will stop program execution\n");
    input("Please press a key to continue.")
    PulseBlaster1.Stop()
    times_out, horiz_unit_out, voltages_out, vertical_unit_out=Scope.ReadWaveform('C2',Info1)
    freqs_out=(times_out*(sweepWidth1/D1)+ startFreq1)*1e-6
    Scope.WriteData('C2',"Hole at 400MHz_{} Field.txt".format(Fields[step]), freqs_out, 'MHz', voltages_out, vertical_unit_out)





# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
Magnet.SetCurrent(0,100)
Magnet.SetVolts(0,5)
Magnet.SetState('OFF')
Magnet.close()
PulseBlaster1.Close()
AFG1.close()
Scope.close()
AWG1.close()
rm.close()
#-----------------------------------------------------------------------------