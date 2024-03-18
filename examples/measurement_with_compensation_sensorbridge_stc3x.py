#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2024 Sensirion AG, Switzerland
#
#     THIS FILE IS AUTOMATICALLY GENERATED!
#
# Generator:     sensirion-driver-generator 0.38.1
# Product:       stc3x
# Model-Version: 1.0.0
#

import argparse
import time

from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_driver import I2cConnection, CrcCalculator
from sensirion_i2c_sht4x import Sht4xDevice
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import (SensorBridgePort,
                                          SensorBridgeShdlcDevice,
                                          SensorBridgeI2cProxy)

from sensirion_i2c_stc3x.device import Stc3xDevice

parser = argparse.ArgumentParser()
parser.add_argument('--serial-port', '-p', default='COM1')
args = parser.parse_args()

with ShdlcSerialPort(port=args.serial_port, baudrate=460800) as port:
    bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
    bridge.switch_supply_on(SensorBridgePort.ONE)
    i2c_proxy = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
    i2c_connection = I2cConnection(i2c_proxy)
    stc3x_channel = I2cChannel(i2c_connection,
                               slave_address=0x29,
                               crc=CrcCalculator(8, 0x31, 0xff, 0x0))
    sht4x_channel = I2cChannel(i2c_connection,
                               slave_address=0x44,
                               crc=CrcCalculator(8, 0x31, 0xff, 0x0))
    stc3x_sensor = Stc3xDevice(stc3x_channel)
    sht4x_sensor = Sht4xDevice(sht4x_channel)
    time.sleep(0.014)

    # Output SHT4x serial number
    sht4x_serial_number = sht4x_sensor.serial_number()
    print(f"SHT4x Serial Number = {sht4x_serial_number}")

    # Output the product identifier and serial number
    (stc3x_product_id, stc3x_serial_number) = stc3x_sensor.get_product_id()
    print(f"STC3x Product id = {stc3x_product_id}")
    print(f"STC3x Serial Number = {stc3x_serial_number}")

    # Measure STC31-C CO2 in air in range 0% - 40%
    # or STC31 CO2 in air in range 0% - 25%
    stc3x_sensor.set_binary_gas(19)

    for i in range(100):
        # Slow down the sampling to 1Hz
        time.sleep(1.0)

        # Read humidity and temperature from external SHT4x sensor and use
        # it for compensation.
        sht4x_temperature, sht4x_humidity = sht4x_sensor.measure_high_precision()

        stc3x_sensor.set_relative_humidity(sht4x_humidity.value)
        stc3x_sensor.set_temperature(sht4x_temperature.value)
        (co2_concentration, stc3x_temperature) = stc3x_sensor.measure_gas_concentration()

        #     Print CO2 concentration in Vol% and temperature in degree celsius.
        print(f"CO2 concentration = {co2_concentration}")
        print(f"STC3x Temperature = {stc3x_temperature}")
