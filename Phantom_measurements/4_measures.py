import tobi
import bimms as bm
import matplotlib.pyplot as plt
import numpy as np
import time
import os

import pyeit.eit.bp as bp
import pyeit.eit.jac as jac
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh

DIR_res = "./results/"
if not os.path.isdir(DIR_res):
    os.mkdir(DIR_res)
ls = os.listdir(DIR_res)
print(len(ls), ls)

DIR_res += f"{len(ls)}/"
if not os.path.isdir(DIR_res):
    os.mkdir(DIR_res)


## Parameters
n_elec = 15
off_elec = 4
freq = 1e3
amp_AWG = 0.1
g_ch1 = 1

p1 = tobi.simple_pyeit_protocol(n_elec=n_elec, inj_offset=off_elec)



comment = f"PARAMETERS:\nn_elec={n_elec}\noff_elec={off_elec}\nfreq={freq} Hz\namp_AWG={amp_AWG}\ng_ch1{g_ch1}\nprotocole:\n"

for i, p in enumerate(p1):
    comment += f"{i}: {p}"

comment += "\nCOMMENT\n"
comment += input("add a comment to the measure:\n")

with open(DIR_res+"comment.txt", "w") as text_file:
    text_file.write(comment)


fname = DIR_res

tb1 = tobi.TomoBimms()
tb1.keep_on()


tb1.manual_config.excitation_signaling_mode("DIFF")
tb1.manual_config.wire_mode("4_WIRE")

tb1.manual_config.CH1_gain(g_ch1)
tb1.manual_config.CH2_gain(1)

#AWG_offset=.07

tb1.manual_config.AWG_amp(amp_AWG)


tb1.protocol = p1


m1 = bm.FrequentialSingleFrequency(freq=freq,nperiods=32 ,settling_time=0.001)

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
np.savetxt(fname+"v01.csv", v01)

tb1.clear_measures()
tb1.clear_results()


time.sleep(1)
tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
v02 = results.mag_Z
ds_0 = eit.solve(v02, v01, normalize=True)
tb1.clear_measures()
tb1.clear_results()
np.savetxt(fname+"v02.csv", v02)

###################################
####### measure dz -> E1 ##########
###################################
print("measure dz -> E1")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
vd1 = results.mag_Z
tb1.clear_measures()
tb1.clear_results()
np.savetxt(fname+"vd1.csv", vd1)


ds_1 = eit.solve(vd1, v01, normalize=True)



###################################
####### measure dz -> E4 ##########
###################################
print("measure dz -> E5")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
vd2 = results.mag_Z
tb1.clear_measures()
tb1.clear_results()
np.savetxt(fname+"vd2.csv", vd2)


ds_2 = eit.solve(vd2, v01, normalize=True)

###################################
####### measure dz -> E8 ##########
###################################
print("measure dz -> E9")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
vd3 = results.mag_Z
tb1.clear_measures()
tb1.clear_results()
np.savetxt(fname+"vd3.csv", vd3)

ds_3 = eit.solve(vd3, v01, normalize=True)


###################################
####### measure dz -> E8 ##########
###################################
print("measure dz -> E13")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure()
results.EIS()
vd4 = results.mag_Z
tb1.clear_measures()
tb1.clear_results()
np.savetxt(fname+"vd4.csv", vd4)

ds_4 = eit.solve(vd4, v01, normalize=True)

plt.figure()
plt.plot(v02)
plt.plot(vd1)
plt.plot(vd2)
plt.plot(vd3)
plt.plot(vd4)

plt.figure()
plt.plot(abs(v01 - v02))
plt.plot(abs(v01 - vd1))
plt.plot(abs(v01 - vd2))
plt.plot(abs(v01 - vd3))
plt.plot(abs(v01 - vd4))




# extract node, element, alpha
pts = mesh_obj.node
tri = mesh_obj.element

vmin, vmax = np.min([ds_1, ds_2, ds_3, ds_4]), np.max([ds_1, ds_2, ds_3, ds_4])
# draw
fig = plt.figure(figsize=(9, 9))
im = plt.tripcolor(pts[:, 0], pts[:, 1], tri, ds_0, vmin=vmin, vmax=vmax)
plt.title(r"Reconstituted $\Delta$ Conductivities")
plt.axis("equal")

fig.colorbar(im)

fig = plt.figure(figsize=(9, 9))
# reconstructed
ax1 = plt.subplot(222)
im = ax1.tripcolor(pts[:, 0], pts[:, 1], tri, ds_2, vmin=vmin, vmax=vmax)
ax1.set_title(r"Reconstituted 2nd scan")
ax1.axis("equal")

#fig.colorbar(im)

# fig.savefig('../doc/images/demo_bp.png', dpi=96)
#fig.colorbar(im)

# reconstructed
ax2 = plt.subplot(223)
im2 = ax2.tripcolor(pts[:, 0], pts[:, 1], tri, ds_3, vmin=vmin, vmax=vmax)
ax2.set_title(r"Reconstituted 3th scan")
ax2.axis("equal")

ax3 = plt.subplot(224)
im3 = ax3.tripcolor(pts[:, 0], pts[:, 1], tri, ds_4, vmin=vmin, vmax=vmax)
ax3.set_title(r"Reconstituted 4th scan")
ax3.axis("equal")

ax4 = plt.subplot(221)
im4 = ax4.tripcolor(pts[:, 0], pts[:, 1], tri, ds_1, vmin=vmin, vmax=vmax)
ax4.set_title(r"Reconstituted 1st scan")
ax4.axis("equal")
#fig.colorbar(im, ax=axes.ravel().tolist())
# fig.savefig('../doc/images/demo_bp.png', dpi=96)
plt.tight_layout()
fig.colorbar(im2)

fig.savefig(DIR_res+"im_same_scale.png")

fig = plt.figure(figsize=(9, 9))
# reconstructed
ax1 = plt.subplot(222)
im = ax1.tripcolor(pts[:, 0], pts[:, 1], tri, ds_2)
ax1.set_title(r"Reconstituted 2nd scan")
ax1.axis("equal")

#fig.colorbar(im)


# reconstructed
ax2 = plt.subplot(223)
im2 = ax2.tripcolor(pts[:, 0], pts[:, 1], tri, ds_3)
ax2.set_title(r"Reconstituted 3th scan")
ax2.axis("equal")

ax3 = plt.subplot(224)
im3 = ax3.tripcolor(pts[:, 0], pts[:, 1], tri, ds_4)
ax3.set_title(r"Reconstituted 4th scan")
ax3.axis("equal")

ax4 = plt.subplot(221)
im4 = ax4.tripcolor(pts[:, 0], pts[:, 1], tri, ds_1)
ax4.set_title(r"Reconstituted 1st scan")
ax4.axis("equal")
#fig.colorbar(im, ax=axes.ravel().tolist())
# fig.savefig('../doc/images/demo_bp.png', dpi=96)
plt.tight_layout()
fig.savefig(DIR_res+"im.png")


comment += "\n"+input("add a comment to the measure:\n")

with open(DIR_res+"comment.txt", "w") as text_file:
    text_file.write(comment)
plt.show()


