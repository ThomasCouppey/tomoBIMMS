import tobi
import bimms as bm
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import pyeit.eit.bp as bp
import pyeit.eit.jac as jac
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh
import time

fname = "unitary_tests/results/024_results"

def bandpass(data: np.ndarray, edges: list[float], sample_rate: float, poles: int = 5):
    sos = scipy.signal.butter(poles, edges, 'bandpass', fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data

## Requiered: Two known resistors R1, R2
# E1 -- E2 --- R1 -- E3 -- E4
# E5 -- E6 --- R2 -- E7 -- E8
# E9 -- E10 --- R3 -- E11 -- E12
# E13 -- E14 --- R4 -- E15 -- E16

tb1 = tobi.TomoBimms(1)
tb1.keep_on()


tb1.config_mode("MANUAL")
tb1.manual_config.waveform_gen("INTERNAL")
tb1.manual_config.excitation_source("CURRENT")
tb1.manual_config.I_source_gain("HIGH")
tb1.manual_config.wire_mode("4_WIRE")
tb1.manual_config.excitation_signaling_mode("DIFF")
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
tb1.manual_config.CH1_gain(100)
tb1.manual_config.CH2_gain(1)


amp_AWG = 1
AWG_offset=.09

tb1.test_config.AWG_amp(amp_AWG)
tb1.test_config.AWG_offset(AWG_offset)

n_avg = 3
n_elec = 16
off_elec = 3
p1 = tobi.simple_pyeit_protocol(n_elec=n_elec, inj_offset=off_elec)
tb1.protocol = p1

f = 10000
n_p = 30
m1 = bm.TemporalSingleFrequency(freq=f,nperiods=n_p,)


mesh_obj = mesh.create(n_elec, h0=0.08)
protocol_obj = protocol.create(n_elec, dist_exc=off_elec, step_meas=1, parser_meas="std")
eit = jac.JAC(mesh_obj, protocol_obj)
eit.setup(p=0.50, lamb=1e-3, method="kotre")


##############################
####### 1st measure ##########
##############################

t_lim = (5/f, (n_p-5)/f)

tb1.attach_measure(m1)
results = tb1.eit_measure(rec_kwargs={"clear_mstack":False})

results.fft(*t_lim)
v01 = results.amp_freq(f)
tb1.clear_measures()
tb1.clear_results()


tb1.clear_measures()
tb1.clear_results()


time.sleep(1)
tb1.attach_measure(m1)
results = tb1.eit_measure(rec_kwargs={"clear_mstack":False})
results.save(save=True, fname = fname+"_02.json")
tb1.clear_measures()
tb1.clear_results()

t_lim = (5/f, (n_p-5)/f)
results.fft(*t_lim)

v02 = results.amp_freq(f)
ds_0 = eit.solve(v02, v01, normalize=True)


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
results = tb1.eit_measure(rec_kwargs={"clear_mstack":False})

results.fft(*t_lim)
vd1 = results.amp_freq(f)
tb1.clear_measures()
tb1.clear_results()

ds_1 = eit.solve(vd1, v01, normalize=True)


###################################
####### measure dz -> E4 ##########
###################################
print("measure dz -> E5")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure(rec_kwargs={"clear_mstack":False})

results.fft(*t_lim)
vd5 = results.amp_freq(f)
tb1.clear_measures()
tb1.clear_results()


ds_5 = eit.solve(vd5, v01, normalize=True)

###################################
####### measure dz -> E8 ##########
###################################
print("measure dz -> E9")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure(rec_kwargs={"clear_mstack":False})

results.fft(*t_lim)
vd9 = results.amp_freq(f)
tb1.clear_measures()
tb1.clear_results()

ds_9 = eit.solve(vd9, v01, normalize=True)


###################################
####### measure dz -> E8 ##########
###################################
print("measure dz -> E13")
input("press enter")

tb1.attach_measure(m1)
results = tb1.eit_measure(rec_kwargs={"clear_mstack":False})

results.fft(*t_lim)
vd13 = results.amp_freq(f)
tb1.clear_measures()
tb1.clear_results()


ds_13 = eit.solve(vd13, v01, normalize=True)
#################################
####### Reconstruction ##########
#################################
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

vmin, vmax = min(ds_13), max(ds_13)
# draw
fig = plt.figure(figsize=(9, 9))
im = plt.tripcolor(pts[:, 0], pts[:, 1], tri, ds_0, vmin=vmin, vmax=vmax)
plt.title(r"Reconstituted $\Delta$ Conductivities")
plt.axis("equal")

fig.colorbar(im)

fig = plt.figure(figsize=(9, 9))
# reconstructed
ax1 = plt.subplot(221)
im = ax1.tripcolor(pts[:, 0], pts[:, 1], tri, ds_5, vmin=vmin, vmax=vmax)
ax1.set_title(r"Reconstituted $\Delta Z$ to N-E")
ax1.axis("equal")

#fig.colorbar(im)

# fig.savefig('../doc/images/demo_bp.png', dpi=96)
#fig.colorbar(im)

# reconstructed
ax2 = plt.subplot(222)
im2 = ax2.tripcolor(pts[:, 0], pts[:, 1], tri, ds_9, vmin=vmin, vmax=vmax)
ax2.set_title(r"Reconstituted $\Delta Z$ to E-E")
ax2.axis("equal")

ax3 = plt.subplot(223)
im3 = ax3.tripcolor(pts[:, 0], pts[:, 1], tri, ds_13, vmin=vmin, vmax=vmax)
ax3.set_title(r"Reconstituted $\Delta Z$ to E-S")
ax3.axis("equal")

ax4 = plt.subplot(224)
im4 = ax4.tripcolor(pts[:, 0], pts[:, 1], tri, ds_1, vmin=vmin, vmax=vmax)
ax4.set_title(r"Reconstituted $\Delta Z$ to E-W")
ax4.axis("equal")
#fig.colorbar(im, ax=axes.ravel().tolist())
# fig.savefig('../doc/images/demo_bp.png', dpi=96)
plt.tight_layout()
plt.show()