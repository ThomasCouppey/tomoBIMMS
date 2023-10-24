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


cmd_shift = 2**25
## Comannd values
set_switch = 0x0A

## SPI with MUX
MUX_STM32_CLK = cst.STM32_CLK
MUX_STM32_CLK_p = cst.STM32_CLK_p
MUX_STM32_MOSI_p = cst.STM32_MOSI_p
MUX_STM32_MISO_p = cst.STM32_MISO_p
MUX_STM32_CS_p = 7

