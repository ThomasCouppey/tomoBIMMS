import tobi
import bimms as bm
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import pyeit.eit.bp as bp
import pyeit.eit.jac as jac
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh

def bandpass(data: np.ndarray, edges: list[float], sample_rate: float, poles: int = 5):
    sos = scipy.signal.butter(poles, edges, 'bandpass', fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data

## Requiered: Two known resistors R1, R2
# E1 -- E2 --- R1 -- E3 -- E4
# E5 -- E6 --- R2 -- E7 -- E8
# E9 -- E10 --- R3 -- E11 -- E12
# E13 -- E14 --- R4 -- E15 -- E16

tb1 = tobi.TomoBimms()
tb1.keep_on()

tb1.config_mode("TEST")
tb1.test_config.waveform_gen("INTERNAL")
tb1.test_config.excitation_source("CURRENT")
tb1.test_config.I_source_gain("HIGH")
tb1.test_config.wire_mode("4_WIRE")
tb1.test_config.excitation_signaling_mode("SE")
tb1.test_config.excitation_coupling("DC")
tb1.test_config.DC_feedback(False)
tb1.test_config.Enable_Isource(True)

tb1.test_config.CHx_to_Scopex("CH1")
tb1.test_config.CH1_coupling("DC")
tb1.test_config.CH2_coupling("DC")
tb1.test_config.TIA_coupling("DC")
tb1.test_config.connect_TIA(False)
tb1.test_config.TIA_to_CH2(False)
tb1.test_config.TIA_NEG("GND")
tb1.test_config.CH1_gain(5)
tb1.test_config.CH2_gain(1)

amp_AWG = 1
#AWG_offset=.07

tb1.test_config.AWG_amp(amp_AWG)
#tb1.test_config.AWG_offset(AWG_offset)


"""p1 = tobi.protocole()
p1.add_patern(inj=(1, 6), rec=(2, 5))
p1.add_patern(inj=(1, 6), rec=(2, 3))"""
#p1.add_patern(inj=(2, 4), rec=(3, 5))
#p1.add_patern(inj=(1, 3), rec=(2, 4))
#p1.add_patern(inj=(1, 3), rec=(2, 4))


"""p1.add_patern(inj=(3, 1), rec=(4, 2))
p1.add_patern(inj=(10,4), rec=(9,5))
#p1.add_patern(inj=(1, 7), rec=(2, 6))
p1.add_patern(inj=(1, 7), rec=(2, 6))"""

n_elec = 8

p1 = tobi.simple_injection_protocole(n_elec=n_elec, inj_offset=2)
p1.change_electrode_id(0, 8)
tb1.protocole = p1

#m1 = bm.FrequentialSingleFrequency(freq=1000,nperiods=8 ,settling_time=0.001)
f = 1000
n_p = 10 + 4
m1 = bm.TemporalSingleFrequency(freq=f,nperiods=n_p,)
v1 = np.zeros(len(p1))
v1 = np.zeros(len(p1))




##############################
####### 1st measure ##########
##############################
tb1.attach_measure(m1)
results = tb1.eit_measure(rec_kwargs={"clear_mstack":False})
#results = tb1.measure()


t = results['t']
ch1  = results['chan1_raw']



# Load sample data from a WAV file
sample_rate = 1/(t[1] - t[0])
I = np.argwhere((t>2/f)&(t<(n_p-3)/f))[:,0]


# Apply a 10-50 Hz high-pass filter to the original data
ch1_filter = bandpass(ch1, [f/5, 10*f], sample_rate, 2)
plt.figure()
    #plt.plot(t,ch1-np.mean(ch1))
plt.plot(t,ch1_filter.T, ":")
plt.plot(t[I],ch1_filter.T[I, :])
v2 = ch1_filter[:,I].max(axis=1) - ch1_filter[:,I].min(axis=1)
print(v2)
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
#results = tb1.measure()


t = results['t']
ch1  = results['chan1_raw']



# Load sample data from a WAV file
sample_rate = 1/(t[1] - t[0])
I = np.argwhere((t>2/f)&(t<(n_p-3)/f))[:,0]


# Apply a 10-50 Hz high-pass filter to the original data
ch1_filter = bandpass(ch1, [f/5, 10*f], sample_rate, 2)
plt.figure()
    #plt.plot(t,ch1-np.mean(ch1))
plt.plot(t,ch1_filter.T, ":")
plt.plot(t[I],ch1_filter.T[I, :])
v1 = ch1_filter[:,I].max(axis=1) - ch1_filter[:,I].min(axis=1)
print(v1)
tb1.clear_measures()
tb1.clear_results()

#################################
####### Reconstruction ##########
#################################
plt.figure()
plt.plot(v1)
plt.plot(v2)

mesh_obj = mesh.create(n_elec, h0=0.1)
protocol_obj = protocol.create(n_elec, dist_exc=2, step_meas=1, parser_meas="std")
"""eit = bp.BP(mesh_obj, protocol_obj)
eit.setup(weight="none")
# the normalize for BP when dist_exc>4 should always be True
ds = eit.solve(v2, v1, normalize=True)
"""
eit = jac.JAC(mesh_obj, protocol_obj)
eit.setup(p=0.50, lamb=1e-3, method="kotre")
ds = eit.solve(v2, v1, normalize=True)

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

plt.show()
exit()