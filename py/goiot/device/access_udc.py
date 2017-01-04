#!/usr/bin/env python

"""
@summary: Access UDC-3200 via modbus-RTU on serial
@author: Yun Hua, yun_hua@yashentech.com
@date: 2017.01.04
"""

import minimalmodbus

# Reference: http://stackoverflow.com/questions/17081442/python-modbus-library
if __name__ == '__main__':
    instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1)
    temperature = instrument.read_float(0x40)
    print(temperature)

