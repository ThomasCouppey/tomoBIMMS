"""
	Python library to use BIMMS measurement setup - STM32 constants
	Authors: Florian Kolbl / Louis Regnacq / Thomas Couppey
	(c) ETIS - University Cergy-Pontoise
		IMS - University of Bordeaux
		CNRS

	Requires:
		Python 3.6 or higher
"""

from bimms import cst


cmd_shift = 2**24
## Comannd values
set_switch = 0x0A

## SPI with MUX
MUX_STM32_CLK = cst.STM32_CLK
MUX_STM32_CLK_p = cst.STM32_CLK_p
MUX_STM32_MOSI_p = cst.STM32_MOSI_p
MUX_STM32_MISO_p = cst.STM32_MISO_p
MUX_STM32_CS_p = 7


sw_default = 0 #Default switch value on startup

STIMn_shift = 0
STIMp_shift = 4
CH2n_shift = 8
CH2p_shift = 12
CH1p_shift = 16
CH1n_shift = 20


STIMn_mask = 0xFFFFF0
STIMp_mask = 0xFFFF0F
CH2n_mask = 0xFFF0FF
CH2p_mask = 0xFF0FFF
CH1p_mask = 0xF0FFFF
CH1n_mask = 0x0FFFFF
