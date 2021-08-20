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

Factors=np.arange(0.1,1.1,0.1)
Durations=np.arange(1*1e-4,1.05*1e-3,1*1e-4)

WFNames=[]
Ilist=[]
for i,factor in enumerate(Factors):
    Jlist=[]
    for j,dur in enumerate(Durations):
        
        #Make and Upload Second Waveform: BURN1
        D2 = dur # specified waveform duration in sec
        P2 = wf.Points(SR,D2)
        t2=wf.Times(SR,duration=D2)
        #WFName2='JHD_Hole_149MHz_1us'
        freq2= 149e6
        wfmData2 = signal.sawtooth(2*np.pi*np.multiply(freq2,t2))
        wfmData2 = wf.OptimiseWaveform(wfmData2,freq2,7)

        #Make and Upload Second Waveform: BURN2
        D3 = dur # specified waveform duration in sec
        P3 = wf.Points(SR,D3)
        t3=wf.Times(SR,duration=D3)
        #WFName3='JHD_Hole_151MHz_1us'
        freq3= 151e6
        wfmData3 = signal.sawtooth(2*np.pi*np.multiply(freq3,t3))
        wfmData3 = wf.OptimiseWaveform(wfmData3,freq3,7)
        
        #Make and Upload Second Waveform: BURN3
        D6 = dur # specified waveform duration in sec
        P6 = wf.Points(SR,D6)
        t6=wf.Times(SR,duration=D6)
        #WFName3='JHD_Hole_151MHz_1us'
        freq6= 150e6
        wfmData6 = signal.sawtooth(2*np.pi*np.multiply(freq6,t6))
        wfmData6 = wf.OptimiseWaveform(wfmData6,freq6,7)
    
        D5=D2
        wfmData5=np.multiply(np.add(np.add(wfmData2,wfmData3),wfmData6),factor)
        MData1= np.ones(len(wfmData5))
        MData2= np.ones(len(wfmData5))
        MData1[0:9]=0
        MData2[0:9]=0
        WFName5='JHD_Hole_149,150,151MHz_Factor{}_Dur{}'.format(factor,'{:0.2e}'.format(dur))
        WFNames.append(WFName5)
        Jlist.append(WFName5)
        start=time.time()
        AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
        print('Keep Calm. I am uploading your waveform.')
        AWG1.write_waveform(WFName5,wfmData5,MData1,MData2)
        print(time.time()-start)
        print('Waveform HOT from the oven...MMMM')
        #AWG1.save_Func(WFName5,'WAV')
        AWG1.close()
    Ilist.append(Jlist)
WFNames=Ilist

total=2e-3
#Make sure the AFG has the right settings for Hole Burning
#-----------------------------------------------------------------------------
AFG1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)
AFG1.SetFunction("1","PULS")
AFG1.SetBurst("1","ON")
AFG1.SetVoltage("1","HIGH",5) #V
AFG1.SetVoltage("1","LOW",0.7)
AFG1.SetPer("1",(total)*1000+5)
AFG1.SetWidth("1",(total)*1000)
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

