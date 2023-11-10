import tobi
import time

x = 17
TB1 = tobi.TomoBimms()
while(True):
    for i in range (1,17):
        print("Electrode: " +str(i))
        TB1.set_CH1n_to_elec(i)
        TB1.set_CH1p_to_elec(x-i)
        time.sleep(0.05)
