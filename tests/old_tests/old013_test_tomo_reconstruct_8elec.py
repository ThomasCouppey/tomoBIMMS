import tobi
import bimms as bm
import matplotlib.pyplot as plt
import numpy as np
import time

import pyeit.eit.bp as bp
import pyeit.eit.jac as jac
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh
## Requiered: Two known resistors R1, R2
# E1 -- E2 --- R1 -- E3 -- E4
# E5 -- E6 --- R2 -- E7 -- E8
# E9 -- E10 --- R3 -- E11 -- E12
# E13 -- E14 --- R4 -- E15 -- E16
n_elec = 8
tb1 = tobi.TomoBimms()
"""
tb1.config.excitation_sources("INTERNAL")
tb1.config.excitation_mode("G_EIS")
tb1.config.wire_mode("4_WIRE")
tb1.config.recording_mode("V")
tb1.config.excitation_signaling_mode("DIFF")
tb1.config.recording_signaling_mode("DIFF")
tb1.config.excitation_coupling("DC")
tb1.config.G_EIS_gain = "LOW"
tb1.config.IRO_gain = 5
tb1.config.VRO_gain = 5
tb1.config.DC_feedback = False
tb1.config.I_amplitude = 100 # uA
tb1.config.V_amplitude = 100 # mV
"""
tb1.config_mode("TEST")

tb1.manual_config.waveform_gen("INTERNAL")
tb1.manual_config.excitation_source("CURRENT")
tb1.manual_config.I_source_gain("HIGH")
tb1.manual_config.wire_mode("4_WIRE")
tb1.manual_config.excitation_signaling_mode("SE")
tb1.manual_config.excitation_coupling("DC")
tb1.manual_config.DC_feedback(False)
tb1.manual_config.Enable_Isource(True)

tb1.manual_config.CHx_to_Scopex("CH1")
tb1.manual_config.CH1_coupling("DC")
tb1.manual_config.CH2_coupling("DC")
tb1.manual_config.TIA_coupling("DC")
tb1.manual_config.connect_TIA(False)
tb1.manual_config.TIA_to_CH2(False)
tb1.manual_config.TIA_NEG("GND")
tb1.manual_config.CH1_gain(10)
tb1.manual_config.CH2_gain(10)

amp_AWG = 1
tb1.manual_config.AWG_amp(amp_AWG)
#p1 = tobi.simple_injection_protocol(n_elec=n_elec)


p1 = tobi.protocol()
for i in range(1):
    p1.add_patern(inj=(2, 3), rec=(4,3))
    """p1.add_patern(inj=(3, 4), rec=(5, 6))
    p1.add_patern(inj=(1, 2), rec=(5, 6))
    p1.add_patern(inj=(3, 4), rec=(3, 4))"""


tb1.protocol = p1

#m1 = bm.FrequentialSingleFrequency(freq=1000,nperiods=16 ,settling_time=0.001)
m1 = bm.TemporalSingleFrequency(freq = 1000,nperiods=16)
tb1.attach_measure(m1)

tb1.set_CH2p_to_elec(16)
tb1.set_CH2n_to_elec(15)

for i in range(5):

    tb1.set_STIMn_to_elec(1)
    tb1.set_STIMp_to_elec(2)
    tb1.set_CH1n_to_elec(5)
    tb1.set_CH1p_to_elec(6)

    """tb1.set_STIMn_to_elec(1)
    tb1.set_STIMp_to_elec(4)
    tb1.set_CH1n_to_elec(5)
    tb1.set_CH1p_to_elec(8)"""

    results1 = tb1.measure(clear_mstack=False)
    results1.save(save=True, fname="013_Omega_0.json")
    tb1.clear_results()

    tb1.set_STIMn_to_elec(3)
    tb1.set_STIMp_to_elec(4)
    tb1.set_CH1n_to_elec(7)
    tb1.set_CH1p_to_elec(8)

    """tb1.set_STIMn_to_elec(2)
    tb1.set_STIMp_to_elec(7)
    tb1.set_CH1n_to_elec(6)
    tb1.set_CH1p_to_elec(3)"""



    results2 = tb1.measure(clear_mstack=False)
    results2.save(save=True, fname="013_Omega_1.json")
    tb1.clear_results()
    t = results1['t']
    ch1  = results1['chan1_raw']
    ch2 = results2['chan1_raw']
    time.sleep(1)

    plt.figure(1)
    plt.plot(t,ch1-np.mean(ch1))
    plt.figure(2)
    plt.plot(t,ch2-np.mean(ch2))
plt.show()
exit()

results1.EIS()
results2.EIS()
err = results1.mag_Z - results2.mag_Z
print(np.shape(results1.mag_Z))
print(np.shape(results2.mag_Z))
print(err)
print(err/results1.mag_Z)
print(max(err))




# set-up data
v0 = results1.mag_Z#set_up_data(res1, key=1)
v1 = results2.mag_Z#set_up_data(res2, key=1)

exit()
mesh_obj = mesh.create(n_elec, h0=0.05)
protocol_obj = protocol.create(n_elec, dist_exc=1, step_meas=1, parser_meas="std")
"""eit = bp.BP(mesh_obj, protocol_obj)
eit.setup(weight="none")
# the normalize for BP when dist_exc>4 should always be True
ds = eit.solve(v1, v0, normalize=True)"""

eit = jac.JAC(mesh_obj, protocol_obj)
self.eit.setup(p=0.5, lamb=0.4, method='kotre')
ds = eit.solve(v1, v0, normalize=False)

# extract node, element, alpha
pts = mesh_obj.node
tri = mesh_obj.element

# draw
fig = plt.figure(figsize=(11, 9))
# reconstructed
im = plt.tripcolor(pts[:, 0], pts[:, 1], tri, ds)
plt.title(r"Reconstituted $\Delta$ Conductivities")
plt.axis("equal")
# fig.savefig('../doc/images/demo_bp.png', dpi=96)
fig.colorbar(im)
#plt.savefig(DIR_res+"reconstruction.png", dpi=500)
plt.tight_layout()
plt.show()
