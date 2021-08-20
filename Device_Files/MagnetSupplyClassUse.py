# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 11:08:03 2021

@author: LocalAdmin
"""
import pyvisa
import MagnetSupplyClassObjects as MO
import time
#Example code for accessing the AFG functions

rm=pyvisa.ResourceManager()
Magnet=rm.open_resource('GPIB0::9::INSTR',resource_pyclass=MO.MagnetSupply)
print(Magnet.query('*IDN?'))
#value=Magnet.UpdateField()


# Eample code for setting the state of a magnet and ramping the field up to 
# a particular value, waiting for a key press, and then ramping back down. 
print(Magnet.GetState())
print(Magnet.GetLevel())
mags=Magnet.GetLevel()
Magnet.SetState('ON')
#time.sleep(5)
#Magnet.SetState('ON')
Magnet.SetVolts(5,1) #(V,sec)
Magnet.SetCurrent(0,60) #(Amps=kG, sec)
#print(Magnet.GetLevel())
Magnet.SetState('OFF')

#print(Magnet.GetState())

#Magnet.SetVolts(2,2)
#print(Magnet.GetLevel())
#Magnet.SetCurrent(0.1,5)
#print(Magnet.GetLevel())
#input("Please press a key to continue.")

#print(Magnet.GetLevel())
#time.sleep(2)
#Magnet.SetCurrent(4.0,30)
#Magnet.SetVolts(0,20)
#Magnet.SetState('OFF')




Magnet.close()
rm.close()