# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyvisa
import time
import numpy as np
from matplotlib import pyplot as plt
import TekClassObjects as TO
from scipy import signal,interpolate 
import Device_Files.WaveformFunctionsUse as wf # import useful waveform functions




#Example code for accessing the AFG functions

rm=pyvisa.ResourceManager()

print(rm.list_resources())

Thingy1=rm.open_resource("TCPIP0::1.1.1.3::INSTR",resource_pyclass=TO.AFG)


print(Thingy1.query("*IDN?"))
#Thingy1.SetPolarity('1','INV')

#Make an Arbitrary function for the function generator
'''
z=wf.SecHypePulse(7,2000,600,400,1000)
plt.plot(z)
Thingy1.set_custom_waveform(z,memory_num=4,normalise=True, print_progress=False)
Thingy1.SetFunction("2","USER4")
'''
Thingy1.SetFunction("2","GAUS")
#Thingy1.SetBurst("2","OFF")
#Thingy1.SetVoltage("1","HIGH",5)
#Thingy1.SetVoltage("1","LOW",0)
#Thingy1.write('OUTP1:STAT ON')
#Thingy1.write('SOUR1:VOLT:LEV:IMM:HIGH 3V')
#time.sleep(3)
#Thingy1.SetVoltage("1","HIGH",5)
#Thingy1.SetState("2","ON")
#time.sleep(2)
#Thingy1.SetState("2","OFF")


Thingy1.close()
rm.close()


















