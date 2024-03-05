import tobi
import bimms as bs
## Requiered: Two known resistors R1, R2
# E1 -- E2 --- R1 -- E3 -- E4
# E5 -- E6 --- R2 -- E7 -- E8
# E9 -- E10 --- R3 -- E11 -- E12
# E13 -- E14 --- R4 -- E15 -- E16

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


p1 = tobi.protocol()
p1.add_patern(inj=(1, 3), rec=(2, 4))
p1.add_patern(inj=(5, 7), rec=(6, 8))
p1.add_patern(inj=(9, 11), rec=(10, 12))
p1.add_patern(inj=(13, 15), rec=(14, 16))


p1.add_patern(inj=(3, 1), rec=(4, 2))
p1.add_patern(inj=(7, 5), rec=(8, 6))
p1.add_patern(inj=(11, 9), rec=(12, 10))
p1.add_patern(inj=(15, 13), rec=(16, 14))

p1.add_patern(inj=(2, 4), rec=(1, 3))
p1.add_patern(inj=(6, 8), rec=(5, 7))
p1.add_patern(inj=(10, 12), rec=(9, 11))
p1.add_patern(inj=(14, 16), rec=(13, 15))


p1.add_patern(inj=(4, 2), rec=(3, 1))
p1.add_patern(inj=(8, 6), rec=(7, 5))
p1.add_patern(inj=(12, 10), rec=(11, 9))
p1.add_patern(inj=(16, 14), rec=(15, 13))

"""
p1.add_patern(inj=(3, 1), rec=(4, 2))
p1.add_patern(inj=(10,4), rec=(9,5))
#p1.add_patern(inj=(1, 7), rec=(2, 6))
p1.add_patern(inj=(1, 7), rec=(2, 6))"""
tb1.protocol = p1

m1 = bs.FrequentialSingleFrequency(freq=1000,nperiods=8 ,settling_time=0.001)
tb1.attach_measure(m1)
results = tb1.eit_measure()
print(results.EIS())