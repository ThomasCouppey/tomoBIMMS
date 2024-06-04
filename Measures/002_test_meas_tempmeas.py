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
c_file = "sources/cuff_config.json"
fig_file = "figures/002_elec_mag_Z.png"

meas_file = "results/002_elec_mag_Z.json"

tb1 = tobi.TomoBimms()
tb1.keep_on()
tb1.load_config(c_file, manual=True)

tb1.manual_config.CH1_gain(100)

n_elec = 8
n_rec = n_elec -3
p0 = tobi.simple_injection_protocol(n_elec=n_elec, start_elec=1)+8
p1 = tobi.protocol()
N_test = 10

for _ in range(N_test):
    for i in range(n_rec):
        print(p0[i])
        p1.add_patern(*p0[i])

"""
#p1.add_patern(inj=(2, 4), rec=(3, 5))
#p1.add_patern(inj=(1, 3), rec=(2, 4))
#p1.add_patern(inj=(1, 3), rec=(2, 4))


p1.add_patern(inj=(3, 1), rec=(4, 2))
p1.add_patern(inj=(10,4), rec=(9,5))
#p1.add_patern(inj=(1, 7), rec=(2, 6))
p1.add_patern(inj=(1, 7), rec=(2, 6))

n_elec = 8

p1 = tobi.simple_injection_protocol(n_elec=n_elec, inj_offset=2)
p1.change_electrode_id(0, 8)
"""
tb1.protocol = p1

#m1 = bm.FrequentialSingleFrequency(freq=1000,nperiods=8 ,settling_time=0.001)
f = 1000
n_p = 15 + 4
m1 = bm.TemporalSingleFrequency(freq=f,nperiods=n_p,)
v1 = np.zeros(len(p1))
v1 = np.zeros(len(p1))




##############################
####### 1st measure ##########
##############################
tb1.attach_measure(m1)

results = tb1.eit_measure(rec_kwargs={"clear_mstack":False})
del tb1
#results = tb1.measure()

#results["chan1_raw"] = bandpass(results["chan1_raw"], [f/5, 10*f], results["sample_rate"], 2)

t_lim = (4/f, (n_p-3)/f)
results.crop_time(*t_lim)

# Apply a 10-50 Hz high-pass filter to the original data


colors = ["r", "g", "b", "y", "k", "r", "g", "b", "y", "k", "r", "g", "b", "y", "k"]
n_plot=0
results.fft(*t_lim)
for i in range(N_test):
    for j in range(n_elec-3):
        #print(i, j, n_plot)
        v = results['chan1_t'][n_plot,:]
        c = colors[j]
        #print(v, c)
        plt.figure(100)
        plt.plot(results["t"],v, color=c)
        plt.figure(2)
        V = np.abs(results['chan1_f'][n_plot,:])/results["n_sample"]
        print(np.shape(V), np.shape(results['chan1_f']), np.shape(results['chan1_t']))
        print(np.shape(V), np.shape(results['f']), np.shape(results['t']))
        I = np.where(results["f"]>100)
        plt.plot(results["f"][I],V[I], color=c)
        n_plot += 1



plt.figure(2)
plt.xlim((100,15000))

#plt.plot(results["t_raw"],results['chan1_raw'].T, ":")



v1 = results['chan1_t'].max(axis=1) - results['chan1_t'].min(axis=1)
v12 = np.abs(results['chan1_f']/results["n_sample"]).max(axis=1)
v13 = results.amp_freq(f)
print(v13)

for i in range(n_rec):
    plt.figure(11)
    v = v13[i::n_rec]
    I = i+np.ones(len(v))
    plt.plot(I, v, ".")
plt.savefig(fig_file)
plt.show()
exit()
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

plt.show()
exit()