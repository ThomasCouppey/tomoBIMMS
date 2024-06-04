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

c_file = "sources/cuff_config.json"
fig_file = "figures/004_elec_mag_Z.png"

meas_file = "results/004_elec_mag_Z"

tb1 = tobi.TomoBimms()
tb1.keep_on()
tb1.load_config(c_file, manual=True)

tb1.manual_config.CH1_gain(50)


n_avg = 3
n_elec = 8
off_elec = 2
p1 = tobi.simple_pyeit_protocol(n_elec=n_elec, inj_offset=off_elec)
tb1.protocol = p1+8

m1 = bm.FrequentialSingleFrequency(freq=10000,nperiods=32 ,settling_time=0.001)

mesh_obj = mesh.create(n_elec, h0=0.04)
protocol_obj = protocol.create(n_elec, dist_exc=off_elec, step_meas=1, parser_meas="std")
eit = jac.JAC(mesh_obj, protocol_obj)
eit.setup(p=0.50, lamb=1e-3, method="kotre")


##############################
####### 1st measure ##########
##############################
tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
v01 = results.mag_Z
results.save(save=True, fname=meas_file+"0.json")


tb1.clear_measures()
tb1.clear_results()


time.sleep(1)
tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
v02 = results.mag_Z
ds_0 = eit.solve(v02, v01, normalize=True)
results.save(save=True, fname=meas_file+"1.json")

tb1.clear_measures()
tb1.clear_results()

"""
for i, p in enumerate(p1):
    if v2[i]<1e-5:
        print(p)
exit()
"""
###################################
####### measure dz -> E1 ##########
###################################
print("measure dz -> E1")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
vd1 = results.mag_Z
results.save(save=True, fname=meas_file+"1.json")

tb1.clear_measures()
tb1.clear_results()

ds_1 = eit.solve(vd1, v01, normalize=True)


###################################
####### measure dz -> E4 ##########
###################################
print("measure dz -> E5")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
vd5 = results.mag_Z
results.save(save=True, fname=meas_file+"5.json")

tb1.clear_measures()
tb1.clear_results()


ds_5 = eit.solve(vd5, v01, normalize=True)

###################################
####### measure dz -> E8 ##########
###################################
print("measure dz -> E9")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
vd9 = results.mag_Z
results.save(save=True, fname=meas_file+"9.json")

tb1.clear_measures()
tb1.clear_results()

ds_9 = eit.solve(vd9, v01, normalize=True)


###################################
####### measure dz -> E8 ##########
###################################
print("measure dz -> E13")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
vd13 = results.mag_Z
results.save(save=True, fname=meas_file+"13.json")

tb1.clear_measures()
tb1.clear_results()

ds_13 = eit.solve(vd13, v01, normalize=True)

plt.figure()
plt.plot(v02)
plt.plot(vd1)
plt.plot(vd5)
plt.plot(vd9)
plt.plot(vd13)

plt.figure()
plt.plot(abs(v01 - v02))
plt.plot(abs(v01 - vd1))
plt.plot(abs(v01 - vd5))
plt.plot(abs(v01 - vd9))
plt.plot(abs(v01 - vd13))



# extract node, element, alpha
pts = mesh_obj.node
tri = mesh_obj.element

vmin, vmax = np.min([ds_1, ds_5, ds_9, ds_13]), np.max([ds_1, ds_5, ds_9, ds_13])
# draw
fig = plt.figure(figsize=(9, 9))
im = plt.tripcolor(pts[:, 0], pts[:, 1], tri, ds_0, vmin=vmin, vmax=vmax)
plt.title(r"Reconstituted $\Delta$ Conductivities")
plt.axis("equal")

fig.colorbar(im)

fig = plt.figure(figsize=(9, 9))
# reconstructed
ax1 = plt.subplot(222)
im = ax1.tripcolor(pts[:, 0], pts[:, 1], tri, ds_5, vmin=vmin, vmax=vmax)
ax1.set_title(r"Reconstituted 2nd scan")
ax1.axis("equal")

#fig.colorbar(im)

# fig.savefig('../doc/images/demo_bp.png', dpi=96)
#fig.colorbar(im)

# reconstructed
ax2 = plt.subplot(223)
im2 = ax2.tripcolor(pts[:, 0], pts[:, 1], tri, ds_9, vmin=vmin, vmax=vmax)
ax2.set_title(r"Reconstituted 3th scan")
ax2.axis("equal")

ax3 = plt.subplot(224)
im3 = ax3.tripcolor(pts[:, 0], pts[:, 1], tri, ds_13, vmin=vmin, vmax=vmax)
ax3.set_title(r"Reconstituted 4th scan")
ax3.axis("equal")

ax4 = plt.subplot(221)
im4 = ax4.tripcolor(pts[:, 0], pts[:, 1], tri, ds_1, vmin=vmin, vmax=vmax)
ax4.set_title(r"Reconstituted 1st scan")
ax4.axis("equal")
#fig.colorbar(im, ax=axes.ravel().tolist())
# fig.savefig('../doc/images/demo_bp.png', dpi=96)
plt.subplots_adjust(bottom=0.1, right=1, left=0)
cax = plt.axes((0.1, 0.025, 0.8, 0.03))
plt.colorbar(im4, cax=cax, orientation='horizontal')
plt.savefig(fig_file)
plt.show()