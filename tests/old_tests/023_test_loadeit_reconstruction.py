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

fname = "unitary_tests/sources/022_results"

def bandpass(data: np.ndarray, edges: list[float], sample_rate: float, poles: int = 5):
    sos = scipy.signal.butter(poles, edges, 'bandpass', fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data

#m1 = bm.FrequentialSingleFrequency(freq=1000,nperiods=8 ,settling_time=0.001)
f = 10000
n_p = 30 
m1 = bm.TemporalSingleFrequency(freq=f,nperiods=n_p,)





##############################
####### 1st measure ##########
##############################


results = bm.load_any(data=fname+"_01.json")
#results = tb1.measure()

t_lim = (5/f, (n_p-5)/f)
results.fft(*t_lim)

v01 = results.amp_freq(f)
print(v01)
exit()
results = bm.temporal_results()
results.load(fname=fname+"_02.json")


t_lim = (5/f, (n_p-5)/f)
results.fft(*t_lim)

v02 = results.amp_freq(f)

tb1.clear_measures()
tb1.clear_results()

"""
for i, p in enumerate(p1):
    if v2[i]<1e-5:
        print(p)
exit()
"""
##############################
####### 2nd measure ##########
##############################

input("press enter")
tb1.attach_measure(m1)
results = tb1.eit_measure(rec_kwargs={"clear_mstack":False})
results.save(save=True, fname = fname+"_1.json")

results.fft(*t_lim)
v2 = results.amp_freq(f)

tb1.clear_measures()
tb1.clear_results()

#################################
####### Reconstruction ##########
#################################
plt.figure()
plt.plot(abs(v01 - v02))
plt.plot(abs(v01 - v2))

mesh_obj = mesh.create(n_elec, h0=0.1)
protocol_obj = protocol.create(n_elec, dist_exc=off_elec, step_meas=1, parser_meas="std")

"""
eit = bp.BP(mesh_obj, protocol_obj)
eit.setup(weight="none")
# the normalize for BP when dist_exc>4 should always be True

"""
eit = jac.JAC(mesh_obj, protocol_obj)
eit.setup(p=0.50, lamb=1e-3, method="kotre")


ds = eit.solve(v2, v01, normalize=True)
ds_noise = eit.solve(v02, v01, normalize=True)

# extract node, element, alpha
pts = mesh_obj.node
tri = mesh_obj.element

vmin, vmax = min(ds), max(ds)
# draw
fig = plt.figure(figsize=(9, 9))

# reconstructed
ax1 = plt.subplot(211)
im = ax1.tripcolor(pts[:, 0], pts[:, 1], tri, ds, vmin=vmin, vmax=vmax)
ax1.set_title(r"Reconstituted $\Delta$ Conductivities")
ax1.axis("equal")

fig.colorbar(im)

# fig.savefig('../doc/images/demo_bp.png', dpi=96)
#fig.colorbar(im)

# reconstructed
ax2 = plt.subplot(212)
im2 = ax2.tripcolor(pts[:, 0], pts[:, 1], tri, ds_noise, vmin=vmin, vmax=vmax)
ax2.set_title(r"Reconstituted $\Delta$ Conductivities + Noise")
ax2.axis("equal")
#fig.colorbar(im, ax=axes.ravel().tolist())
# fig.savefig('../doc/images/demo_bp.png', dpi=96)
plt.tight_layout()
plt.show()