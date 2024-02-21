import tobi
import bimms as bs
import matplotlib.pyplot as plt
## Requiered: Two known resistors R1, R2
# E1 -- E2 --- R1 -- E3 -- E4
# E5 -- E6 --- R2 -- E7 -- E8
# E9 -- E10 --- R3 -- E11 -- E12
# E13 -- E14 --- R4 -- E15 -- E16

tb1 = tobi.TomoBimms()

tb1.config.excitation_sources("INTERNAL")
tb1.config.excitation_mode("G_EIS")
tb1.config.wire_mode("4_WIRE")
tb1.config.recording_mode("BOTH")
tb1.config.excitation_signaling_mode("DIFF")
tb1.config.recording_signaling_mode("AUTO")
tb1.config.excitation_coupling("DC")
tb1.config.G_EIS_gain = "LOW"
tb1.config.IRO_gain = 10
tb1.config.VRO_gain = 10
tb1.config.DC_feedback = False
tb1.config.V_amplitude = 100 # mV


p1 = tobi.simple_injection_protocole()


tb1.protocole = p1



#m1 = bs.TemporalSingleFrequency(freq = 10000,nperiods=100,phase = 90)

m1 = bs.FrequentialSingleFrequency(freq=1000,nperiods=16 ,settling_time=0.001)
tb1.attach_measure(m1)

results = tb1.eit_measure()
print(results.EIS())
results.save(save=True, fname="012_Omega_0.json")
"""
t = results['t']
ch1  = results['chan1_raw']
ch2 = results['chan2_raw']

plt.figure()
plt.plot(t,ch1)
plt.plot(t,ch2)
plt.show()"""