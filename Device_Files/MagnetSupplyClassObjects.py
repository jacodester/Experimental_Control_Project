# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:31:36 2021

@author: LocalAdmin
"""
import pyvisa
import time
import numpy as np


class MagnetSupply(pyvisa.resources.GPIBInstrument):
    """
    This is a child class of the pyvisa GPIB instrument class. it contains a
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
        super(MagnetSupply,self).__init__(*args,**kwargs)
        #self.sensorRM = pyvisa.ResourceManager()
        #self.Sensor=self.sensorRM.open_resource('ASRL5::INSTR',resource_pyclass=HallSensor)
        #self.SensorID=self.Sensor.ReadID()
        #self.Field=self.Sensor.ReadField()
        #self.FieldUnit=self.Sensor.ReadUnit()
        
        
        
    def GetState(self):
        """
        Returns state of the output, either Enabled or Disabled

        Returns
        -------
        int
            0 disabled; 1 Enabled

        """
        return self.query('OUTP:STAT?')
    
    def SetState(self,state):
        """
        Set whether output is Enabled or Disabled

        Parameters
        ----------
        state : str
            Either 'ON' or 'OFF' depending on desired state

        Returns
        -------
        int
            result of the OPC query

        """
        self.write('OUTP:STAT {}'.format(state))
        return self.query('*OPC?')
    
    def SetVolts(self,volts,rate):
        """
        This function sets the voltage of the magnet power supply

        Parameters
        ----------
        volts : float
            A number of volts between 0 and 4 V to set the source to
        rate : int
            Number of seconds over which to ramp the voltage

        Returns
        -------
            float
            the actual set voltage of the magnet supply

        """
        VNow=float(self.query('VOLT?'))
        if volts-VNow == 0:
            return
        midpoints=np.linspace(VNow,volts,rate)
        for pt in midpoints:
            self.write('VOLT:LEVEL:IMM:AMPL {}V'.format(pt))
            time.sleep(1)
        
        return float(self.query('VOLT?'))
    
    def SetCurrent(self, current,rate):
        """
        This function sets the current of the magnet power supply

        Parameters
        ----------
        current : float
            The current that you want to provide to the magnet supply 0 amp to VOLTAGE LIMITED
        rate : int
            number of seconds over which to ramp the current

        Returns
        -------
        float
        the actual set current of the magnet supply

        """
        INow=float(self.query('CURR?'))
        diff1 = current - INow 
        if diff1 == 0:
            return
        midpoints1 = np.linspace(INow, current, rate)
        for pt in midpoints1:
            self.write('CURR:LEV:IMM:AMPL {}A'.format(pt))
            time.sleep(1)
            
        return self.query('CURR?')
        
        
    def GetLevel(self):
        """
        Get list of the magnet supply current and voltage settings

        Returns
        -------
        list1 : list
            3 element list, actual magnet voltage, actual magnet current, 
            actual magnet state 'ON' or 'OFF'

        """
        list1 = [self.query('VOLT?') , self.query('CURR?'), self.GetState()]
        return list1
    
    def UpdateField(self):
        """
        Get the current field as measured most recently by the hall sensor

        Returns
        -------
        float
            the field in the defined device Unit. 

        """
        self.Field=self.Sensor.ReadField()
        print('{} {}'.format(self.Field,self.FieldUnit))
        return self.Field
    
class HallSensor(pyvisa.resources.SerialInstrument):
    
    def __init__(self,*args,**kwargs):
        """
        Initialize parameters in the class object, that we will change in
        the class methods later

        Returns
        -------
        None.

        """
        super(HallSensor,self).__init__(*args,**kwargs)
       
    def ReadID(self):
        """
        Get device Identification for the Hall Sensor

        Returns
        -------
        ID : str
            result of the * IDN query for the associated Hall sensor for this magnet

        """
        self.write('*IDN?')
        self.read()
        ID=self.read()
        return ID
    
    def ReadField(self):
        """
        Get the field that is currently measured by the Hall sensor

        Returns
        -------
        float
            Returns the numerical value for the field in the units of the device

        """
        self.write('MEAS?')
        self.read() # device Echos command
        field=self.read() # but we want the result so we return the second read
        return float(field.split(' ')[0]) # Pull only the numeric value
    
    def ReadUnit(self):
        """
        Get the field unit that is the current setting of the hall sensor

        Returns
        -------
        str
            a string of the unit of the hall sensor. 

        """
        self.write('UNITS?')
        self.read() # device Echos command
        unit=self.read() # but we want the result so we return the second read
        return unit # is unit only
    
    def Zero(self):
        """
        Set Hall sensor zero field value

        Returns
        -------
        None.

        """
        self.write('ZERO')
        return 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        