import tobi
import bimms as bm
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

def bandpass(data: np.ndarray, edges: list[float], sample_rate: float, poles: int = 5):
    sos = scipy.signal.butter(poles, edges, 'bandpass', fs=sample_rate, output='sos')
    filtered_data = scipy.signal.sosfiltfilt(sos, data)
    return filtered_data

## Requiered: Two known resistors R1, R2
# E1 -- E2 --- R1 -- E3 -- E4
# E5 -- E6 --- R2 -- E7 -- E8
# E9 -- E10 --- R3 -- E11 -- E12
# E13 -- E14 --- R4 -- E15 -- E16

tb1 = bm.BIMMS()
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
tb1.test_config.CH1_gain(2)
tb1.test_config.CH2_gain(1)

amp_AWG = 1
#AWG_offset=.07

tb1.test_config.AWG_amp(amp_AWG)
#tb1.test_config.AWG_offset(AWG_offset)

"""
p1 = tobi.protocole()
p1.add_patern(inj=(2, 4), rec=(3, 5))
#p1.add_patern(inj=(2, 4), rec=(3, 5))
#p1.add_patern(inj=(1, 3), rec=(2, 4))
#p1.add_patern(inj=(1, 3), rec=(2, 4))


p1.add_patern(inj=(3, 1), rec=(4, 2))
p1.add_patern(inj=(10,4), rec=(9,5))
#p1.add_patern(inj=(1, 7), rec=(2, 6))
p1.add_patern(inj=(1, 7), rec=(2, 6))
tb1.protocole = p1
"""
#m1 = bm.FrequentialSingleFrequency(freq=1000,nperiods=8 ,settling_time=0.001)
f = 1000
m1 = bm.TemporalSingleFrequency(freq=f,nperiods=10+4,)


for i in range(10):
    tb1.attach_measure(m1)
    #results = tb1.eit_measure()
    results = tb1.measure()


    t = results['t']
    ch1  = results['chan1_raw']



    # Load sample data from a WAV file
    sample_rate = 1/(t[1] - t[0])

    # Apply a 10-50 Hz high-pass filter to the original data
    ch1_filter = bandpass(ch1, [f/5, 10*f], sample_rate, 2)

    plt.figure(1)
    plt.plot(t,ch1-np.mean(ch1))
    #plt.plot(t,ch1_filter)
plt.show()
exit()