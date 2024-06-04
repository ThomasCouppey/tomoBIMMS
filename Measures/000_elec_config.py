import tobi
import bimms as bm
import matplotlib.pyplot as plt
import numpy as np

import pyeit.eit.bp as bp
import pyeit.eit.jac as jac
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh
## Requiered: Two known resistors R1, R2
# E1 -- E2 --- R1 -- E3 -- E4
# E5 -- E6 --- R2 -- E7 -- E8
# E9 -- E10 --- R3 -- E11 -- E12
# E13 -- E14 --- R4 -- E15 -- E16
tb1 = tobi.TomoBimms()
tb1.keep_on()

tb1.config_mode("MANUAL")
tb1.manual_config.waveform_gen("INTERNAL")
tb1.manual_config.excitation_source("VOLTAGE")
tb1.manual_config.I_source_gain("HIGH")
tb1.manual_config.wire_mode("4_WIRE")
tb1.manual_config.excitation_signaling_mode("DIFF")
tb1.manual_config.excitation_coupling("DC")
tb1.manual_config.DC_feedback(False)
tb1.manual_config.Enable_Isource(True)

tb1.manual_config.CHx_to_Scopex("BOTH")
tb1.manual_config.CH1_coupling("DC")
tb1.manual_config.CH2_coupling("DC")
tb1.manual_config.TIA_coupling("DC")
tb1.manual_config.connect_TIA(True)
tb1.manual_config.TIA_to_CH2(True)
tb1.manual_config.TIA_NEG("Ineg")
tb1.manual_config.CH1_gain(50)
tb1.manual_config.CH2_gain(1)

amp_AWG = .1
#AWG_offset=.07

tb1.manual_config.AWG_amp(amp_AWG)
tb1.save_config(save=True, fname="sources/cuff_config.json", manual=True)
del tb1