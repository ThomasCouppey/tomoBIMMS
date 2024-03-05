from bimms.system.BIMMS import BIMMS
from bimms.utils.functions import convert
from bimms.utils import constants as cstbm
import andi as ai
import time

from ..utils import constantsmux  as cstmux
from ..backend.EIT_class import EIT_class
from ..results.EIT_results import EIT_results

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)


############################################
#              Class TomoBIMMS             #
############################################
class TomoBimms(BIMMS, EIT_class):
    def __init__(self, bimms_id=None, serialnumber=None):
        BIMMS.__init__(self, bimms_id=bimms_id, serialnumber=serialnumber)
        EIT_class.__init__(self)
        self.init_CS_pin(cstmux.MUX_STM32_CS_p)

        self.sw_vector=cstmux.sw_default 
        self.set_switches(0)    #Dummy set (Bug?)

        self.current_inj = None
        self.current_rec = None

    ############################
    # BIMMS Hardware overloads #
    ############################

    def init_CS_pin(self,CS_pin):
        self.set_CS_pin(CS_pin)

    def set_CS_pin(self,CS_pin):
        self.set_IO(CS_pin,1)
    
    def reset_CS_pin(self,CS_pin):
            self.set_IO(CS_pin,0)

    def SPI_write_32_MUX(self,CS_pin,value):
        tx_8bvalues = convert(value)
        self.ad2.set_SPI_CS(cstbm.STM32_CS_p, -1)       #Apparently required :(
        self.reset_CS_pin(CS_pin)
        for k in tx_8bvalues:
            self.ad2.SPI_write_one(ai.SPI_cDQ["MOSI/MISO"], 8, k)
        self.set_CS_pin(CS_pin)

    def tx_2_STM32_MUX(self,value):
        self.SPI_write_32_MUX( cstmux.MUX_STM32_CS_p, value)

    def set_switches(self, switches_vector, bimms_sel=0):
        value = cstmux.cmd_shift * (cstmux.set_switch + bimms_sel) + switches_vector
        self.tx_2_STM32_MUX(value)

    def electrode_2_vector(self,electrode,shift,mask):
        self.sw_vector=(self.sw_vector & mask)+ (electrode-1<<shift)

    def set_CH1p_to_elec(self,electrode,bimms_sel = 0): 
        self.electrode_2_vector(electrode,cstmux.CH1p_shift,cstmux.CH1p_mask)
        self.set_switches(self.sw_vector, bimms_sel)

    def set_CH1n_to_elec(self,electrode,bimms_sel = 0): 
        self.electrode_2_vector(electrode,cstmux.CH1n_shift,cstmux.CH1n_mask)
        self.set_switches(self.sw_vector, bimms_sel)

    def set_CH2p_to_elec(self,electrode,bimms_sel = 0): 
        self.electrode_2_vector(electrode,cstmux.CH2p_shift,cstmux.CH2p_mask)
        self.set_switches(self.sw_vector, bimms_sel)

    def set_CH2n_to_elec(self,electrode,bimms_sel = 0): 
        self.electrode_2_vector(electrode,cstmux.CH2n_shift,cstmux.CH2n_mask)
        self.set_switches(self.sw_vector, bimms_sel)
    
    def set_STIMp_to_elec(self,electrode,bimms_sel = 0): 
        self.electrode_2_vector(electrode,cstmux.STIMp_shift,cstmux.STIMp_mask)
        self.set_switches(self.sw_vector, bimms_sel)

    def set_STIMn_to_elec(self,electrode,bimms_sel = 0): 
        self.electrode_2_vector(electrode,cstmux.STIMn_shift,cstmux.STIMn_mask)
        self.set_switches(self.sw_vector, bimms_sel)

    ##########################
    # BIMMS Config overloads #
    ##########################


    ########################
    # EIT relative methods #
    ########################
    def update_injection(self, inj_pat, **kwgs):
        if self.current_inj != inj_pat:
            print("\ninjection set to", inj_pat)
            self.current_inj = inj_pat
            self.set_STIMn_to_elec(inj_pat[0])
            self.set_STIMp_to_elec(inj_pat[1])

    def update_recording(self, rec_pat, **kwgs):
        if self.current_rec != rec_pat:
            print("recording set to", rec_pat)
            self.current_rec = rec_pat
            self.set_CH1n_to_elec(rec_pat[0])
            self.set_CH1p_to_elec(rec_pat[1])
            #time.sleep(0.001)

    def get_recording(self, clear_mstack=False, overwrite=False, **kwgs):

        super().measure(clear_mstack=clear_mstack, overwrite=overwrite)
        return {}

    def eit_measure(self, inj_kwargs={}, rec_kwargs={}, save=False, fname="output.json"):
        super().setup_bimms()
        self.is_setup = True
        super().eit_measure(inj_kwargs, rec_kwargs, save, fname)
        return self.results
