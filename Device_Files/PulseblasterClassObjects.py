# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 16:43:48 2021

@author: Jake Davidson

Class definition for a Tektronics objects 
"""

import spinapi as sa

class PulseBlaster():
    

    def __init__(self):
        """
        For documentation on the Pulseblaster please consult the information
        available in the  C:\SpinCore folder. More usecases are covered here
        including information about the different instruction commands cast
        as object attributes in this class
        
        From SPIN API Documentation online:
        Meaning of inst_data field
        0	CONTINUE	Not Used
        1	STOP	Not Used
        2	LOOP	Number of desired loops
        3	END_LOOP	Address of instruction originating loop
        4	JSR	Address of first instruction in subroutine
        5	RTS	Not Used
        6	BRANCH	Address of instruction to branch to
        7	LONG_DELAY	Number of desired repetitions
        8	WAIT	Not Used

        Returns
        -------
            A Pulseblaster object, an instance of the object class

        """
        
        def enum(**enums):
            return type('Enum', (), enums)

        self.ns = 1.0
        self.us = 1000.0
        self.ms = 1000000.0

        self.MHz = 1.0
        self.kHz = 0.001
        self.Hz = 0.000001
        
        # Defines for start_programming
        self.PULSE_PROGRAM  = 0
        self.FREQ_REGS = 1
        self.PHASE_REGS = 2

        # Defines for enabling analog output
        self.ANALOG_ON = 1
        self.ANALOG_OFF = 0

        # Defines for resetting the phase:
        self.PHASE_RESET = 1
        self.NO_PHASE_RESET = 0

        # Instruction enum
        self.Inst = enum(
                CONTINUE=0,
                STOP=1,
                LOOP=2,
                END_LOOP=3,
                JSR=4,
                RTS=5,
                BRANCH=6,
                LONG_DELAY=7,
                WAIT=8,
                RTI=9
                )
        self.ChannelListBin=[]
        for i in range(24): # Size Set by Channels of PB
            element = 0b000000000000000000000001
            newelement= element << (i)
            self.ChannelListBin.append(newelement)
            
        self.channelcommands=[]
        self.instcommands=[]
        self.instdata=[]
        self.timecommands=[]
        
        
        
        sa.pb_set_debug(1)
        
        sa.pb_select_board(0)

        if sa.pb_init() != 0:
            print("Error initializing board: %s" % sa.pb_get_error())
            input("Please press a key to continue.")
            exit(-1)

        # Configure the core clock
        sa.pb_core_clock(200.0)
        
        
    def ProgStart(self):
        """
        Start the board programming sequence for this pulse blaster object. 

        Returns
        -------
        int
            returns an integer, likely 0 if the start occurs correctly,

        """
        return sa.pb_start_programming(self.PULSE_PROGRAM)
    
    def ProgStop(self):
        """
        Stpo the board programming sequence for this pulse blaster object. 

        Returns
        -------
        int
            returns an integer, likely 0 if the start occurs correctly,

        """
        return sa.pb_stop_programming()
    
    def WriteProg(self):
        """
        Sets the pulse blaster sequence to the current set of commands as
        as stored in the objects attributes. 

        Returns
        -------
        int
            0 on success

        """        
        self.ProgStart()
        for i in range(len(self.channelcommands)):
            sumInteger=0
            if (len(self.channelcommands[i]) >> 0):
                for j in range(len(self.channelcommands[i])):
                    sumInteger = sumInteger + self.ChannelListBin[self.channelcommands[i][j]]
            else:
                sumInteger=0            
            sa.pb_inst_pbonly(sumInteger,self.instcommands[i], self.instdata[i], self.timecommands[i])
        return self.ProgStop()
    
    
    def ViewProg(self):
        """
        Prints current set of instructions in the pulseblaster object to the
        console

        Returns
        -------
        None.

        """
        if len(self.channelcommands)==0:
            print("Empty")
            return
        for i in range(len(self.channelcommands)):
            print(str(self.channelcommands[i]) + ":" + str(self.instcommands[i]) + ":" + str(self.instdata[i]) + ":" + str(self.timecommands[i]) + "\n")
        self.WriteProg()
        return 
    
    def ResetProg(self):
        """
        Sets the current set of pulse blaster commands to an empty list.
        Note that this function scrubs the python object, not the machine.
        to stop the machine from running the sequence use the stop method

        Returns
        -------
        None.

        """
        
        self.channelcommands=[]
        self.instcommands=[]
        self.instdata=[]
        self.timecommands=[]
        return 
    
    
    def WriteCommand(self,channel,cmnd,time,data=0):
        """
        Method writes a sequence command to the end of the command list for the 
        pulse blaster. Note that this method only changes the digital python
        instance. To write the state of the command list to the machine itself
        use the WriteProg method above. 

        Parameters
        ----------
        channel : list
            input a list of numbers from 0-23 corresponding to the channels 
            which should switch on during this command. If all channels should
            be off for this command use the empty list []. 
        cmnd : int
            This input determines the type of pulse blaster instruction to
            write to the board. for most cases the 0, or CONTINUE type is what
            is needed. The final line of a repeating program should be type 6,
            BRANCH. A list of available options for this parameter is in the 
            __init__ method of this function and the pulseblaster docs in the
            C:\SpinCore folder.
        time : double
            the amount of time this command should create pulses for in 
            micro seconds.
        data: int 
                can be many things. Pulseblaster class description contains
                the use for this data input depending on the different types of 
                commands. 
        Returns
        -------
        None.

        """
        
        self.channelcommands.append(channel)
        self.instcommands.append(cmnd)
        self.instdata.append(data)
        self.timecommands.append(time*self.us)
        return
    
    def InsertCommand(self,channel,cmnd,time,index,data=0):
        """
         Method writes a sequence command to the specified position of the command list for the 
        pulse blaster. Note that this method only changes the digital python
        instance. To write the state of the command list to the machine itself
        use the WriteProg method above. 

        Parameters
        ----------
        channel : list
            input a list of numbers from 0-23 corresponding to the channels 
            which should switch on during this command. If all channels should
            be off for this command use the empty list []. 
        cmnd : int
            This input determines the type of pulse blaster instruction to
            write to the board. for most cases the 0, or CONTINUE type is what
            is needed. The final line of a repeating program should be type 6,
            BRANCH. A list of available options for this parameter is in the 
            __init__ method of this function and the pulseblaster docs in the
            C:\SpinCore folder.
        time : double
            the amount of time this command should create pulses for in 
            micro seconds.
        index : int
            Position in the current list of commands to insert the new command.
            All elements after this index are shifted right
        data: int 
                can be many things. Pulseblaster class description contains
                the use for this data input depending on the different types of 
                commands. 
        Returns
        -------
        None.

        """
       
        
        self.channelcommands.insert(index,channel)
        self.instcommands.insert(index,cmnd)
        self.instdata.insert(index,data)
        self.timecommands.insert(index,time*self.us)
        self.WriteProg()
        return
    
    def PopCommand(self,index):
        """
        Remove command at a specific index from the pulse blaster command list

        Parameters
        ----------
        index : int
            remove the command at the selected position from the pulseblaster
            command list. 

        Returns
        -------
        None.

        """
    
        self.channelcommands.pop(index)
        self.instcommands.pop(index)
        self.instdata.pop(index)
        self.timecommands.pop(index)
        self.WriteProg()
        return
    
    def Start(self):
        """
        Start the pulseblaster board sequence

        Returns
        -------
        int
            returns 0 on success

        """
        return sa.pb_start()
    
    def Stop(self):
        """
        Stop the pulseblaster board sequence

        Returns
        -------
        int
            returns 0 on success

        """
        return sa.pb_stop()
    
    def Close(self):
        """
        Close the the digital connection and de-initiallize the pulse blaster. 

        Returns
        -------
        int
            returns 0 on success

        """
        return sa.pb_close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    