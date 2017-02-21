from __future__ import division, absolute_import, print_function
from ScopeFoundry import HardwareComponent

try:
    from ScopeFoundryHW.ni_daq import NI_AdcTask
except Exception as err:
    print ("Cannot load required modules for  analog readout: {}".format( err))

class TestAnalogReadOutHW(HardwareComponent):

    name = 'test_analog_readout'

    def setup(self):
        
        self.settings.New('voltage', dtype=float, ro=True, unit='V')
        
        self.settings.New('channel', dtype=str, initial='/Dev1/ai0')
        
    def connect(self):
        self.settings.channel.change_readonly(True)
    
        self.adc = NI_AdcTask(channel=self.settings['channel'], range=10, name=self.name, terminalConfig='rse')
        self.adc.set_single()
        
        self.adc.start()
        
        #Connect settings to hardware
        self.settings.voltage.hardware_read_func = self.read_adc_single
        
    
    def disconnect(self):
        #disconnect all settings from hardware
        for lq in self.settings.as_list():
            lq.hardware_read_func = None
            lq.hardware_set_func = None
        
        if hasattr(self, 'adc'):
            #disconnect hardware
            self.adc.stop()
            self.adc.close()
            
            # clean up hardware object
            del self.adc

        self.settings.channel.change_readonly(False)


    def read_adc_single(self):
        resp = self.adc.get()
        if self.debug_mode.val:
            self.log.debug( "read_adc_single resp: {}".format( resp))
        return float(resp[0])