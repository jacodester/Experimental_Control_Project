# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 12:56:09 2021

@author: LocalAdmin
"""
from WavemeterClassObject import *

scpi = pyBristolSCPI('1.1.1.6')
wl = scpi.readWL()
freq = scpi.readFREQ()
stuff = scpi.readALL()
print(stuff)

del scpi