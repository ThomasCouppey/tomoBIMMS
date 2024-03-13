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
import os
import datetime
import json
import time

## Parameter to set before measurment
t0 = time.time()
galvanostat = False      #Measurment type: True  = galvanostat, False = potentiostat

freqs = [100, 500, 1000, 10000, 50000]    #Measurment Frequencies (Hz)
amp_pot = 0.1               #Amplitude for potentiostat(V)
amp_gal = 0.01              #Amplitude for galvanostat(mA)
offset = 0

gain_current = 20
gain_voltage = gain_current

settling_time = 0.01    #Settling time between points
NPeriods = 32           #Number of period per frequency points
two_wires = False       #Connection to the DUT mode: True  = 2wires, False = 4wires
differential = False
High_gain=True


keep_on = False         #Keep bimms configuration (to debug with waveform)

# Tomography
Nelec = 8


out_dir = 'csv/'        #output directory
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
out_dir += "EIT_Single_Manual_Switch/"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S/")
out_dir += date
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


BS = bm.BIMMS()

if keep_on:
    BS.keep_on()

if not galvanostat:
    BS.set_potentiostat_EIS_config(differential=differential, two_wires=two_wires, coupling = 'DC',voltage_gain=gain_voltage,current_gain=gain_current)
    output_fname = out_dir + "galvanostat_EIT"
    if (differential):
        amp = amp_pot/BS.Gain_Voltage_DIFF
        offset = offset/BS.Gain_Voltage_DIFF
    else :
        amp = amp_pot/BS.Gain_Voltage_SE
        offset = offset/BS.Gain_Voltage_SE
else:
    output_fname = out_dir + "galvanostat_EIT"
    BS.set_galvanostat_EIS_config(differential=differential, High_gain=High_gain,two_wires=two_wires, coupling = 'DC' ,voltage_gain=gain_voltage,current_gain=gain_current)
    if High_gain:
        amp = amp_gal / BS.Gain_High_current
        offset = offset / BS.Gain_High_current
    else:
        amp = amp_gal / BS.Gain_Low_current
        offset = offset / BS.Gain_Low_current

##### Measurement
# Output dict
meas = {}
meas['date'] = date
for freq in freqs:
    meas[freq] = []
meas['protocol'] = {}
meas['protocol']['inj'] = []
meas['protocol']['rec'] = []
meas['status'] = "processing"
meas['comment'] = input('eventually add a comment:\n')
try:
    for i_inj in range(Nelec):
        inj_pat = (i_inj, (i_inj + 1)%Nelec)
        print('-------------------------')
        print('----- NEW INJECTION -----')
        print('-------------------------')
        print('patern: (stim-, stim+) =', inj_pat)
        print("switch inj electrodes")
        input('- Press a Key when ready')
        for i_rec in range(Nelec - 3):
            rec_pat = (((i_inj + i_rec + 2)%Nelec, (i_inj + i_rec + 3)%Nelec))
            print('----- NEW RECORDING -----')
            print('patern: (V-, V+) =', rec_pat)
            print("switch inj electrodes")
            input('- Press a Key when ready')
            if rec_pat[1] == i_inj:
                rec_pat[1] = (rec_pat[1]+2) %Nelec
            meas['protocol']['inj'] += [inj_pat]
            meas['protocol']['rec'] += [rec_pat]

            for freq in freqs:
                print("f =", freq)
                output_freq_fname = output_fname + str(freq) +".csv"
                gain, phase, gain_ch1 = BS.interface.single_frequency_gain_phase(freq,dB = False, settling_time=settling_time,
                amp=amp, offset=offset, Nperiods=NPeriods, Vrange_CH1=1.0, Vrange_CH2=1.0, 
                offset_CH1 = 0.0,offset_CH2 = 0.0, verbose = False)
                data = gain*BS.Gain_TIA
                meas[freq] += [data]
                print("R =", data)
    meas['status'] = "completed"
    meas['comment'] += input('eventually add a comment:\n')
except KeyboardInterrupt:
    meas['status'] = "Interrupted"
except Exception as error:
    print("An error occurred:", error)
    meas['error'] = error

meas['duration'] = time.time() - t0
print('duration:', meas['duration'])

with open(output_fname + ".json", "w") as outfile:
    json.dump(meas, outfile)
print('measurments saved')