holedepths1=np.zeros((len(WFNames),len(WFNames[0])))
holedepths2=np.zeros((len(WFNames),len(WFNames[0])))
holedepths3=np.zeros((len(WFNames),len(WFNames[0])))
for i in range(len(WFNames)):
    for j in range(len(WFNames[0])):
        #Make the pulseblaster program as we so desire. 
        #-----------------------------------------------------------------------------
        PulseBlaster1.ResetProg()
        #PulseBlaster1.ViewProg()
        PulseBlaster1.WriteCommand([0,1], 0, 1) #SF and AFG
        PulseBlaster1.WriteCommand([], 0, total*1e6) 
        PulseBlaster1.WriteCommand([], 0, 15000)  #waiting in us
        PulseBlaster1.WriteCommand([0,2], 0, D1*1e6) #SF and Scope
        PulseBlaster1.WriteCommand([], 1, 5000)
        PulseBlaster1.WriteProg()
        
        #-----------------------------------------------------------------------------
        
        
        reps=total/(D5)
        # Make Sequence of the uploaded waveforms
        SEQList=[[(WFNames[i][j],''), 1, 'BTR', round(reps), 0],
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
    
    

        FileName=WFNames[i][j]
        Scope=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
        Scope.timeout=200000
        PulseBlaster1.Start()
        time.sleep(1)
        PulseBlaster1.Stop()
        times_out, horiz_unit_out, voltages_out, vertical_unit_out = Scope.ReadWaveform('C2',Info1)
        #times_out2, horiz_unit_out2, voltages_out2, vertical_unit_out2 = Scope.ReadWaveform('C3',Info2)
        freqs_out=(times_out*(sweepWidth1/D1)+ startFreq1)*1e-6
        Scope.WriteData('C2',FileName +".txt", freqs_out, 'MHz', voltages_out, vertical_unit_out, voltages_out, vertical_unit_out)
        Scope.close()
        
    
    
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
        plt.close()
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
        plt.close()
        
        indices1 = [idx1 for idx1,val1 in enumerate(Freq_new) if (val1 > 150.5 and val1 < 151.5)]
        indices2 = [idx2 for idx2,val2 in enumerate(Freq_new) if (val2 > 148.5 and val2 < 149.5)]
        indices3 = [idx3 for idx3,val3 in enumerate(Freq_new) if (val3 > 149.5 and val3 < 150.5)]
        Hole1OD = np.amax(OD[indices2[0]:indices2[-1]]) - np.amin(OD[indices2[0]:indices2[-1]])
        Hole2OD = np.amax(OD[indices1[0]:indices1[-1]]) - np.amin(OD[indices1[0]:indices1[-1]])
        Hole3OD = np.amax(OD[indices3[0]:indices3[-1]]) - np.amin(OD[indices3[0]:indices3[-1]])
        holedepths1[i][j]=Hole1OD
        holedepths2[i][j]=Hole2OD
        holedepths3[i][j]=Hole3OD
        
        
        time.sleep(1)
        AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
        AWG1.timeout=20000
        AWG1.SetState('STOP')
        AWG1.SetON_OFF(1,'OFF')
        AWG1.close()

PlotName="100pt_Summed_Surface_0-1_100us-1ms"
np.savetxt("C:/Users/LocalAdmin/Desktop/data/"+PlotName+".txt",holedepths1)
np.save("C:/Users/LocalAdmin/Desktop/data/binary1",holedepths1)
np.save("C:/Users/LocalAdmin/Desktop/data/binary2",holedepths2)
np.save("C:/Users/LocalAdmin/Desktop/data/binary3",holedepths3)


fig1, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = Factors
Y = Durations
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = holedepths1

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

plt.title(PlotName + " Hole 1")
plt.xlabel("Norm Factors")
plt.ylabel("WF Duration")
plt.show()
plt.savefig("C:/Users/LocalAdmin/Desktop/data/"+PlotName+"1.png")

fig2, bx = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = Factors
Y = Durations
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = holedepths2

# Plot the surface.
surf2 = bx.plot_surface(X, Y, Z,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
#ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig2.colorbar(surf2, shrink=0.5, aspect=5)

plt.title(PlotName + " Hole 2")
plt.xlabel("Norm Factors")
plt.ylabel("WF Duration")
plt.show()
plt.savefig("C:/Users/LocalAdmin/Desktop/data/"+PlotName+"2.png")

fig3, cx = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = Factors
Y = Durations
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = holedepths3

# Plot the surface.
surf3 = cx.plot_surface(X, Y, Z,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
#ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig3.colorbar(surf3, shrink=0.5, aspect=5)

plt.title(PlotName + " Hole 3")
plt.xlabel("Norm Factors")
plt.ylabel("WF Duration")
plt.show()
plt.savefig("C:/Users/LocalAdmin/Desktop/data/"+PlotName+"3.png")

# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
PulseBlaster1.Close()
rm.close()
#-----------------------------------------------------------------------------
