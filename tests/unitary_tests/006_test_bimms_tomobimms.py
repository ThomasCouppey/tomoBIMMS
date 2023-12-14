import tobi
import time
import bimms as bm
import matplotlib.pyplot as plt

freq = 100000
n_period=1
amp_AWG = 0.1

TB1 = tobi.TomoBimms()

TB1.config_mode("TEST")
TB1.test_config.waveform_gen("INTERNAL")
TB1.test_config.excitation_source("VOLTAGE")
TB1.test_config.excitation_signaling_mode("DIFF")
TB1.test_config.excitation_coupling("DC")
TB1.test_config.CHx_to_Scopex("CH1")
TB1.test_config.CH1_coupling("DC")
TB1.test_config.CH2_coupling("DC")
TB1.test_config.CH1_gain(1)
TB1.test_config.CH2_gain(1)
TB1.test_config.AWG_amp(amp_AWG)
TB1.test_config.wire_mode("2_WIRE")
m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)

TB1.set_CH1p_to_elec(10)
TB1.set_CH1n_to_elec(11)

TB1.set_STIMp_to_elec(9)
TB1.set_STIMn_to_elec(12)

TB1.attach_measure(m1)
results = TB1.measure()

time.sleep(1)

TB1.set_CH1p_to_elec(1)
TB1.set_CH1n_to_elec(2)

TB1.set_STIMp_to_elec(3)
TB1.set_STIMn_to_elec(4)

TB1.attach_measure(m1)
results = TB1.measure()

del TB1
