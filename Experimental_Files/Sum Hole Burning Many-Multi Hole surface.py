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

#Make and Upload first Waveform: READ1
DRead1 = 1000*1e-6 # specified waveform duration in sec
PRead1 = wf.Points(SR,DRead1)
tRead1=wf.Times(SR,duration=DRead1)
WFRead1='JHD_Read_1148MHz_1152MHz_1ms'
startFreqRead1=1148e6
sweepWidthRead1=4e6
freqRead1=wf.chirpedSawtooth(startFreqRead1,sweepWidthRead1,len(tRead1))
wfmRead1 = signal.sawtooth(2*np.pi*np.multiply(freqRead1,tRead1))
wfmRead1 = wf.OptimiseWaveform(wfmRead1,freqRead1,7)
MData1= np.ones(len(wfmRead1))
MData2= np.ones(len(wfmRead1))
MData1[0:1]=0
MData2[0:1]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform')
AWG1.write_waveform(WFRead1,wfmRead1,MData1,MData2)
print(time.time()-start)
print('Waveform HOT  from the oven...MMMM')
#AWG1.save_Func(WFName1,'WAV')
AWG1.close()

#Make and Upload first Waveform: READ2
DRead2 = 1000*1e-6 # specified waveform duration in sec
PRead2 = wf.Points(SR,DRead2)
tRead2=wf.Times(SR,duration=DRead2)
WFRead2='JHD_Read_1152MHz_1156MHz_1ms'
startFreqRead2=1152e6
sweepWidthRead2=4e6
freqRead2=wf.chirpedSawtooth(startFreqRead2,sweepWidthRead2,len(tRead2))
wfmRead2 = signal.sawtooth(2*np.pi*np.multiply(freqRead2,tRead2))
wfmRead2 = wf.OptimiseWaveform(wfmRead2,freqRead2,7)
MData1= np.ones(len(wfmRead2))
MData2= np.ones(len(wfmRead2))
#MData1[0:1]=0
#MData2[0:1]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform')
AWG1.write_waveform(WFRead2,wfmRead2,MData1,MData2)
print(time.time()-start)
print('Waveform HOT  from the oven...MMMM')
#AWG1.save_Func(WFName1,'WAV')
AWG1.close()

#Make and Upload first Waveform: READ3
DRead3 = 1000*1e-6 # specified waveform duration in sec
PRead3 = wf.Points(SR,DRead3)
tRead3=wf.Times(SR,duration=DRead3)
WFRead3='JHD_Read_1156MHz_1160MHz_1ms'
startFreqRead3=1156e6
sweepWidthRead3=4e6
freqRead3=wf.chirpedSawtooth(startFreqRead3,sweepWidthRead3,len(tRead3))
wfmRead3 = signal.sawtooth(2*np.pi*np.multiply(freqRead3,tRead3))
wfmRead3 = wf.OptimiseWaveform(wfmRead3,freqRead3,7)
MData1= np.ones(len(wfmRead3))
MData2= np.ones(len(wfmRead3))
#MData1[0:1]=0
#MData2[0:1]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform')
AWG1.write_waveform(WFRead3,wfmRead3,MData1,MData2)
print(time.time()-start)
print('Waveform HOT  from the oven...MMMM')
#AWG1.save_Func(WFName1,'WAV')
AWG1.close()

#Make and Upload first Waveform: READ4
DRead4 = 1000*1e-6 # specified waveform duration in sec
PRead4 = wf.Points(SR,DRead4)
tRead4=wf.Times(SR,duration=DRead4)
WFRead4='JHD_Read_1160MHz_1164MHz_1ms'
startFreqRead4=1160e6
sweepWidthRead4=4e6
freqRead4=wf.chirpedSawtooth(startFreqRead4,sweepWidthRead4,len(tRead4))
wfmRead4 = signal.sawtooth(2*np.pi*np.multiply(freqRead4,tRead4))
wfmRead4 = wf.OptimiseWaveform(wfmRead4,freqRead4,7)
MData1= np.ones(len(wfmRead4))
MData2= np.ones(len(wfmRead4))
#MData1[0:1]=0
#MData2[0:1]=0
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform')
AWG1.write_waveform(WFRead4,wfmRead4,MData1,MData2)
print(time.time()-start)
print('Waveform HOT  from the oven...MMMM')
#AWG1.save_Func(WFName1,'WAV')
AWG1.close()

# specified the DC delay
DDC =10*1e-6 # specified waveform duration in sec 
PDC = wf.Points(SR,DDC)
tDC=wf.Times(SR,duration=DDC)
WFNameDC='JHD_Delay_1ms'
wfmDataDC = np.ones(len(tDC))
MData1= np.ones(len(wfmDataDC))
MData2= np.ones(len(wfmDataDC))
start=time.time()
AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform Master.')
AWG1.write_waveform(WFNameDC,wfmDataDC,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName3,'WAV')
AWG1.close()

