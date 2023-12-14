import tobi
import time
import bimms as bm
import matplotlib.pyplot as plt

TB1 = tobi.TomoBimms()

Gain_IRO = 10
Gain_VRO = 10
fmin = 1000
fmax = 1e6
n_pts = 101
settling_time = 0.01
NPeriods = 32
I_stim = 100 #100uA excitation
V_stim = 100

ELEC_GND = 16
ELEC_min = 1
ELEC_max = 14

TB1.config.excitation_mode("G_EIS")
TB1.config.wire_mode("4_WIRE")
TB1.config.excitation_signaling_mode("SE")
TB1.config.excitation_coupling("DC")
TB1.config.G_EIS_gain("HIGH")
TB1.config.IRO_gain(Gain_IRO)
TB1.config.VRO_gain(Gain_VRO)
TB1.config.I_amplitude = I_stim 


TB1.set_STIMn_to_elec(ELEC_GND)
TB1.set_CH1n_to_elec(ELEC_GND)

plt.figure()
for k in range (ELEC_min,ELEC_max+1):
    print("Resistor number: "+str(k))

    TB1.set_CH1p_to_elec(k)
    TB1.set_STIMp_to_elec(k)

    m1 = bm.EIS(fmin=fmin,fmax=fmax,n_pts=n_pts,settling_time=settling_time,NPeriods=NPeriods)
    TB1.attach_measure(m1)
    results = TB1.measure()
    plt.semilogx(results['freq'],results['mag_Z']) 


del TB1
plt.show()

