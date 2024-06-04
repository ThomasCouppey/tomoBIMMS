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

c_file = "sources/cuff_config.json"
fig_file = "figures/001_elec_mag_Z.png"

meas_file = "results/001_elec_mag_Z.json"

tb1 = tobi.TomoBimms()
tb1.keep_on()
tb1.load_config(c_file, manual=True)

tb1.manual_config.CH1_gain(100)

n_avg = 3
n_elec = 15
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
    for i in range(n_elec):
        p1.add_patern((i+1, e_ret), (i+1, e_ret))
tb1.protocol = p1

m1 = bm.Bode(fmin=1e3,fmax=1e6,n_pts=101,settling_time=0.01,nperiods=8, ID=i)
tb1.attach_measure(m1)

tb1.set_CH2p_to_elec(16)
tb1.set_CH2n_to_elec(15)


results1 = tb1.eit_measure()
results1.EIS()
results1.save(save=True, fname="results/elec.json")
labels = []
plt.figure(figsize=(10, 6))
plt.loglog(results1['freq'],results1['mag_Z'].T)
for i in range(n_elec):
    labels += [f"E{i+1}"]
#results1.save(save=True, fname="013_Omega_0.json")
plt.legend(labels)
plt.savefig(fig_file)
plt.show()
