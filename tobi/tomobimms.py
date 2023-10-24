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
