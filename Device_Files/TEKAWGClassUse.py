# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyvisa
import time
import TekClassObjects as TO
import numpy as np
from scipy import signal 
from matplotlib import pyplot as plt
import WaveformFunctionsUse as wf 



#Example code for accessing the AFG functions

rm=pyvisa.ResourceManager()

print(rm.list_resources())

Thingy1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
Thingy1.query('*IDN?')
#Thingy1.close()


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
#AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform')
Thingy1.write_waveform(WFName1,wfmData1,MData1,MData2)
print(time.time()-start)
print('Waveform HOT  from the oven...MMMM')
#AWG1.save_Func(WFName1,'WAV')
#AWG1.close()

# #Make and Upload Second Waveform: BURN
# D2 = 100*1e-6 # specified waveform duration in sec
# P2 = wf.Points(SR,D2)
# t2=wf.Times(SR,duration=D2)
# WFName2='JHD_Hole_150MHz_100us'
# freq2= 150e6
# wfmData2 = signal.sawtooth(2*np.pi*np.multiply(freq2,t2))
# wfmData2 = wf.OptimiseWaveform(wfmData2,freq2,7)
# MData1= np.ones(len(wfmData2))
# MData2= np.ones(len(wfmData2))
# MData1[0:9]=0
# MData2[0:9]=0
# start=time.time()
# AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
# print('Keep Calm. I am uploading your waveform.')
# #AWG1.write_waveform(WFName2,wfmData2,MData1,MData2)
# print(time.time()-start)
# print('Waveform HOT from the oven...MMMM')
# #AWG1.save_Func(WFName2,'WAV')
# AWG1.close()

#Make and Upload Second Waveform: BURN
D2 = 100*1e-6 # specified waveform duration in sec
P2 = wf.Points(SR,D2)
t2=wf.Times(SR,duration=D2)
WFName2='JHD_100KHzHole_150MHz_100us'
startFreq2=149.975e6
sweepWidth2=0.05e6
freq2=wf.chirpedSawtooth(startFreq2,sweepWidth2,len(t2))
wfmData2 = signal.sawtooth(2*np.pi*np.multiply(freq2,t2))
wfmData2 = wf.OptimiseWaveform(wfmData2,freq2,7)
MData1= np.ones(len(wfmData2))
MData2= np.ones(len(wfmData2))
MData1[0:9]=0
MData2[0:9]=0
start=time.time()
#AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform.')
Thingy1.write_waveform(WFName2,wfmData2,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName2,'WAV')
#AWG1.close()

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
#AWG1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)
print('Keep Calm. I am uploading your waveform.')
Thingy1.write_waveform(WFName3,wfmData3,MData1,MData2)
print(time.time()-start)
print('Waveform HOT from the oven...MMMM')
#AWG1.save_Func(WFName3,'WAV')
#AWG1.close()

print('ESE')
print(Thingy1.query('*ESE?'))
print('SRE')
print(Thingy1.query('*SRE?'))
print('STB')
print(Thingy1.query('*STB?'))

SEQList=[]

SEQList.append([(WFName1,''), 1, 'ATR', 0, 0])
SEQList.append([(WFName2,''), 2, 'OFF', 2, 1]) 
SEQList.append([(WFName3,''), 3, 'OFF', 2, 1])  

#Thingy1=rm.open_resource("TCPIP0::1.1.1.5::INSTR",resource_pyclass=TO.AWG)

Thingy1.write_sequence('Test2',SEQList)
Thingy1.ChannelFunc('Test2', 1, 'SEQ')
Thingy1.SetON_OFF(1,'ON')
Thingy1.write('AWGC:{}:IMM'.format('RUN'))
Thingy1.write('*WAI')
print('ESE')
print(Thingy1.query('*ESE?'))
print('SRE')
print(Thingy1.query('*SRE?'))
print('STB')
print(Thingy1.query('*STB?'))
#print(Thingy1.query('*OPC?'))

# Thingy1.SetState('RUN')
#Thingy1.close()

# Example code for turning on a channel and running the active wavefrom or sequence
'''
Thingy1.SetON_OFF(1,'ON')
Thingy1.SetState('RUN')
time.sleep(2)
Thingy1.SetState('STOP')
Thingy1.SetON_OFF(1,'OFF')
'''



# Change these based on your signal requirements
'''
SR = 25e9
D = 0.000001
P = wf.Points(SR,D)
t1=wf.Times(SR,duration=D)


#freq=np.linspace(0,100e6,len(t1),dtype=np.float32)
#wfmData = signal.sawtooth(2*np.pi*np.multiply(freq,t1))
#startFreq=380e6
#sweepWidth=40e6
#freq1=wf.chirpedSawtooth(startFreq,sweepWidth,len(t1))
freq1=12e6
wfmData = signal.sawtooth(2*np.pi*np.multiply(freq1,t1))
wfmData1 = wf.OptimiseWaveform(wfmData,freq1,7)



plt.plot(t1, wfmData)
plt.show()
MData1= np.ones(len(wfmData))
MData2= np.ones(len(wfmData))
MData1[0:9]=0
MData2[0:9]=0
'''
'''
# Example Code for writing a custom waveform to the machine and saving it
WFName='JHD_12MHz_Sawtooth'
start=time.time()
print('Start Tranfser')
Thingy1.write_waveform(WFName,wfmData1,MData1,MData2)
print(time.time()-start)
Thingy1.ChannelFunc(WFName,1,'WAV')
print('Done')
#Thingy1.save_Func(WFName,'WAV')


# code for writing sequences two ways 

#Thingy1.ChannelFunc('JakeTest',1,'WAV')
#Thingy1.NewSeq('SeqNew4',2)
#Thingy1.sequence_set_waveform("SeqNew4","JakeTest",1,1)
#Thingy1.sequence_set_wait_trigger("SeqNew4",1,'BTR')
#Thingy1.sequence_set_waveform("SeqNew4","JakeTest1",2,1)
#Thingy1.sequence_set_wait_trigger("SeqNew4",2,'BTR')
#Thingy1.sequence_set_repetitions("SeqNew4", 2, 9)

#SEQList=[[('JakeTest','JakeTest1'), 1, 'BTR', 0, 0],
#         [('JakeTest1','JakeTest'), 2, 'OFF', 0, 1]
#         ]

SEQList1=[[('',''), 1, 'BTR', 1, 0],
          [('',''), 2, 'OFF', 10, 1]
         ]
Thingy1.write_sequence('Nir',SEQList1)


Thingy1.ChannelFunc('Nir', 1, 'SEQ')
Thingy1.save_Func('SeqNew4','SEQ')
time.sleep(5)
#Thingy1.DeleteSeq('SeqNew4')
'''


#Thingy1.close()

#rm.close()


















