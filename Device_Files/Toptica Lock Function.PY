import sys
import asyncio
import nest_asyncio
import time
nest_asyncio.apply()

import matplotlib.pyplot as pyplot
import numpy as np

from toptica.lasersdk.dlcpro.v2_2_0 import DLCpro, NetworkConnection, DeviceNotFoundError
from toptica.lasersdk.utils.dlcpro import *


def Lock_Me(dlcpro,amp):
     ampInitial = dlcpro.laser1.scan.amplitude.get()
     
     # Do an initial wide scan of the frequencies and get the rough lock point
     offsetInitial = dlcpro.laser1.scan.offset.get()
     
     dlcpro.laser1.scan.amplitude.set(amp)
     #asyncio.sleep(5)
     scope_data = avgTraces(dlcpro,5) #extract_float_arrays('xyY', dlcpro.laser1.scope.data.get())
     SR=amp/(scope_data['x'][-1]) # gives a sweep rate in V/ms
     maxErrIndex=np.argmax(scope_data['y']) #scope_data['Y'].index(max(scope_data['Y'])) # find max index of error signal
     timeMaxErr=scope_data['x'][maxErrIndex] # use this index to find a time in ms. 
     print(timeMaxErr)
     offsetNeeded=SR*timeMaxErr-(0.5*amp)
     print(offsetNeeded)
     offsetFinal=offsetInitial+offsetNeeded
     print(offsetInitial)
     print(offsetFinal)
     dlcpro.laser1.scan.offset.set(offsetFinal)
     return
 
    
def avgTraces(dlcpro, numavgs):
     scope_data= extract_float_arrays('xyY', dlcpro.laser1.scope.data.get())
     datxInit = scope_data['x']
     daty1Init = scope_data['y']
     daty2Init = scope_data['Y']
     datx = scope_data['x'][0:]
     daty1 = scope_data['y'][0:]
     daty2 = scope_data['Y'][0:]
     for i in range(numavgs-1):
         scope_data = extract_float_arrays('xyY', dlcpro.laser1.scope.data.get())
         datx = np.add(datx[0:],scope_data['x'][0:])
         daty1 = np.add(daty1[0:],scope_data['y'][0:])
         daty2 = np.add(daty2[0:],scope_data['Y'][0:])
     scope_data['x'] = np.divide(datx,numavgs)
     scope_data['y'] = np.divide(daty1,numavgs)
     scope_data['Y'] = np.divide(daty2,numavgs)
     return scope_data
    
    
def main():
    try:
        with DLCpro(NetworkConnection('1.1.1.7')) as dlcpro:
            # Retrieve scan, lock raw data from device
            Lock_Me(dlcpro,5.000)
            #Lock_Me(dlcpro,3.000)
            #Lock_Me(dlcpro,1.000)
            #avg_Data = avgTraces(dlcpro,5)
            #scope_data = extract_float_arrays('xyY', dlcpro.laser1.scope.data.get())
            scope_data = avgTraces(dlcpro,10)
            raw_lock_candidates = dlcpro.laser1.dl.lock.candidates.get()
            lock_candidates = extract_lock_points('clt', raw_lock_candidates)
            lock_state = extract_lock_state(raw_lock_candidates)
            scanFreq=dlcpro.laser1.scan.frequency.get()
            health=dlcpro.system_health_txt.get()
            #print(scope_data)
            
            # Create double y axis plot
            fig, laxis = pyplot.subplots()
            fig.suptitle('DLC pro Scope Output')

            ch1_available = dlcpro.laser1.scope.channel1.signal.get() != -3  # Signal is 'none'
            ch2_available = dlcpro.laser1.scope.channel2.signal.get() != -3

            # Set label and unit of X axis
            laxis.set_xlabel("{} [{}]".format(
                dlcpro.laser1.scope.channelx.name.get(),
                dlcpro.laser1.scope.channelx.unit.get()))

            if ch1_available:
                red = laxis

                # Set label and unit of left Y axis
                red.set_ylabel("{} [{}]".format(
                    dlcpro.laser1.scope.channel1.name.get(),
                    dlcpro.laser1.scope.channel1.unit.get()),
                    color='red')

                # Plot first scope channel data
                red.plot(
                    scope_data['x'],
                    scope_data['y'],
                    linestyle='solid',
                    color='red',
                    zorder=1)
            # Plot second scope channel data if available
            if ch2_available:
                if ch1_available:
                    blue = laxis.twinx()
                else:
                    blue = laxis

                blue.set_ylabel("{} [{}]".format(
                    dlcpro.laser1.scope.channel2.name.get(),
                    dlcpro.laser1.scope.channel2.unit.get()),
                    color='blue')

                blue.plot(
                    scope_data['x'],
                    scope_data['Y'],
                    linestyle='solid',
                    color='blue',
                    zorder=0)

                laxis.set_zorder(blue.get_zorder() + 1)
                laxis.patch.set_visible(False)

            pyplot.margins(x=0.0)
            pyplot.show()
            
    except DeviceNotFoundError:
        sys.stderr.write('Device not found')


if __name__ == "__main__":
    main()
