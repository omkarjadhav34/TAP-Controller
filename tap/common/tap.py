##########################################################
# PSU ECE510 Post-silicon Validation Project 1
# --------------------------------------------------------
# Filename: tap.py
# --------------------------------------------------------
# Purpose: TAP Controler Class
##########################################################

from tap.common.tap_gpio import *
from tap.log.logging_setup import *
import time

class Tap(Tap_GPIO):
    """ Class for JTAG TAP Controller"""

    def __init__(self,log_level=logging.INFO):
        """ initialize TAP """
        self.logger = get_logger(__file__,log_level)
        self.max_length = 1000
        self.tck = 0

        #set up the RPi TAP pins
        Tap_GPIO.__init__(self)

    def toggle_tck(self, tms, tdi):
        """ toggle TCK for state transition 

        :param tms: data for TMS pin
        :type tms: int (0/1)
        :param tdi: data for TDI pin
        :type tdi: int (0/1)

        """
        Tap_GPIO.set_io_data(tms, tdi, 1)
        Tap_GPIO.delay(1.0)
        Tap_GPIO.set_io_data(tms, tdi, 0)
        Tap_GPIO.delay(1.0)
        
        pass
       
    def reset(self):
        """ set TAP state to Test_Logic_Reset """
        
        # Assert TMS for 5 TCKs in a row
        # State transition from TLReset to IDLE State 
        for clk_count in range(0, 5):
            self.toggle_tck(tms = 0, tdi = 0)
            Tap_GPIO.delay(1.0)
            
        pass

    def reset2ShiftIR(self):
        """ shift TAP state from reset to shiftIR """
        
        # State transitions: Idle -> Select DR -> Select IR
        # -> Capture IR -> Shift IR
        
        # Add a contion to check if the present state is Idle state
        # or not
        
        # Currently assuming that it is in the idle state only.
        
        # Idle -> Select DR
        self.toggle_tck(tms = 1, tdi = 0)
        
        # Select DR -> Select IR
        self.toggle_tck(tms = 0, tdi = 0)
        
        # Select IR -> Capture IR
        self.toggle_tck(tms = 0, tdi = 0)
        
        # Capture IR -> Shift IR
        self.toggle_tck(tms = 0, tdi = 0)
        
        pass 

    def exit1IR2ShiftDR(self):
        """ shift TAP state from exit1IR to shiftDR """

        # State transitions: Shift IR -> Exit1IR -> Update IR -> IDLE
        # -> IDLE -> Select DR -> Capture DR -> Shift DR
        
        # Shift IR -> Exit1IR
        self.toggle_tck(tms = 1, tdi = 0)

        # Exit1IR -> Update IR
        self.toggle_tck(tms = 1, tdi = 0)
        
        # Update IR -> IDLE
        self.toggle_tck(tms = 0, tdi = 0)
        
        pass

    def exit1DR2ShiftIR(self):
        """ shift TAP state from exit1DR to shiftIR """
        
        # State transitions: Exit1DR -> Update DR -> IDLE
        # -> Idle -> Select DR -> Select IR -> Capture IR 
        # -> Shift IR
        
        # Shift DR -> Exit1DR
        self.toggle_tck(tms = 1, tdi = 0)

        # Exit1DR -> Update DR
        self.toggle_tck(tms = 1, tdi = 0)
        
        # Update DR -> IDLE
        self.toggle_tck(tms = 0, tdi = 0)
        
        # State transitions: Idle -> Select DR -> Select IR
        # -> Capture IR -> Shift IR
        self.reset2ShiftIR(self)
        
        pass

    def shiftInData(self, tdi_str):    
        """ shift in IR/DR data

        :param tdi_str: TDI data to shift in
        :type tdo_str: str

        """
    
        for binary in tdi_str:
            self.toggle_tck(tms = 0, tdi = int(binary))
        pass

    def shiftOutData(self, length):
        """ get IR/DR data

        :param length: chain length        
        :type length: int
        :returns: int - TDO data

        """
        for i in range(0, length):
            self.toggle_tck(tms = 0, tdi = 0)
        
        return Tap_GPIO.read_tdo_data()

    def getChainLength(self):
        """ get chain length

        :returns: int -- chain length	

        """

        return 0
