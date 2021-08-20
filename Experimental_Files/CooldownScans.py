# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 15:51:59 2021

@author: LocalAdmin
"""
import numpy as np
import matplotlib.pyplot as plt
import time, sys, os
#import nest_asyncio
#nest_asyncio.apply()

from toptica.lasersdk.dlcpro.v2_2_0 import DLCpro, NetworkConnection, DeviceNotFoundError, DecopError, UserLevel
from toptica.lasersdk.utils.dlcpro import *
from pyBristolSCPI import *

# ------- Parameters -------
ip_toptica = '1.1.1.7'
# --------------------------


mode =  'Continuous'  # 'Single' #
xunit = 'ms'#Wavelength [nm]'# 'Frequency [GHz]'
ch1_plot, ch2_plot = False, True
force_updata_calibration = False
name_calib = "calibration_toptica_dlcpro.txt"
refresh = 30  # s
path_save = "DATA_SCAN_J"


print("DLC pro python interface")
with DLCpro(NetworkConnection(ip_toptica)) as dlcpro:
    if False:
        print(dlcpro.system_summary())

    
    if mode == 'Single':
        print("single scope aquisition")
        # Retrieve scan, lock raw data from device
        scope_data = extract_float_arrays('xyY', dlcpro.laser1.scope.data.get())

        
        ch1_available = dlcpro.laser1.scope.channel1.signal.get() != -3  # Signal is 'none'
        ch2_available = dlcpro.laser1.scope.channel2.signal.get() != -3

        fig, laxis = plt.subplots()
        fig.suptitle('DLC pro scope')

        # Set label and unit of X axis
        laxis.set_xlabel("{} [{}]".format(
            dlcpro.laser1.scope.channelx.name.get(),
            dlcpro.laser1.scope.channelx.unit.get()))

        if ch1_available and ch1_plot:
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
        if ch2_available and ch2_plot:
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

        plt.margins(x=0.0)
        plt.savefig("plot_spectrum_J.png")
        #plt.show()
    else:
        print("continuous scope aquisition")
        
        freq = dlcpro.laser1.scan.frequency.get()
        ch1_available = dlcpro.laser1.scope.channel1.signal.get() != -3  # Signal is 'none'
        ch2_available = dlcpro.laser1.scope.channel2.signal.get() != -3
        
        plt.ion()
        fig, laxis = plt.subplots()
        fig.suptitle('DLC pro scope')
        laxis.set_autoscale_on(True)
        laxis.autoscale_view(True, True, True)

        if ch1_available and ch1_plot:
            red = laxis

            # Set label and unit of left Y axis
            red.set_ylabel("{} [{}]".format(
                dlcpro.laser1.scope.channel1.name.get(),
                dlcpro.laser1.scope.channel1.unit.get()),
                color='red')

            # Plot first scope channel data
            ax1 = red.plot(
                [],
                [],
                linestyle='solid',
                color='red',
                zorder=1)
        
        # Plot second scope channel data if available
        if ch2_available and ch2_plot:
            if ch1_available:
                blue = laxis.twinx()
            else:
                blue = laxis

            blue.set_ylabel("{} [{}]".format(
                dlcpro.laser1.scope.channel2.name.get(),
                dlcpro.laser1.scope.channel2.unit.get()),
                color='blue')

            ax2 = blue.plot(
                [],
                [],
                linestyle='solid',
                color='blue',
                zorder=0)

            laxis.set_zorder(blue.get_zorder() + 1)
            laxis.patch.set_visible(False)

        plt.margins(x=0.0)
        
        global keep_loop
        keep_loop = True

        def handle_close(e):
            global keep_loop
            keep_loop = False

        fig.canvas.mpl_connect('close_event', handle_close)
        
        time_save = 0
        while keep_loop:
            
            #scope_data = extract_float_arrays('xyY', dlcpro.laser1.scope.data.get())
            laxis.set_xlabel('Time [ms]')
            '''
            if ch1_available and ch1_plot:
                #ax1[0].set_xdata(scope_data['x'])
                #ax1[0].set_ydata(scope_data['y'])
                red.relim()
                red.autoscale_view(True, True, True)
            
            if ch2_available and ch2_plot:
                #ax2[0].set_xdata(scope_data['x'])
                #ax2[0].set_ydata(scope_data['Y'])
                blue.relim()
                blue.autoscale_view(True, True, True)
            '''
            Jfile= time.strftime("%Y%m%d-%H%M%S") + "_spectrum"
            if time.time()>time_save+refresh:
                print(Jfile)
                #plt.savefig(os.path.join(path_save, Jfile))
                np.savetxt(os.path.join(path_save, Jfile)+".txt", [1, 2])
                time_save = time.time()
			
            fig.canvas.draw()
            plt.pause(0.01) #is necessary for the plot to update for some reason
    print("done.")