from bimms.system.BIMMS import BIMMS
from bimms.utils.functions import convert
import andi as ai

from . import constantsmux  as cstmux


############################################
#              Class TomoBIMMS             #
############################################
class TomoBimms(BIMMS):
    def __init__(self, bimms_id=None, serialnumber=None):
        super().__init__(bimms_id=bimms_id, serialnumber=serialnumber)
        self.SPI_init_MUX()

        self.sw_vector=cstmux.sw_default 
        self.set_switches(0)    #Dummy set (Bug?)


    ##
    def SPI_init_MUX(self):
        self.SPI_init(cstmux.MUX_STM32_CLK, cstmux.MUX_STM32_CLK_p, cstmux.MUX_STM32_MOSI_p, cstmux.MUX_STM32_MISO_p, cstmux.MUX_STM32_CS_p)

    def tx_2_STM32_MUX(self,value):
        self.SPI_write_32( cstmux.MUX_STM32_CS_p, value)

    def rx_from_STM32_MUX(self):
        return self.SPI_read_32( cstmux.MUX_STM32_CS_p)

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

    def set_STIMp_to_elec(self,electrode,bimms_sel = 0): 
        self.electrode_2_vector(electrode,cstmux.STIMn_shift,cstmux.STIMn_mask)
        self.set_switches(self.sw_vector, bimms_sel)
