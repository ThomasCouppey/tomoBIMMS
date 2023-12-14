import tobi
import time
import andi as ai
import bimms as bm

value = 10

'''TB1 = tobi.TomoBimms()
for i in range(100):
    TB1.tx_2_STM32_MUX(10)
    time.sleep(0.2)'''

def set_bit(value, bit):
    value = int(value)
    return value | (1<<bit)

def clear_bit(value, bit):
    value = int(value)
    return value & ~(1<<bit)

    
ad2 = ai.Andi('SN:210321B28CCD')

## STM32 to AD2 SPI 
STM32_CLK = 1e6
STM32_CLK_p = 1
STM32_MOSI_p = 2
STM32_MISO_p = 3
STM32_CS_p = 0

#Init MUX_CS pin as output
MUX_CS_p = 7
IO_vector = 0
IO_vector = set_bit(IO_vector,MUX_CS_p)
ad2.digitalIO_set_as_output(IO_vector)

#set it high 
IO_state = ad2.digitalIO_read_outputs()
IO_state = set_bit(IO_state,MUX_CS_p)
ad2.digitalIO_output(IO_vector)

## init SPI
ad2.SPI_reset()
ad2.set_SPI_frequency(STM32_CLK)
ad2.set_SPI_Clock_channel(STM32_CLK_p)
ad2.set_SPI_Data_channel(ai.SPIDataIdx["DQ0_MOSI_SISO"], STM32_MOSI_p)
ad2.set_SPI_Data_channel(ai.SPIDataIdx["DQ1_MISO"], STM32_MISO_p)
ad2.set_SPI_mode(ai.SPIMode["CPOL_1_CPA_1"])
ad2.set_SPI_MSB_first()

ad2.set_SPI_CS(STM32_CS_p, ai.LogicLevel["H"])  #useless but still required.....


value = 128
#TX a value
tx_8bvalues = bm.convert(value)

for k in range (100):
    IO_state = ad2.digitalIO_read_outputs()
    IO_state = clear_bit(IO_state,MUX_CS_p)
    
    ad2.digitalIO_output(IO_state)
    #ad2.SPI_select(STM32_CS_p, ai.LogicLevel["H"])
    ad2.set_SPI_CS(STM32_CS_p, -1)  #useless but still required.....
    for k in tx_8bvalues:
        ad2.SPI_write_one(ai.SPI_cDQ["MOSI/MISO"], 8, k)
    IO_state = ad2.digitalIO_read_outputs()
    IO_vector = set_bit(IO_vector,MUX_CS_p)
    #ad2.SPI_select(STM32_CS_p, ai.LogicLevel["H"])
    ad2.digitalIO_output(IO_vector)

    ad2.set_SPI_CS(STM32_CS_p, ai.LogicLevel["H"])  #useless but still required.....
    ad2.SPI_select(STM32_CS_p, ai.LogicLevel["L"])
    for k in tx_8bvalues:
        ad2.SPI_write_one(ai.SPI_cDQ["MOSI/MISO"], 8, k)
    ad2.SPI_select(STM32_CS_p, ai.LogicLevel["H"])
