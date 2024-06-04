import tobi
import bimms as bm
import matplotlib.pyplot as plt
import numpy as np

import pyeit.eit.bp as bp
import pyeit.eit.jac as jac
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh
## Requiered: Two known resistors R1, R2
# E1 -- E2 --- R1 -- E3 -- E4
# E5 -- E6 --- R2 -- E7 -- E8
# E9 -- E10 --- R3 -- E11 -- E12
# E13 -- E14 --- R4 -- E15 -- E16
tb1 = tobi.TomoBimms()
tb1.keep_on()

tb1.config_mode("MANUAL")
tb1.manual_config.waveform_gen("INTERNAL")
tb1.manual_config.excitation_source("VOLTAGE")
tb1.manual_config.I_source_gain("HIGH")
tb1.manual_config.wire_mode("4_WIRE")
tb1.manual_config.excitation_signaling_mode("DIFF")
tb1.manual_config.excitation_coupling("DC")
tb1.manual_config.DC_feedback(False)
tb1.manual_config.Enable_Isource(True)

tb1.manual_config.CHx_to_Scopex("BOTH")
tb1.manual_config.CH1_coupling("DC")
tb1.manual_config.CH2_coupling("DC")
tb1.manual_config.TIA_coupling("DC")
tb1.manual_config.connect_TIA(True)
tb1.manual_config.TIA_to_CH2(True)
tb1.manual_config.TIA_NEG("Ineg")
tb1.manual_config.CH1_gain(1)
tb1.manual_config.CH2_gain(1)

amp_AWG = 1
#AWG_offset=.07

tb1.manual_config.AWG_amp(amp_AWG)
n_avg = 3
n_elec = 9
off_elec = 3
p1 = tobi.simple_pyeit_protocol(n_elec=n_elec, inj_offset=off_elec)
tb1.protocol = p1


"""
p1 = tobi.simple_injection_protocol(n_elec=n_elec)

"""
p0 = tobi.simple_injection_protocol(n_elec=n_elec, start_elec=1)
p1 = tobi.protocol()
N_test = 1
e_ret = 16
for _ in range(N_test):
    for i in range(1):
        p1.add_patern((i+3, e_ret), (i+3, e_ret))
        print(p1[i])
tb1.protocol = p1

m1 = bm.Bode(fmin=1e3,fmax=1e6,n_pts=101,settling_time=0.01,nperiods=8, ID=i)
tb1.attach_measure(m1)

tb1.set_CH2p_to_elec(16)
tb1.set_CH2n_to_elec(15)


results1 = tb1.eit_measure()
results1.EIS()
print(results1.keys())
print(results1['freq'].shape,results1['mag_Z'].shape)
results1.save(save=True, fname="unitary_tests/results/elec.json")
labels = []

plt.loglog(results1['freq'],results1['mag_Z'].T)
for i in range(n_elec):
    labels += [f"E{i+1}"]
#results1.save(save=True, fname="013_Omega_0.json")
plt.legend(labels)
plt.show()

"""
#
tb1.clear_results()
input("Change the impedance and press a key")
results2 = tb1.eit_measure()
results2.save(save=True, fname="013_Omega_1.json")
results2.EIS()

err = results1.mag_Z - results2.mag_Z
print(np.shape(results1.mag_Z))
print(np.shape(results2.mag_Z))
print(results1.mag_Z)
print(results2.mag_Z)

print()
print(err)
print(err/results1.mag_Z)
print(max(err))
"""



exit()

# set-up data
v0 = results1.mag_Z#set_up_data(res1, key=1)
v1 = results2.mag_Z#set_up_data(res2, key=1)


mesh_obj = mesh.create(n_elec, h0=0.05)
protocol_obj = protocol.create(n_elec, dist_exc=1, step_meas=1, parser_meas="std")
eit = bp.BP(mesh_obj, protocol_obj)
eit.setup(weight="none")
# the normalize for BP when dist_exc>4 should always be True
ds = eit.solve(v1, v0, normalize=True)
"""
eit = jac.JAC(mesh_obj, protocol_obj)
eit.setup(p=0.50, lamb=1e-3, method="kotre")
ds = eit.solve(v1, v0, normalize=False)"""

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
