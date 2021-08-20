# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 10:16:48 2021

@author: LocalAdmin
"""
import pyvisa
import time
import numpy as np

class Attocube(pyvisa.resources.SerialInstrument):
    
    def __init__(self,*args,**kwargs):
        """
        Initialize parameters in the class object, that we will change in
        the class methods later

        Returns
        -------
        None.

        """
        super(Attocube,self).__init__(*args,**kwargs)
       
