import tobi
import time
import bimms as bm
import matplotlib.pyplot as plt

TB1 = tobi.TomoBimms()

Gain_IRO = 1
Gain_VRO = 1
fmin = 1000
fmax = 1e6
n_pts = 101
settling_time = 0.01
NPeriods = 8
I_stim = 10 #100uA excitation

ELEC_GND = 8
ELEC_min = 1
ELEC_max = 2

TB1.config.excitation_mode("G_EIS")
TB1.config.wire_mode("4_WIRE")
TB1.config.excitation_signaling_mode("DIFF")
TB1.config.excitation_coupling("DC")
TB1.config.G_EIS_gain("LOW")
TB1.config.recording_signaling_mode("DIFF")
TB1.config.recording_mode("V")  #Record voltage only
TB1.config.IRO_gain(Gain_IRO)
TB1.config.VRO_gain(Gain_VRO)
TB1.config.I_amplitude = I_stim 


TB1.set_STIMn_to_elec(ELEC_GND)
TB1.set_CH1n_to_elec(1)


N_electrode = 8
plt.figure()
for k in range (N_electrode):
    stim_n = k+1
    stm_p = ((k+1)%N_electrode)+1
    print("=========================")
    print("Stim_n: " +str(stim_n))
    print("Stim_p: " +str(stm_p))
    for j in range (N_electrode-3):
        V_neg = ((stm_p+j)%N_electrode)+1
        V_pos = ((V_neg)%N_electrode)+1
        print("V_neg: " +str(V_neg))
        print("V_pos: " +str(V_pos))

        TB1.set_STIMn_to_elec(stim_n)
        TB1.set_STIMp_to_elec(stm_p)

        TB1.set_CH1p_to_elec(V_neg)
        TB1.set_CH2p_to_elec(V_pos)

        m1 = bm.Bode(fmin=fmin,fmax=fmax,n_pts=n_pts,settling_time=settling_time,NPeriods=NPeriods)
        TB1.attach_measure(m1)
        results = TB1.measure()
        plt.semilogx(results['freq'],results['V_readout']) 

del TB1
plt.show()

