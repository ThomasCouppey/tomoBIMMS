import tobi
import time


TB1 = tobi.TomoBimms()
for i in range (16):
    TB1.set_switches(i<<20)
    time.sleep(0.1)
