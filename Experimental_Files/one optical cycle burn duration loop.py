
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

#Make and Upload Second Waveform: BURN
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


# Define NUmber of Burn Cycles, Length of each Burn, and Length of each Wait
optical_cycle = 1
# optical_cycle = np.arange(1,101,1)
waiting_time = 2000 #in us
#BurnDur=0.001 #Seconds (Light ON)
BurnDur=np.arange(0.001,0.101,0.001) # seconds (Light ON)

high = 1.5
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
#Make Scope Capture the correct window of signals
Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
Scope.SetVDiv('C1',1)   #1V/div
Scope.SetTrig('C1','SINGLE',-D1/2,1.35)
Scope.SetOffset('C2',-0.100,"VOLTS") #35mV/div
#Scope.SetOffset('C2',-0.271,"VOLTS") #100mV/div
#Scope.SetOffset('C2',-0.50,"VOLTS") #200mV/div
Scope.SetVDiv('C2',0.025)   #25mV/div
Scope.SetSampleRate('C1',100000)
Scope.SetTDiv('C2',500e-6)
Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C2')
Info2=Scope.ReadInfo('C3')
Scope.close()

Populations=[]
Populations2=[]
for step,number in enumerate (BurnDur):
    reps=int(BurnDur[step]/D2)
    # Make Sequence of the uploaded waveforms
    SEQList=[]
    SEQList.append([(WFName2,''), optical_cycle, 'BTR', reps, 0])
    SEQList.append([(WFName1,''), optical_cycle+1, 'ATR', 0, 0])
    SEQList.append([(WFName3,''), optical_cycle+2, 'OFF', 2, 1])  
    
    AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
    AWG1.write_sequence('Test1',SEQList)
    AWG1.ChannelFunc('Test1', 1, 'SEQ')
    AWG1.SetON_OFF(1,'ON')
    AWG1.SetState('RUN')
    AWG1.close()
    #-----------------------------------------------------------------------------
    #Make sure the AFG has the right settings for Hole Burning
    
    AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
    AFG1.SetFunction("1","PULS")
    AFG1.SetBurst("1","ON")
    AFG1.SetVoltage("1","HIGH",high) #V
    AFG1.SetVoltage("1","LOW",0.1)
    AFG1.SetPer("1",(D2*reps)*1000+((D2*reps)*1000)*0.01)
    AFG1.SetWidth("1",(D2*reps)*1000)
    AFG1.SetNumCyc("1",1)
    AFG1.SetState("1","ON")
    AFG1.close()
    
    #-----------------------------------------------------------------------------
    
    #Make the pulseblaster program as we so desire. 
    #-----------------------------------------------------------------------------
    PulseBlaster1.ResetProg()
    PulseBlaster1.WriteCommand([0,1], 2, 1, optical_cycle) # 1us Trigger for AFG and AWG and Loop
    PulseBlaster1.WriteCommand([], 0, D2*reps*1e6) # Do nothing for duration of Burn
    PulseBlaster1.WriteCommand([], 3, waiting_time,0)  # waiting in us and end the loop
    PulseBlaster1.WriteCommand([2,6,7], 0, D1*1e6) # Trigger 6 AWG (TrigA) for read, and 2 scope for the duration of the read pulse
    PulseBlaster1.WriteCommand([], 1, 5000) # Do Nothing now that the cycle has ended
    PulseBlaster1.ViewProg()
    
    
    #-----------------------------------------------------------------------------
    
    #wl = wavemeter.readWL()
    #freq = wavemeter.readFREQ()
    # print(wl)
    # print(freq)
    
    
    PulseBlaster1.Start()
    time.sleep((reps*waiting_time*1e-6) + 1)
    PulseBlaster1.Stop()
    Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
    times_out, horiz_unit_out, voltages_out, vertical_unit_out = Scope.ReadWaveform('C2',Info1)
    #times_out2, horiz_unit_out2, voltages_out2, vertical_unit_out2 = Scope.ReadWaveform('C3',Info2)
    freqs_out=(times_out*(sweepWidth1/D1)+ startFreq1)*1e-6
    Scope.WriteData('C2',"{}ms_burn_hole_{}cycle.txt".format(round(BurnDur[step]*1000),optical_cycle), freqs_out, 'MHz', voltages_out, vertical_unit_out, voltages_out, vertical_unit_out)
    Scope.close()
    
    # Start Analysis on the data from this trace sweep
    #-----------------------------------------------------------------------------
    voltages_out1=af.SavgolSmooth(voltages_out,51,3)
    af.MakeBaseFig(1,freqs_out, voltages_out, "Freq", "Voltage/Transmission","Burning duration:{}".format(round(BurnDur[step]*1000)),
                   "C:/Users/LocalAdmin/Desktop/data/{}ms_burn_hole_{}cycle.png".format(round(BurnDur[step]*1000),optical_cycle))  #D2*1e6*reps
    Freq_new,OD=af.CalcODRegion(freqs_out,voltages_out1,10000,149,151)
    Freq_new2,OD2=af.CalcODRegion(freqs_out,voltages_out1,10000,149.5,150.5)
    af.MakeBaseFig(2,Freq_new, OD, "Freq", "OD","Burning duration:{}".format(round(BurnDur[step]*1000)),
                   "C:/Users/LocalAdmin/Desktop/data/{}ms_burn_hole_{}cycle_OD.png".format(round(BurnDur[step]*1000),optical_cycle))
    #Depth,Width1,Inds,minInd=af.CalcHoleParam(Freq_new, OD, 149, 151, 149.2, 149.5)
    
    #diffs=np.diff(Inds[0])
    #lowInd=int(np.where(diffs[0:minInd[0][0]] > 1)[0][-1]+Inds[0][0])
    #highInd=minInd[0][0]+(minInd[0][0]-lowInd)
    Populations.append(OD)
    Populations2.append(OD2)
    
    #af.MakeBaseFig(2, Freq_new[Inds[0][0]:Inds[0][-1]], OD[Inds[0][0]:Inds[0][-1]],Filename='C:/Users/LocalAdmin/Desktop/data/')
    #af.MakeBaseFig(2, Freq_new[lowInd:highInd], OD[lowInd:highInd])

Populations=np.array(Populations)
Populations2=np.array(Populations2)
PlotName="Hole burning spectra"
fig1, ax = plt.subplots(subplot_kw={"projection": "3d"})
# Make data.
X = Freq_new
Y = BurnDur*1000
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = Populations

# Plot the surface.
surf1 = ax.plot_surface(X, Y, Z,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
#ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig1.colorbar(surf1, shrink=0.5, aspect=5)

plt.title(PlotName)
plt.xlabel("Frequency (MHz)")
plt.ylabel("Burning duration (ms)")
plt.show()
plt.savefig("C:/Users/LocalAdmin/Desktop/data/"+PlotName+".png")
PlotName1="Zoomed in Hole burning spectra"

fig2, ax = plt.subplots(subplot_kw={"projection": "3d"})
# Make data.
X = Freq_new2
Y = BurnDur*1000
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = Populations2

# Plot the surface.
surf2 = ax.plot_surface(X, Y, Z,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
#ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig2.colorbar(surf2, shrink=0.5, aspect=5)

plt.title(PlotName1)
plt.xlabel("Frequency (MHz)")
plt.ylabel("Burning duration (ms)")
plt.show()
plt.savefig("C:/Users/LocalAdmin/Desktop/data/"+PlotName1+".png")







# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
PulseBlaster1.Close()
#AFG1.close()
#Scope.close()
#AWG1.close()
rm.close()
#-----------------------------------------------------------------------------
#del wavemeter