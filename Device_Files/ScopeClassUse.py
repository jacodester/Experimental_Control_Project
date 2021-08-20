# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:41:19 2021

@author: LocalAdmin
"""
import pyvisa
import time
import ScopeClassObjects as SO
from matplotlib import pyplot as plt
import Device_Files.AnalysisFunctionsUse as af # import useful waveform functions

rm=pyvisa.ResourceManager()

print(rm.list_resources())

Thingy1=rm.open_resource("TCPIP0::1.1.1.4::INSTR",resource_pyclass=SO.LecroyScope)
print(Thingy1.query("*IDN?"))
Info1=Thingy1.ReadInfo('M3')
Thingy1.timeout= 20000

# Example uses of methods to change the divisions, the Y offset, and some averaging
#Thingy1.SetAVG('C1',100)
#Thingy1.SetOffset('C1',-1,"VOLTS")
#Thingy1.SetVDiv('F1',0.5)
#Thingy1.SetTDiv("C1",100e-6)


# Example code to alter the trigger of the scope
#Thingy1.SetTrig('C1','AUTO',0,0.6)
#time.sleep(5)
#Thingy1.SetTrig('NORM')


# Example code to read the waveform from the scope in short syntax
time,timeunit,voltage,voltageunit=Thingy1.ReadWaveform('M3',Info1)
#Thingy1.SetNotes("")
Thingy1.WriteData('M3',"1us_pulse_input_dev10.txt")
af.MakeBaseFig(1,time,voltage, "Time", "Voltage","Yo Mamma",
                    "C:/Users/LocalAdmin/Desktop/data/Antas_MAMMA.png",close=1)



# Example of how to return the values with the read function, and then display
# the data as a plot
#Thingy1.SetSampleRate('C1',10000)
#times_out, horiz_unit_out, voltages_out, vertical_unit_out = Thingy1.ReadWaveform('F1',Info1)
#Thingy1.WriteData('F1',"10MHz Unlocked Self-Heterodyne.txt", times_out, horiz_unit_out, voltages_out, vertical_unit_out,voltages_out,vertical_unit_out)
#plt.plot(times_out, voltages_out)
#plt.show()

Thingy1.close()
rm.close()