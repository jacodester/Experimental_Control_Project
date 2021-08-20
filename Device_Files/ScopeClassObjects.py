# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:42:06 2021

@author: LocalAdmin
"""
import pyvisa
import struct
import numpy
#import os
#import errno

class LecroyScope(pyvisa.resources.TCPIPInstrument):
    
    def __init__(self,*args,**kwargs):
        """
        Initialize parameters in the class object, that we will change in
        the class methods later

        Returns
        -------
        None.

        """
        super(LecroyScope,self).__init__(*args,**kwargs)
        
        self.filename=""
        self.channel='C1'
        self.path="C:/Users/LocalAdmin/Desktop/data/" + "" #+ self.filename
        self.lastTimes=""
        self.lastVolts=""
        self.lastTimesUnit=""
        self.lastVoltsUnit=""
        self.lastInfo=""
        self.Notes=""
    
        #self.ChannelDesc = self.ReadInfo(self.channel)
        
    def SetFileName(self,name):
        """
        Sets internal object filename if you need to save the same object data
        differently

        Parameters
        ----------
        name : str
            Name of the current file to be saved

        Returns
        -------
        None.

        """
        
        self.filename=name
        return 
    
    def ReadInfo(self,ch):
        """
        Reads channel info to generate the correct library of terms describing 
        the channel. Must be generated before reading the waveform data and 
        writing it to  a file.

        Parameters
        ----------
        ch : str
            input has to be=  'F1','F2','F3'..... for MATH functions.in the 1GHz scopes can also be TA,TB,TC,TD (instead of F1,F2,F3,F4)
                              'C1','C2,'C3'..... for Channels
                              'M1','M2','M3'..... for memories

        Returns
        -------
        wf_desc : dictionary
            a dictionary of information about the channel of interest
            this dictionary includes the channel units so it is important to 
            keep this information updated

        """
        
        wf_desc = dict()
        wf_desc_raw = self.query('{}:INSPECT? WAVEDESC'.format(ch))
        wf_desc_lines = wf_desc_raw.split('\r\n')[1:-1]

        for line in wf_desc_lines:
            params = [field.strip() for field in line.split(':')]
            wf_desc.update({params[0]: params[1]})
        self.lasInfo=wf_desc
        return wf_desc
        
    def ReadWaveform(self,channel,info=None):
        """
        Reads the current waveform on the scope for the specified channel. User
        should include the channel info dictionary from a run of the ReadInfo()
        function on the same channel just before use. If this is not done, the 
        channel info will default to the last used channel. 

        Parameters
        ----------
        ch : str
            input has to be=  'F1','F2','F3'..... for MATH functions.in the 1GHz scopes can also be TA,TB,TC,TD (instead of F1,F2,F3,F4)
                              'C1','C2,'C3'..... for Channels
                              'M1','M2','M3'..... for memories
        info : dictionary, optional
            a dictionary of information about the channel of interest
            this dictionary includes the channel units so it is important to 
            keep this information updated
            DESCRIPTION. The default is None.

        Returns
        -------
        This function returns the data to be read, but also updates the objects
        last read parameters so that they are easy to access from later statements
        
        times : array of float64
            list of times that represent the x axis of the scope waveform.
        horiz_unit : str
            unit name string for the x scop axis
        voltages : array of float 64
            list of voltages that represent the y axis values of the indicated
            waveform
        vertical_unit : str
            unit name string for the y scop axis

        """
        if(info is None):
            info=self.lastInfo
        #   Returns lists containing the corresponding times and voltages of the waveform.

        # Force single acquisition
        #self.write('TRMD STOP;ARM;FRTR')
        self.query("*OPC?")
        self.write('{}:WF? DAT1'.format(channel))


        wf_raw = self.read_raw()
        wf_data_raw = wf_raw[22:-1] # skip header and newline



        # raw data --> list of signed integers
        ndatapoints = len(wf_data_raw)
        wf_data_array = struct.unpack('{0}b'.format(ndatapoints), wf_data_raw)


        # derive actual measured values with correct units
        vertical_gain = float(info['VERTICAL_GAIN'])
        vertical_offset = float(info['VERTICAL_OFFSET'])
        vertical_unit = info['VERTUNIT']
        horiz_interval = float(info['HORIZ_INTERVAL'])
        horiz_offset = float(info['HORIZ_OFFSET'])
        horiz_unit = info['HORUNIT']

        times = numpy.arange(ndatapoints) * round(horiz_interval,10) + round(horiz_offset,10)
        voltages = numpy.array(wf_data_array) * vertical_gain - vertical_offset
        
        self.write('TRMD NORM')
        self.query('*OPC?')
        self.lastTimes=times
        self.lastVolts=voltages
        self.lastTimesUnit=horiz_unit
        self.lastVoltsUnit=vertical_unit
        self.Notes=""
        self.trigVolt=0
        return times, horiz_unit, voltages, vertical_unit
        
    
    def SetNotes(self, Notes):
        """
        Inlcudes a small experimental note of text at the beginning of the 
        oobjects save file to include information about the saved waveform

        Parameters
        ----------
        Notes : str
            string to be included in the saved CSV file

        Returns
        -------
        None.

        """
        self.Notes=Notes
        return
    
    def WriteData(self,channel,name=None,times=None, hor_unit=None, volt=None, vert_unit=None,volt2=None, vert_unit2=None):
        """
        Function writes the data from the either the specified arrays, or from
        the last read of the scope object to a text file with specified CSV 
        formatting. 

        Parameters
        ----------
        channel : str
            input has to be=  'F1','F2','F3'..... for MATH functions.in the 1GHz scopes can also be TA,TB,TC,TD (instead of F1,F2,F3,F4)
                              'C1','C2,'C3'..... for Channels
                              'M1','M2','M3'..... for memories
        name : str, optional
            Filename for the data that is to be saved. The default is the same
            name as the last saved file, so data will be over written.
        times : array of float64
            list of times that represent the x axis of the scope waveform. Default
            is the last array of data generated by the ReadWaveform() function
        horiz_unit : str
            unit name string for the x scop axis. Default is the last unit string generated by the ReadWaveform() function
        voltages : array of float 64
            list of voltages that represent the y axis values of the indicated
            waveform.Default is the last array of data generated by the ReadWaveform() function
        vertical_unit : str
            Default is the last unit string generated by the ReadWaveform() function

        Returns
        -------
        None.

        """
        if (name is None):
            name=self.filename
        else:
            self.filename=name
        #if not os.path.exists(os.path.dirname(file_path('50us'))):
        #    try:
        #        os.makedirs(os.path.dirname(file_path('50us')))
        #    except OSError as exc:  # Guard against race condition
        #        if exc.errno != errno.EEXIST:
        #           raise
        if  ((times is None) & (volt is None)):
            with open(self.path + self.filename, "w") as f:
                f.write(channel + "\n\n")
                f.write(self.Notes)
                f.write("\n\n")
                f.write(str(self.lastTimesUnit) + ";" +str(self.lastVoltsUnit) + ";\n")
                for x in range(len(self.lastTimes[:])):
                    f.write(str(self.lastTimes[x]) + ";"+str(self.lastVolts[x]) + ";\n")
        else:
            with open(self.path + self.filename, "w") as f:
                f.write(channel + "\n\n")
                f.write(self.Notes)
                f.write("\n\n")
                f.write(str(hor_unit) + ";" + str(vert_unit) + ";" + str(vert_unit2) + ";\n")
                for x in range(len(times[:])):
                    f.write(str(times[x]) + ";" + str(volt[x])+ ";" + str(volt2[x])+";\n")
        return

    def SetVDiv(self,channel,level):
        """
        Set vertical scale for the given channel

        Parameters
        ----------
        channel : str
            input has to be=  'F1','F2','F3'..... for MATH functions.in the 1GHz scopes can also be TA,TB,TC,TD (instead of F1,F2,F3,F4)
                              'C1','C2,'C3'..... for Channels
                              'M1','M2','M3'..... for memories
        level : double
            Scale for the specified channel in Volts/Div
        Returns
        -------
        int
            Returns the result of the *OPC? query

        """
        self.write("{}:VDIV {}V".format(channel,level))
        return self.query('*OPC?')
    
    def SetTDiv(self,channel,timediv):
        """
        Set horrizontal scale for the given channel, but this will affect the 
        whole instrument

        Parameters
        ----------
        channel : str
            input has to be=  'F1','F2','F3'..... for MATH functions.in the 1GHz scopes can also be TA,TB,TC,TD (instead of F1,F2,F3,F4)
                              'C1','C2,'C3'..... for Channels
                              'M1','M2','M3'..... for memories
        timediv : double
            Scale for the specified channel in seconds/Div
        Returns
        -------
        int
            Returns the result of the *OPC? query

        """
        self.write("{}:TDIV {}".format(channel,timediv))
        return self.query('*OPC?')

    def SetTrig(self,channel,trigmode,delay=0,voltage=None):
        """
        

        Parameters
        ----------
        channel : str
            input has to be = C1','C2,'C3'..... for Channel to trigger from
                              
        trigmode : str
            One of the strings 'AUTO'
                               'NORM'
                               'SINGLE'
                               'STOP'
        delay : double, optional
            a delay from the trigger in seconds.Essentially the horizontal 
            offset of the scope. The default is 0.
        voltage : double, optional
            trigger voltage level. If supplied the trigger level for the specified
            channel will change. If not supplied the previous trigger level will
            be maintained. 

        Returns
        -------
         int
            Returns the result of the *OPC? query

        """
        if (voltage is None ):
            voltage=self.trigVolt
        else:
            self.trigVolt=voltage
        self.write("TRSE EDGE,SR,{}".format(channel))
        self.write('{}:TRLV {}V'.format(channel,voltage))
        if (len(trigmode) == 0):
            self.write('TRMD STOP;ARM;FRTR')
            return self.query("*OPC?")
        else:
            self.write('TRMD {}'.format(trigmode))
            self.write('TRDL {}S'.format(delay))
            return self.query("*OPC?")
        return self.query('*OPC?')
    
    def SetOffset(self,channel,offset, mode):
        """
         Set the voltage offset for the specified channel

        Parameters
        ----------
        channel : str
            input has to be = C1','C2,'C3'..... for channel to trigger from
        offset : double
            the desired offset in volts
        mode : str
            Should be 'VOLTS' or 'DIV' only

        Returns
        -------
         int
            Returns the result of the *OPC? query

        """
        self.write("OFCT {}".format(mode))
        self.write('{}:OFST {}V'.format(channel,offset))
        return self.query("*OPC?")
    
    def SetSampleRate(self,channel,rate):
        """
        Change the sampling rate of the instument

        Parameters
        ----------
        channel : str
            input has to be = C1','C2,'C3'..... for channel to trigger from
        rate : int
            integer between 500 and 25,000,000. Sampling rate will be set
            to the nearest available option to the input

        Returns
        -------
        int
            Returns the result of the *OPC? query

        """
        # number between 500 and 25 Million
        self.write("{}:MSIZ {}".format(channel,rate))
        return self.query('*OPC?')
    
    def SetAVG(self,channel,num):
        """
        Sets the function F1 to the average of the specified channel to gather data

        Parameters
        ----------
        channel : str
            input has to be = C1','C2,'C3'..... for channel to trigger from
        num : int
            number of averages to take

        Returns
        -------
        int
            Returns the result of the *OPC? query

        """
        self.write('F1:FRST')
        self.write('F1:DEF EQN,AVG({}),SWEEPS,{}'.format(channel,num))
        return self.query('*OPC?')

    def ClearSweeps(self):
        """
        Clear sweeps function of the scope that averages for all channels. 

        Returns
        -------
        int
           Returns the result of the *OPC? query

        """
        self.write('CLSW')
        return self.query('*OPC?')
































