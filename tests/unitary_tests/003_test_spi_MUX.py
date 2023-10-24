import tobi
import time

value = 10

TB1 = tobi.TomoBimms()
for i in range(100):
    TB1.tx_2_STM32_MUX(10)
    time.sleep(0.2)

