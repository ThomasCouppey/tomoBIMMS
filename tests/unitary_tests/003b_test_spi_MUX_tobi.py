import tobi
import time
import andi as ai
import bimms as bm


TB1 = tobi.TomoBimms()
cs = 7

for x in range (16):
    TB1.tx_2_STM32_MUX(x)
    print(x)
