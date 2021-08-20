# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 15:16:55 2021

@author: LocalAdmin
"""
# Must have to run an event loop for this device. 
import nest_asyncio
nest_asyncio.apply()

import time

from toptica.lasersdk.dlcpro.v2_2_0 import DLCpro, NetworkConnection, DeviceNotFoundError, DecopError, UserLevel
from toptica.lasersdk.utils.dlcpro import *
from toptica.lasersdk.client import Client, NetworkConnection

def main():
    with DLCpro(NetworkConnection('1.1.1.7')) as dlc:
        amp = dlc.laser1.scan.amplitude.get()
        offset = dlc.laser1.scan.offset.get()
        #dlc.laser1.dl.cc.enabled.set(bool(1))
        dlc.laser1.scan.offset.set(105.000)
        offset = dlc.laser1.scan.offset.get()
        print(offset)
        dlc.laser1.scan.offset.set(108.731)
        offset = dlc.laser1.scan.offset.get()
        print(offset)
        return dlc.close()
    
def main2():
    with Client(NetworkConnection('1.1.1.7')) as dlc:
        amp = dlc.get('laser1:scan:amplitude')
        offset = dlc.get('laser1:scan:offset')
        dlc.set("laser1:scan:offset", 108.731)
        offset = dlc.get('laser1:scan:offset')
        #offset = dlc.laser1.scan.offset.get()
        print(offset)
        #dlc.laser1.scan.offset.set(108.731)
        #offset = dlc.laser1.scan.offset.get()
        print(amp)
        return dlc.close()
def main3():
        dlc = Client(NetworkConnection('1.1.1.7'))
        #amp = dlc.get('laser1:scan:amplitude')
        #offset = dlc.get('laser1:scan:offset')
        #dlc.set("laser1:scan:offset", 108.731)
        #offset = dlc.get('laser1:scan:offset')
        #offset = dlc.laser1.scan.offset.get()
        #print(offset)
        #dlc.laser1.scan.offset.set(108.731)
        #offset = dlc.laser1.scan.offset.get()
        #print(amp)
        return dlc.close()
    
if __name__=="__main__":
     main2()
     dlc = Client(NetworkConnection('1.1.1.7'))
     amp = dlc.get('laser1:scan:amplitude')
     #offset = dlc.get('laser1:scan:offset')
     #dlc.set("laser1:scan:offset", 108.731)
     #offset = dlc.get('laser1:scan:offset')
     #offset = dlc.laser1.scan.offset.get()
     #print(offset)
     #dlc.laser1.scan.offset.set(108.731)
     #offset = dlc.laser1.scan.offset.get()
     #print(amp)
     dlc.close()
     print('I Ended')
    
    
    

