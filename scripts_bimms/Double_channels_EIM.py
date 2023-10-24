"""
	Python script to perform galvanostat EIS with BIMMS.
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

f = 1000               #Frequency (Hz)
n_pts = 200             #Number of frequency points
amp_pot = 0.1           #amplitude for potentiostat(V)
amp_gal = 0.01          #amplitude for galvanostat(mA)

settling_time = 0.05    #Settling time between points
NPeriods = 4           #Number of period per frequency points


two_wires = False       #Connection to the DUT mode: True  = 2wires, False = 4wires
out_dir = 'csv/'        #Output directory
keep_on = True         #Keep bimms configuration (to debug with waveform)



BS = bm.BIMMS()
if keep_on:
    BS.keep_on()

BS.set_STM32_idle()
if galvanostat:
    output_file_name = out_dir + "double_galvano.csv"
    amp = amp_gal
    unit = 1e3
    BS.set_current_excitation(coupling = 'AC', differential_stim = True, DC_feedback = False, Internal_AWG = True, High_gain = True)
else:
    output_file_name = out_dir + "double_potentio.csv"
    amp = amp_pot
    unit = 1
    BS.set_voltage_excitation(coupling = 'AC', differential_stim = True, Internal_AWG = True)
    #BS.set_potentiostat_EIS_config(differential = True, two_wires = False, coupling = 'AC',voltage_gain=10,current_gain = 1)

BS.set_recording_channel_1()
BS.set_recording_channel_2()
BS.disconnect_TIA_from_CH2()
BS.set_config()
data = []
it = [k for k in range(16)]

for i in it:
    gain, phase, gain_ch1 = BS.interface.single_frequency_gain_phase(f,dB = False, settling_time=settling_time,
        amp = amp, offset = 0.0, Nperiods = NPeriods,Vrange_CH1 = 1.0,Vrange_CH2 = 1.0, 
        offset_CH1 = 0.0,offset_CH2 = 0.0, verbose = False)


    print([gain, phase, gain_ch1])

    Z1 = gain_ch1 * amp * unit
    Z2 = gain*Z1
    print(Z1, Z2)
    #dump data to csv
    data += [[Z1, Z2]]

del BS

np.savetxt(output_file_name, np.transpose(data), delimiter=",")

plt.plot(it,data)
plt.show()
