# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 13:37:42 2021

@author: Jake Davidson with influence from Github Authors:
https://github.com/asvela/tektronix-func-gen
https://github.com/Ulm-IQO/qudi


Class definition for a Tektronics objects 
"""
import pyvisa
import time
import numpy as np
import os
from ftplib import FTP 


class AFG(pyvisa.resources.TCPIPInstrument):
    """
    This is a child class of the pyvisa TCPIP instrument class. it contains a
    series of methods and functons to connect and control the function generator
    
    """
    def __init__(self,*args,**kwargs):
        """
        Initialize parameters in the class object, that we will change in
        the class methods later

        Returns
        -------
        None.

        """
        super(AFG,self).__init__(*args,**kwargs)
        
        # Values for the TekTronix AFG3102 for uploading Arb functions
        self._arbitrary_waveform_resolution=16382
        self._arbitrary_waveform_length = (1000, 131000)
        self._max_waveform_memory_user_locations=4
        
        
       
    
    def SetFreq(self,channel,frequency):
        """
        Change the frequency of channel 1 on the function generator

        Parameters
        ----------
        frequency : double
            input a frequency in MHz that should be the channel frequency
            
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        Returns
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query

        """
        sendstring ='SOUR'+channel+':FREQ ' + str(frequency) + "MHz"
        self.write(sendstring)
        return self.query("*OPC?")
    
    
    def SetPer(self,channel,period):
        """
        Change the Period of channel on the function generator

        Parameters
        ----------
        period : double
            input a time in ms that should be the channel period
            
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        Returns
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query

        """
        sendstring = 'SOUR'+channel+':PULS:PER ' + str(period) + "ms"
        self.write(sendstring)
        return self.query("*OPC?")
    
    
    def SetWidth(self,channel,width):
        """
        Change the pulse width of channel on the function generator

        Parameters
        ----------
        width : double
            input a time in ms that should be the channel pulse width
            
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        Returns
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query

        """
        sendstring = 'SOUR'+channel+':PULS:WIDT ' + str(width) + "ms"
        self.write(sendstring)
        return self.query("*OPC?")
    
    def SetDuty(self,channel,duty):
        """
        Change the pulse duty cycle of channel on the function generator

        Parameters
        ----------
        duty : double
            input a percentage that should be the pulse duty cycle
            
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        Returns
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query

        """
        sendstring = 'SOUR'+channel+':PULS:DCYC ' + str(duty) 
        self.write(sendstring)
        return self.query("*OPC?")
    
    def SetNumCyc(self,channel,numcyc):
        """
        Change the number of pulses for the burst channel on the function generator
        
        The machine needs to be in BURST mode for this to function. Need to
        add in the insurance that we are in BURST mode before changes
        
        Parameters
        ----------
        numcyc : double
            input a number of pulses that should make up the function
            
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        Returns
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query

        """
        sendstring = 'SOUR'+channel+':BURS:NCYC' + str(numcyc) 
        self.write(sendstring)
        return self.query("*OPC?")
    
    def SetVoltage(self,channel,HL,voltage):
        """
        Change the high voltage for the given channel on the function generator

        Parameters
        ----------
        voltage : double
            input a number in volts that should be pulses max height on the channel
            For now dont set the low voltage higher than the high voltage.
            Need to write precautions to stop this...
        
        HL : str
            determine whether to set the channel high voltage or low voltage.
            Must be string "HIGH" or "LOW" or "OFFS" for the DC mode
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        
        
        Return
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query

        """
        if (voltage+float(5) > 10):
            voltage=float(5)
        if (voltage + float(-5) < -10):
            voltage=-float(5)
        sendstring = 'SOUR'+ channel +':VOLT:LEV:IMM:'+ HL + " " + str(voltage) + 'V'
        sendstring = 'SOUR{}:VOLT:LEV:IMM:{} {}V'.format(channel,HL,voltage)
        self.write(sendstring)
        #print(sendstring)
        return self.query("*OPC?")
    
    
    def SetState(self,channel,state):
        """
        Turn on/off a channel of the AFG 

        Parameters
        ----------
        state : str
            Must be a string either "ON" or "OFF" to indicate the desired state for the given channel
        
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        
        
        Return
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query

        """
        
        sendstring = 'OUTP' + channel +':STAT ' + state
        self.write(sendstring)
        return self.query("*OPC?")
    
    
    def SetFunction(self,channel,shape):
        """
        Switch channel to a different shaped waveform

        Parameters
        ----------
        shape : str
            One of strings:
                "DC"
                "SIN"
                "SQU"
                "RAMP"
                "PULS"
                "ARB"
                "USER1"
                "USER2"
                ...
                to indicate the desired waveform shape for the given channel
        
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        
        
        Return
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query

        """
        
        sendstring = 'SOUR' + channel +':FUNC:SHAP ' + shape
        self.write(sendstring)
        return self.query("*OPC?")
    
    
    def SetBurst(self,channel,state):
        """
        Sets AFG Channel to Burst mode

        Parameters
        ----------
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        state : str
            Must be "on" or "OFF" so as to set the state as desired
        
        Return
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query


        """
    
        sendstring = 'SOUR' + channel +':BURS:STAT ' + state
        self.write(sendstring)
        return self.query("*OPC?")
        
    def SetPolarity(self,channel,POL):
        """
        Switch the Polarity of  a channel of the AFG 

        Parameters
        ----------
        POL : str
            Must be a string either "NORM" or "INV" to indicate the desired state for the given channel
        
        channel : str    
            Must be string either '1' or '2' to denote the channel for freq set
        
        
        Return
        -------
        1 if successful. 0 if there is a problem with "*OPC?" query

        """
        
        sendstring = 'OUTP{}:POL {}'.format(channel,POL)
        self.write(sendstring)
        return self.query("*OPC?")
    
    
    def set_custom_waveform(
        self,
        waveform: np.ndarray,
        normalise: bool = True,
        memory_num: int = 0,
        print_progress: bool = True,
        ):
        """Transfer waveform data to edit memory and then user memory.
        NOTE: Will overwrite without warnings
        Parameters
        ----------
        waveform : ndarray
            Either unnormalised arbitrary waveform (then use `normalise=True`),
            or ints spanning the resolution of the function generator
        normalise : bool
            Choose whether to normalise the waveform to ints over the
            resolution span of the function generator
        memory_num : str or int {0,...,255}, default 0
            Select which user memory to copy to
        print_progress : bool, default `True`
        Returns
        -------
        waveform : ndarray
            The normalised waveform transferred
        Raises
        ------
        ValueError
            If the waveform is not within the permitted length or value range
        RuntimeError
            If the waveform transferred to the instrument is of a different
            length than the waveform supplied
        """
        # Check whether the user wants to put the waveform in the right memory slot
        if not 0 <= memory_num <= self._max_waveform_memory_user_locations:
            raise ValueError(
                f"The memory location {memory_num} is not a valid "
                "memory location for this model"
            )
        # Check if waveform data is suitable
        if print_progress:
            print("Check if waveform data is suitable..", end=" ")
        self._check_arb_waveform_length(waveform)
        try:
            self._check_arb_waveform_type_and_range(waveform)
        except ValueError as err:
            if print_progress:
                print(f"\n  {err}")
                print("Trying again normalising the waveform..", end=" ")
        # Normalize waveform to the correct integer scale for the device
        if normalise:
            waveform = self._normalise_to_waveform(waveform)
            
        if print_progress:
            print("ok")
            print("Transfer waveform to function generator..", end=" ")
        # Transfer waveform
        self.write_binary_values(
            "DATA:DATA EMEMory,", waveform, datatype='H', is_big_endian=True)
        if print_progress:
            print("ok")
            print(f"Copy waveform to USER{memory_num}..", end=" ")
        self.write(f"DATA:COPY USER{memory_num},EMEMory")
        if print_progress:
            print("ok")
        return waveform

    def _normalise_to_waveform(self, shape: np.ndarray) -> np.ndarray:
        """Normalise a shape of any discretisation and range to a waveform that
        can be transmitted to the function generator
        .. note::
            If you are transferring a flat/constant waveform, do not use this
            normaisation function. Transfer a waveform like
            `int(self._arbitrary_waveform_resolution/2)*np.ones(2).astype(np.int32)`
            without normalising for a well behaved flat function.
        Parameters
        ----------
        shape : array_like
            Array to be transformed to waveform, can be ints or floats,
            any normalisation or discretisation
        Returns
        -------
        waveform : ndarray
            Waveform as ints spanning the resolution of the function gen
        """
        # Check if waveform data is suitable
        self._check_arb_waveform_length(shape)
        # Normalise
        waveform = shape - np.min(shape)
        normalisation_factor = np.max(waveform)
        waveform = waveform / normalisation_factor * self._arbitrary_waveform_resolution
        return waveform.astype(np.uint16)
    
    def _check_arb_waveform_length(self, waveform: np.ndarray):
        """Checks if waveform is within the acceptable length
        Parameters
        ----------
        waveform : array_like
            Waveform or voltage list to be checked
        Raises
        ------
        ValueError
            If the waveform is not within the permitted length
        """
        if (len(waveform) < self._arbitrary_waveform_length[0]) or (
            len(waveform) > self._arbitrary_waveform_length[1]
        ):
            msg = (
                "The waveform is of length {}, which is not within the "
                "acceptable length {} < len < {}"
                "".format(len(waveform), *self._arbitrary_waveform_length)
            )
            raise ValueError(msg)

    def _check_arb_waveform_type_and_range(self, waveform: np.ndarray):
        """Checks if waveform is of int/np.int32 type and within the resolution
        of the function generator
        Parameters
        ----------
        waveform : array_like
            Waveform or voltage list to be checked
        Raises
        ------
        ValueError
            If the waveform values are not int, np.uint16 or np.int32, or the
            values are not within the permitted range
        """
        for value in waveform:
            if not isinstance(value, (int, np.uint16, np.int32)):
                raise ValueError(
                    "The waveform contains values that are not"
                    "int, np.uint16 or np.int32"
                )
            if (value < 0) or (value > self._arbitrary_waveform_resolution):
                raise ValueError(
                    f"The waveform contains values out of range "
                    f"({value} is not within the resolution "
                    f"[0, {self._arbitrary_waveform_resolution}])"
                )
        return
    def get_error(self) -> str:
        """Get the contents of the Error/Event queue on the device
        Returns
        -------
        str
            Error/event number, description of error/event
        """
        return self.query("SYSTEM:ERROR:NEXT?")
    
    
    
    
    
    
    
    
    
    
class AWG(pyvisa.resources.TCPIPInstrument):
    """
    This is a child class of the pyvisa TCPIP instrument class. it contains a
    series of methods and functons to connect and control the function generator
    
    Contains some methods from the QUDI implementation of the AWG70002A.
    
    """
    def __init__(self,*args,**kwargs):
        """
        Initialize parameters in the class object, that we will change in
        the class methods later

        Returns
        -------
        None.

        """
        super(AWG,self).__init__(*args,**kwargs)
        self.num_tracks = 2
        self.curpath='C:/Users/OEM/Desktop/YGG Cavity Memory/'
        self.samplerate=25e9
       
        
    def SetON_OFF(self,channel, cmd):
        """
        Supply the parameters for this function according to the syntax from the
        Tektronix AWG devices to change the state of a output channel between on and off.

        Parameters
        ----------
        channel : int
           Specify channel number 1 or 2 to be switched on or off
        cmd : str
            Can be one of 2 strings "ON" or "OFF" depending on the desired state of the channnel

        Returns
        -------
        result of the OPC Query

        """
        self.write('OUTP{}:STAT {}'.format(channel,cmd))
        return self.query('*OPC?')

    def SetState(self, cmd):
        """
        Changes RUN/STOP state of the AWG

        Parameters
        ----------
        cmd : str
            Can be one of 2 strings "RUN" or "STOP" depending on the desired state of the machine

        Returns
        -------
        int
            Result of the *OPC? query

        """
        self.write('AWGC:{}:IMM'.format(cmd))
        return  self.query('*OPC?')

    def ChannelFunc(self,name,channel,seqwav,track=1):
        """
        Sets the specified channel to the specified function name. Works for 
        both sequnces and waveforms individually, but sequence track defaults
        to 1.

        Parameters
        ----------
        name : str
            name of the waveform or sequence that should be run
        channel : int
             1 or 2 depending on the desired channel
        seqwav : str
            Either 'SEQ', or 'WAV' depending on which function name belongs to
        track : int, optional
            if loading a sequence specify the track number to run on this channel.
            The default is 1.

        Returns
        -------
        int
            result of *OPC? query

        """
        if (seqwav == 'SEQ'):
            self.write('SOUR{}:CASS:SEQ "{}",{}'.format(channel,name,track))
        elif (seqwav == 'WAV'):
            self.write('SOUR{}:CASS:WAV "{}"'.format(channel,name))
        return self.query('*OPC?')
    
    
    def NewSeq(self,name,steps):
        """
        Creates new sequence. If a sequence of the given name exists already it
        is deleted.

        Parameters
        ----------
        name : str
            Name for the new sequence to be created or over written
        steps : int
            number of steps to create for the sequence

        Returns
        -------
        int
            result of *OPC? query

        """
        self.DeleteSeq(name)
        self.write('SLIS:SEQ:NEW "{}",{}'.format(name,steps))
        return self.query('*OPC?')
    
    def DeleteSeq(self,name):
        """
        Deletes the named sequence

        Parameters
        ----------
        name : str
            Name of sequence to be deleted

        Returns
        -------
        int
            result of *OPC? query

        """
        self.write('SLIS:SEQ:DEL "{}"'.format(name))
        return self.query('*OPC?')
    
     
    def sequence_set_waveform(self, sequence_name, waveform_name, step, track):
        """
        Sets the given waveform to the specified track and step of the named 
        sequence

        Parameters
        ----------
        sequence_name : str
            sequence name of the sequence to be modified
        waveform_name : str
            name of the waveform to be set as the sequence step
        step : int
            step of the sequence for which the waveform will be added
        track : int
            track of the sequence to add the waveform to 

        Returns
        -------
        int
            result of *OPC? query

        """
     
        self.write('SLIS:SEQ:STEP{0:d}:TASS{1:d}:WAV "{2}", "{3}"'.format(step, track, sequence_name, waveform_name))
        return self.query('*OPC?')

    def sequence_set_repetitions(self, sequence_name, step, repeat=1):
        """
        Set repetition number for the step of the given sequence and step

        Parameters
        ----------
        sequence_name : str
            name of the sequence to modify
        step : int
            step of the sequence to modify 
        repeat : int, optional
            number of times to repeat the step. The default is 0 which means
            the step will run exactly 1 time, and not be repeated.
            (-1: infinite, 0: once, 1: twice, ...)

        Returns
        -------
        int
            result of *OPC? query

        """
        
        repeat = 'INF' if repeat < 0 else str(int(repeat))
        self.write('SLIS:SEQ:STEP{0:d}:RCO "{1}", {2}'.format(step, sequence_name, repeat))
        return self.query('*OPC?')

    def sequence_set_goto(self, sequence_name, step, goto=-1):
        """
        Sets the go to parameter of the given sequence step

        Parameters
        ----------
        sequence_name : str
            name of the given sequence to be modified
        step : int
            step number of the given sequence t be modified
        goto : int, optional
            step number of the go to parameter. For example, to go to the first
            step of the sequence this parameter should be 1. Default input yields
            going to the next step. The default is -1.

        Returns
        -------
        int
            result of *OPC? query

        """
       
        
        goto = str(int(goto)) if goto > 0 else 'NEXT'
        self.write('SLIS:SEQ:STEP{0:d}:GOTO "{1}", {2}'.format(step, sequence_name, goto))
        return self.query('*OPC?')

    def sequence_set_wait_trigger(self, sequence_name, step, trigger='OFF'):
        """
        Sets the trigger parameter of the given sequence step

        Parameters
        ----------
        sequence_name : str
            name of the sequence to be modified
        step : int
            step number of the sequence to be modified
        trigger : str, optional
            Determines the trigger signal to be responded to. Needs to be either
            'ATR', or 'BTR'. The default is 'OFF' which means this step will 
            run when it is gone to. ('OFF', 'ATR', 'BTR' or 'INT')

        Returns
        -------
        int
            result of *OPC? query

        """
      
        self.write('SLIS:SEQ:STEP{0:d}:WINP "{1}", {2}'.format(step, sequence_name, trigger))
        return self.query('*OPC?')

    def make_sequence_continuous(self, sequencename):
        """
        Usually after a run of a sequence the output stops. Many times it is desired that the full
        sequence is repeated many times. This is achieved here by setting the 'jump to' value of
        the last element to 'First'

        Parameters
        ----------
        sequencename : str
            sequence to be modified

        Returns
        -------
        int
            result of *OPC? query

        """
        
        last_step = int(self.query('SLIS:SEQ:LENG? "{0}"'.format(sequencename)))
        self.sequence_set_goto(sequencename, last_step, 1)
        
        return self.query('*OPC?')
    
    def write_sequence(self, name, sequence_parameter_list):
        """
        Use this function to write an antirely new sequence to the AWG, rather 
        than modifying individual parameters of an existing sequence.

        Parameters
        ----------
        name : str
            name of the sequence to be created
        sequence_parameter_list : list of lists
            This parameter needs to be a correctly formatted list of lists. 
            Each sub-list will make a single step of the sequence. A sequence
            step will be created for each sublist in the parameter list. 
            The sublist parameters are:
                1 tuple of strings
                    a tuple of waveform names to be set for the different tracks
                2 int
                    step number to modify
                3 str
                    trigger for the step
                4 int
                    repetitions to be set for the step
                5 int
                    goto parameter for the step
            e.g. SEQList=[[('JakeTest','JakeTest1'), 1, 'BTR', 9, 0],
                     [('JakeTest1',''), 2, 'OFF', 0, 1]
                    ]

        Returns
        -------
        num_steps : int
            number of steps successfully written

        """
        num_steps = len(sequence_parameter_list)
        # Create new sequence and set jump timing to immediate.
        # Delete old sequence by the same name if present.
        self.NewSeq(name=name, steps=num_steps)
        for step, command in enumerate(sequence_parameter_list,1):
            #print(step, command[0])
            for track, waveform in enumerate(command[0],1):
                self.sequence_set_waveform(name, waveform, step, track)
            if command[2] != 'OFF':
                self.sequence_set_wait_trigger(name, step, command[2])
            if command[3] != 0:
                self.sequence_set_repetitions(name,step, command[3])
            if command[4] > 0:
                if command[4] <= num_steps:
                    self.sequence_set_goto(name, step, command[4])
                    
        # Wait for everything to complete
        while int(self.query('*OPC?')) != 1:
            time.sleep(0.25)
        self.write('*cls')
        return num_steps
    def write_waveform(self,wavname,wfmData, marker1Data, marker2Data):
        """
        Writes a new waveform to the AWG with the given name, analog and marker
        data

        Parameters
        ----------
        wavname : str
            name to be assigned on the AWG to the new waveform. If the current
            name exists already the file will be deleted and overwritten.
        wfmData : array
            a 1D numpy array of the analog values in the waveform. Values
            should be type float 32, but if not they will be converted.
            Lenth in points of this waveform determines the duration of the 
            waveform and all contained pulses for the fixed MAX sampling rate of 
            the AWG
        marker1Data : array
            a 1D array of binary values to determine the points which have
            have marker 1 on and off. This array must be the same length as the 
            analog data.
        marker2Data : array
            a 1D array of binary values to determine the points which have
            have marker 2 on and off. This array must be the same length as the 
            analog data.

        Returns
        -------
        int
            result of *OPC? query

        """
        
        self.timeout = 20000
        #self.encoding = 'latin_1'
        #self.write_termination = None
        #self.read_termination = '\n'
        self.write('*cls')
        recordLength=len(wfmData)
        if (recordLength > 200000000):
            print('Caution: Potential Timeout')
        
        # Send Waveform Data
        self.write('WLIS:WAV:DEL "{}"'.format(wavname))
        self.write('WLIS:WAV:NEW "{}", {}'.format(wavname, recordLength))
        stringArg = 'WLIS:WAV:DATA "{}", 0, {}, '.format(wavname, recordLength)
        self.write_binary_values(stringArg, wfmData.astype(np.float32))
        self.query('*OPC?')
        
        # Send Marker Data
        exData1 = (1 << 6) * marker1Data.astype(np.uint8) # np.random.randint(2, size=recordLength, dtype=np.uint8)
        exData2 = (1 << 7) * marker2Data.astype(np.uint8) # np.random.randint(2, size=recordLength, dtype=np.uint8)
        markerData = exData1 + exData2
        stringArg = 'WLIS:WAV:MARK:DATA "{}", 0, {}, '.format(wavname, recordLength)
        self.write_binary_values(stringArg, markerData, datatype='B')
        self.query('*OPC?')
        self.timeout = 2000
        return  self.query('*OPC?')
        
    def save_Func(self,name,seqwav):
        """
        Save the given sequence or waveform to the base path of the digital object

        Parameters
        ----------
        name : str
            name of the waveform or sequence to be saved
            
        seqwav : str
            determines if we are saving a waveform('WAV') or sequence('SEQ')

        Returns
        -------
        int
            result of *OPC? query

        """
        if (seqwav == 'WAV'):
            self.write('MMEM:SAVE:WAV:WFMX "{}", "{}{}.wfmx"'.format(name,self.curpath,name))
        elif (seqwav == 'SEQ'):
            self.write('MMEM:SAVE:SEQ "{}", "{}{}.seqx"'.format(name,self.curpath,name))
        return self.query('*OPC?')

       