Factors=np.arange(0.1,1.1,0.1)
Durations=np.arange(1*1e-4,1.05*1e-3,1*1e-4)
Holes=[1149, 1150, 1151, 1153, 1154, 1155, 1157, 1158, 1159, 1161]
WFNames=[]
Ilist=[]
for i,factor in enumerate(Factors):
    Jlist=[]
    for j,dur in enumerate(Durations):
        DMultiHole = dur # specified waveform duration in sec
        PMultiHole = wf.Points(SR,DMultiHole)
        tMultiHole=wf.Times(SR,duration=DMultiHole)
        wfmDataMultiHole=np.zeros(len(tMultiHole))
        for value in Holes:
            #Make and Upload Second Waveform: BURN1
            DSingleHole = dur # specified waveform duration in sec
            PSingleHole = wf.Points(SR,DSingleHole)
            tSingleHole=wf.Times(SR,duration=DSingleHole)
            #WFName2='JHD_Hole_149MHz_1us'
            wfmDataSingleHole = signal.sawtooth(2*np.pi*np.multiply(value*1e6,tSingleHole))
            wfmDataSingleHole = wf.OptimiseWaveform(wfmDataSingleHole,value*1e6,7)
            wfmDataMultiHole = np.add(wfmDataMultiHole,wfmDataSingleHole)
    
        
        wfmDataMultiHole=np.multiply(wfmDataMultiHole,factor)
        
        MData1= np.ones(len(wfmDataMultiHole))
        MData2= np.ones(len(wfmDataMultiHole))
        MData1[0:9]=0
        MData2[0:9]=0
        
        WFMultiHole='JHD_Hole_149,150,151MHz_Factor{}_Dur{}'.format(factor,'{:0.2e}'.format(dur))
        WFNames.append(WFMultiHole)
        Jlist.append(WFMultiHole)
        start=time.time()
        AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
        print('Keep Calm. I am uploading your waveform.')
        AWG1.write_waveform(WFMultiHole,wfmDataMultiHole,MData1,MData2)
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
Scope.SetTrig('C1','SINGLE',-(DRead1+DRead2+DRead3+DRead4)*5/8,0.35)
Scope.SetOffset('C2',-0.10,"VOLTS")
Scope.SetVDiv('C2',0.1)
Scope.SetSampleRate('C1',100000)
Scope.SetTDiv('C2',500e-6)
Scope.SetNotes("On Resonance hole burning with different waveforms to optimize")
Info1=Scope.ReadInfo('C2')
Info2=Scope.ReadInfo('C3')
Scope.close()
#-----------------------------------------------------------------------------
Holedepths=[]
for i in range(len(Holes)):
    Holedepths.append(np.zeros((len(WFNames),len(WFNames[0]))))



for i in range(len(WFNames)):
    for j in range(len(WFNames[0])):
        #Make the pulseblaster program as we so desire. 
        #-----------------------------------------------------------------------------
        PulseBlaster1.ResetProg()
        #PulseBlaster1.ViewProg()
        PulseBlaster1.WriteCommand([0,1], 0, 1) #SF and AFG
        PulseBlaster1.WriteCommand([], 0, total*1e6) 
        PulseBlaster1.WriteCommand([], 0, 15000)  #waiting in us
        PulseBlaster1.WriteCommand([0,2], 0, (DRead1+DRead2+DRead3+DRead4)*1e6) #SF and Scope
        PulseBlaster1.WriteCommand([], 1, 5000)
        PulseBlaster1.WriteProg()
        
        #-----------------------------------------------------------------------------
        
        
        reps=total/(DMultiHole)
        # Make Sequence of the uploaded waveforms
        SEQList=[[(WFNames[i][j],''), 1, 'BTR', round(reps), 0],
                 [(WFRead1,''), 2, 'BTR', 0, 0],
                 [(WFRead2,''), 3, 'OFF', 0, 0],
                 [(WFRead3,''), 4, 'OFF', 0, 0],
                 [(WFRead4,''), 5, 'OFF', 0, 0],
                 [(WFNameDC,''), 6, 'OFF', 200, 1]
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
        freqs_out=(times_out*(sweepWidthRead1/DRead1)+ startFreqRead1)*1e-6
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
        
        indices = [idx for idx,val in enumerate(freqs_out) if val > (((startFreqRead1*1e-6)+0.02))]
        
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
        
        
        for freq in range(len(Holes)):
            indices = [idx for idx,val in enumerate(Freq_new) if (val > Holes[freq]-0.5 and val < Holes[freq]+0.5)]
            Holedepths[freq][i][j]=np.amax(OD[indices[0]:indices[-1]]) - np.amin(OD[indices[0]:indices[-1]])
       
        
        time.sleep(1)
        AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
        AWG1.timeout=20000
        AWG1.SetState('STOP')
        AWG1.SetON_OFF(1,'OFF')
        AWG1.close()

PlotName="100pt_Summed_Surface_0-1_100us-1ms"


for freq in range(len(Holes)):
    np.savetxt("C:/Users/LocalAdmin/Desktop/data/"+PlotName+"{}.txt".format(freq+1),Holedepths[freq])
    np.save("C:/Users/LocalAdmin/Desktop/data/binary{}".format(freq+1),Holedepths[freq])


    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    
    # Make data.
    X = Factors
    Y = Durations
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = Holedepths[freq]
    
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z,cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    
    # Customize the z axis.
    #ax.set_zlim(-1.01, 1.01)
    #ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    #ax.zaxis.set_major_formatter('{x:.02f}')
    
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
    plt.title(PlotName + "Hole {}".format(freq+1))
    plt.xlabel("Norm Factors")
    plt.ylabel("WF Duration")
    plt.show()
    plt.savefig("C:/Users/LocalAdmin/Desktop/data/"+PlotName+"{}.png".format(freq+1))



# Section of graceful disconnection from different device objects
#-----------------------------------------------------------------------------
PulseBlaster1.Close()
rm.close()
#-----------------------------------------------------------------------------
