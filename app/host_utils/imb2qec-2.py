# Copyright 2022-2024 NXP
# SPDX-License-Identifier: BSD-3-Clause
####################################################################

import numpy as np
from array import array
from sys import argv

def help():
	print('\n\nSUPPORTED COMANDS: \n')
	print('QEC coefficient computation:')
	print('    imb2qec.py <tx|rx> <iq_gain_imb_dB> <iq_phase_imb_deg> <dc_re> <dc_im>')
	print('Help:')
	print('    imb2qec.py help')

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def imb2qec_tx(iq_gain_imb_dB, iq_phase_imb_deg):
	alpha   = 10**(iq_gain_imb_dB/20)
	phi_z   = iq_phase_imb_deg*np.pi/180

	f1 = 1/np.cos(phi_z)
	f2 = -np.tan(phi_z)/alpha
	f4 = 1/alpha

	print('\n**Tx QEC coeffs:**')
	print('f2 (2) = ' + hex(struct.unpack('<I', struct.pack('<f2', f2))[0]))
	print('f1 (3) = ' + hex(struct.unpack('<I', struct.pack('<f1', f1))[0]))
	print('f4 (4) = ' + hex(struct.unpack('<I', struct.pack('<f4', f4))[0]))

	return [f1, f2, f4]

import struct
import sys
import subprocess
def imb2qec_rx(iq_gain_imb_dB, iq_phase_imb_deg):
	gamma     = 10**(iq_gain_imb_dB/20)
	theta_z   = iq_phase_imb_deg*np.pi/180

	f1 = 1/gamma
	f2 = np.tan(theta_z)/gamma
	f4 = 1/np.cos(theta_z)

	print('\n**Rx QEC coeffs:**')
	print('f2 (2) = ' + float_to_hex(f2))
	print('f1 (3) = ' + float_to_hex(f1))
	print('f4 (4) = ' + float_to_hex(f4))
	#sys.argv = ['send', 0 , 0 , 0x08000002 , float_to_hex(f2) ]
	#exec('./vspa_mbox')
	subprocess.run(['vspa_mbox', 'send','0','0','0x08000002' , float_to_hex(f2) ])
	subprocess.run(['vspa_mbox', 'send','0','0','0x0800000b' , float_to_hex(f1) ])
	subprocess.run(['vspa_mbox', 'send','0','0','0x0800000c' , float_to_hex(f4) ])

	return [f1, f2, f4]

#Main#

if argv[1] == 'help':
	help()
elif argv[1] == 'tx':
	tx_qec_coeffs = imb2qec_tx(float(argv[2]), float(argv[3]))
#	qec2file(tx_qec_coeffs)
	print('\nTX QEC coefficients computed successfully!')
elif argv[1] == 'rx':
	print('\n**Rx gain coeffs:**')
	print('dc_g re (1) = ' + float_to_hex(float(argv[4])))
	print('dc_g im (2) = ' + float_to_hex(float(argv[5])))
	subprocess.run(['vspa_mbox', 'send','0','0','0x08000005' , float_to_hex(float(argv[4])) ])
	subprocess.run(['vspa_mbox', 'send','0','0','0x08000006' , float_to_hex(float(argv[5])) ])
	rx_qec_coeffs = imb2qec_rx(float(argv[2]), float(argv[3]))
#   	qec2file(rx_qec_coeffs)
	print('\nRX QEC coefficients computed successfully!')
else:
	raise Exception('\n\nWrong input! Type imb2qec.py help')