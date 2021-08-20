# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 10:18:28 2021

@author: LocalAdmin
"""

import pyvisa
import AttocubeClassObject as AO
import time

rm = pyvisa.ResourceManager()
print(rm.list_resources())

#Thingy1=RM.open_resource('ASRL4::INSTR',resource_pyclass=AO.Attocube)
        