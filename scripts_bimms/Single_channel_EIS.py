"""
	Python script to perform Potentiostat EIS with BIMMS.
	Authors: Florian Kolbl / Louis Regnacq
	(c) ETIS - University Cergy-Pontoise
		IMS - University of Bordeaux
		CNRS

	Requires:
		Python 3.6 or higher
		Analysis_Instrument - class handling Analog Discovery 2 (Digilent)

"""
import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

## Parameter to set before measurment
galvanostat = True      #Measurment type: True  = galvanostat, False = potentiostat

fmin = 1000             #Start Frequency (Hz)
fmax = 10e6             #Stop Frequency (Hz)
n_pts = 200             #Number of frequency points
amp_pot = 0.1           #amplitude for potentiostat(V)
amp_gal = 0.01          #amplitude for galvanostat(mA)

settling_time = 0.01    #Settling time between points
NPeriods = 32           #Number of period per frequency points
two_wires = True       #Connection to the DUT mode: True  = 2wires, False = 4wires

out_dir = 'csv/'        #output directory
keep_on = False         #Keep bimms configuration (to debug with waveform)

BS = bm.BIMMS()

if keep_on:
    BS.keep_on()

if galvanostat:
    amp = amp_gal
    output_file_name = out_dir + "galvanostat_EIS.csv"
    freq, gain_mes, phase_mes = BS.galvanostat_EIS(fmin=fmin, fmax=fmax, n_pts=n_pts, I_amp=amp, I_offset=0, settling_time=settling_time, NPeriods=NPeriods,
        V_range=10.0, V_offset=0.0, differential=False,High_gain=True, two_wires=two_wires, coupling='DC', DC_feedback=True, apply_cal=True)

else:
    amp = amp_pot
    output_file_name = out_dir+"potentiostat_EIS.csv"
    freq, gain_mes, phase_mes = BS.potentiostat_EIS(fmin=fmin, fmax=fmax, n_pts=n_pts, V_amp=amp, V_offset=0, settling_time=settling_time, NPeriods=NPeriods,
        differential=False, two_wires=two_wires, coupling='DC', apply_cal=True)


#dump data to csv
data = np.asarray([freq,gain_mes,phase_mes])
data = np.transpose(data)
np.savetxt(output_file_name, data, delimiter=",")

plt.figure(1)
plt.subplot(211)
plt.semilogx(freq,gain_mes)
plt.ylim(0, 1.1*max(gain_mes))
plt.xlabel('Frequency ($Hz$)')
plt.ylabel('Impedance ($\Omega$)')
plt.grid()
plt.subplot(212)
plt.semilogx(freq,phase_mes)
plt.grid()
plt.xlabel('Frequency ($Hz$)')
plt.ylabel('Phase ($°$)')

plt.show()


