import tobi
import bimms as bs
## Requiered: Two known resistors R1, R2
# E6 -- E7 --- R1 -- E1 -- E2 
# E9 -- E10 --- R2 -- E4 -- E5
tb1 = tobi.TomoBimms()

tb1.config.excitation_sources("INTERNAL")
tb1.config.excitation_mode("P_EIS")
tb1.config.wire_mode("4_WIRE")
tb1.config.recording_mode("BOTH")
tb1.config.excitation_signaling_mode("SE")
tb1.config.recording_signaling_mode("AUTO")
tb1.config.excitation_coupling("DC")
tb1.config.G_EIS_gain = "LOW"
tb1.config.IRO_gain = 1
tb1.config.VRO_gain = 1
tb1.config.DC_feedback = False
tb1.config.V_amplitude = 100 # mV


p1 = tobi.protocole()
p1.add_patern(inj=(1, 7), rec=(2, 6))
p1.add_patern(inj=(10,4), rec=(9,5))
#p1.add_patern(inj=(1, 7), rec=(2, 6))
p1.add_patern(inj=(1, 7), rec=(2, 6))
tb1.protocole = p1

m1 = bs.FrequentialSingleFrequency(freq=1000,nperiods=10 ,settling_time=0.001)
tb1.attach_measure(m1)
results = tb1.eit_measure()
print(results.EIS())