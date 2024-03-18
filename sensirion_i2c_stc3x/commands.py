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
"""
The transfer classes specify the data that is transferred between host and sensor. The generated transfer classes
are used by the driver class and not intended for direct use.
"""

from sensirion_driver_adapters.rx_tx_data import TxData, RxData
from sensirion_driver_adapters.transfer import Transfer
from sensirion_driver_support_types.bitfield import BitField, BitfieldContainer


class TestResultT(BitfieldContainer):
    memory_error = BitField(offset=0, width=2)
    vdd_out_of_range = BitField(offset=2, width=1)
    measurement_value_error = BitField(offset=3, width=6)
    temperature_error = BitField(offset=9, width=1)


class SetBinaryGas(Transfer):
    """
    The STC3x measures the concentration of binary gas mixtures. It is important to note that the STC3x
    is not selective for gases, and it assumes that the binary gas is set correctly. The sensor can only
    give a correct concentration value when only the gases set with this command are present.
    When the system is reset, or wakes up from sleep mode, the sensor goes back to default mode, in
    which no binary gas is selected. This means that the binary gas must be reconfigured.
    When no binary gas is selected (default mode) the concentration measurement will return undefined
    results. This allows to detect unexpected sensor interruption (e.g. due to temporary power loss) and
    consequently reset the binary gas to the appropriate mixture.
    """

    CMD_ID = 0x3615

    def __init__(self, binary_gas):
        self._binary_gas = binary_gas

    def pack(self):
        return self.tx_data.pack([self._binary_gas])

    tx = TxData(CMD_ID, '>HH', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class SetRelativeHumidityRaw(Transfer):
    """
    As mentioned in section 5.1 of the datasheet, the measurement principle of the concentration
    measurement is dependent on the humidity of the gas. With the set relative humidity command, the
    sensor uses internal algorithms to compensate the concentration results.
    When no value is written to the sensor after a soft reset, wake-up or power-up, a relative humidity
    of 0% is assumed.
    The value written to the sensor is used until a new value is written to the sensor
    """

    CMD_ID = 0x3624

    def __init__(self, relative_humidity_ticks):
        self._relative_humidity_ticks = relative_humidity_ticks

    def pack(self):
        return self.tx_data.pack([self._relative_humidity_ticks])

    tx = TxData(CMD_ID, '>HH', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class SetTemperatureRaw(Transfer):
    """
    The concentration measurement requires a compensation of temperature. Per default, the sensor uses
    the internal temperature sensor to compensate the concentration results. However, when using the
    SHTxx, it is recommended to also use its temperature value, because it is more accurate.
    When no value is written to the sensor after a soft reset, wake-up or power-up, the internal
    temperature signal is used.
    The value written to the sensor is used until a new value is written to the sensor.
    """

    CMD_ID = 0x361e

    def __init__(self, temperature_ticks):
        self._temperature_ticks = temperature_ticks

    def pack(self):
        return self.tx_data.pack([self._temperature_ticks])

    tx = TxData(CMD_ID, '>HH', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class SetPressure(Transfer):
    """
    A pressure value can be written into the sensor, for density compensation of the gas concentration
    measurement. It is recommended to set the pressure level, if it differs significantly from 1013mbar.
    Pressure compensation is valid from 600mbar to 1200mbar.
    When no value is written to the sensor after a soft reset, wake-up or power-up, a pressure of
    1013mbar is assumed.
    The value written is used until a new value is written to the sensor.
    """

    CMD_ID = 0x362f

    def __init__(self, absolue_pressure):
        self._absolue_pressure = absolue_pressure

    def pack(self):
        return self.tx_data.pack([self._absolue_pressure])

    tx = TxData(CMD_ID, '>HH', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class MeasureGasConcentrationRawFast(Transfer):
    """
    The measurement of gas concentration is done in one measurement in a single shot, and takes less
    than 66ms. When measurement data is available, it can be read out by sending an I2C read header and
    reading out the data from the sensor. If no measurement data is available yet, the sensor will
    respond with a NACK on the I2C read header.
    In case the ‘Set temperature command’ has been used prior to the measurement command, the
    temperature value given out by the STC3x will be that one of the ‘Set temperature command’. When the
    ‘Set temperature command’ has not been used, the internal temperature value can be read out.
    During product development it is recommended to compare the internal temperature value of the STC3x
    and the temperature value of the SHTxx, to check whether both sensors are properly thermally
    coupled. The values must be within 0.7°C.
    """

    CMD_ID = 0x3639

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.066, slave_address=None, ignore_ack=False)
    rx = RxData('>HH')


class MeasureGasConcentrationRawSlow(Transfer):
    """
    The measurement of gas concentration is done in one measurement in a single shot, and takes less
    than 66ms. When measurement data is available, it can be read out by sending an I2C read header and
    reading out the data from the sensor. If no measurement data is available yet, the sensor will
    respond with a NACK on the I2C read header.
    In case the ‘Set temperature command’ has been used prior to the measurement command, the
    temperature value given out by the STC3x will be that one of the ‘Set temperature command’. When the
    ‘Set temperature command’ has not been used, the internal temperature value can be read out.
    During product development it is recommended to compare the internal temperature value of the STC3x
    and the temperature value of the SHTxx, to check whether both sensors are properly thermally
    coupled. The values must be within 0.7°C.
    """

    CMD_ID = 0x3639

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.11, slave_address=None, ignore_ack=False)
    rx = RxData('>HH')


class ForcedRecalibration(Transfer):
    """
    Forced recalibration (FRC) is used to improve the sensor output with a known reference value. See
    the Field Calibration Guide for more details. If no argument is given, the sensor will assume a
    default value of 0 vol%. This command will trigger a concentration measurement as described in 3.3.6
    of the datasheet and therefore it will take the same measurement time.
    """

    CMD_ID = 0x3661

    def __init__(self, reference_concentration):
        self._reference_concentration = reference_concentration

    def pack(self):
        return self.tx_data.pack([self._reference_concentration])

    tx = TxData(CMD_ID, '>HH', device_busy_delay=0.066, slave_address=None, ignore_ack=False)


class EnableAutomaticSelfCalibration(Transfer):
    """
    Enable the automatic self-calibration (ASC).
    The sensor can run in automatic self-calibration mode. This mode will enhance the accuracy for
    applications where the target gas is not present for the majority of the time. See the Field
    Calibration Guide for more details. This feature can be enabled or disabled by using the commands as
    shown below.
    The automatic self-calibration is optimized for a gas concentration measurement interval of 1s.
    Substantially different measurement intervals may decrease the self-calibration performance.
    The default state is disabled.
    Automatic self-calibration in combination with sleep mode requires a specific sequence of steps. See
    section 3.3.9 in the datasheet for more detailed instructions
    """

    CMD_ID = 0x3fef

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class DisableAutomaticSelfCalibration(Transfer):
    """
    Disable the automatic self-calibration (ASC).
    The sensor can run in automatic self-calibration mode. This mode will enhance the accuracy for
    applications where the target gas is not present for the majority of the time. See the Field
    Calibration Guide for more details. This feature can be enabled or disabled by using the commands as
    shown below.
    The default state is disabled.
    """

    CMD_ID = 0x3f6e

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class PrepareReadState(Transfer):
    """The sensor will prepare its current state to be read out."""

    CMD_ID = 0x3752

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class ReadSensorState(Transfer):
    """
    Read out the sensor state. The 30 bytes must be stored on the microcontroller to be written
    back to the sensor after exiting sleep mode.
    """

    CMD_ID = 0xe133

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H')
    rx = RxData('>30B')


class WriteSensorState(Transfer):
    """
    Write the sensor state. The 30 bytes must be stored on the microcontroller to be written
    back to the sensor after exiting sleep mode.
    """

    CMD_ID = 0xe133

    def __init__(self, state):
        self._state = state

    def pack(self):
        return self.tx_data.pack([self._state])

    tx = TxData(CMD_ID, '>H30B')


class ApplyState(Transfer):
    """The sensor will apply the written state data."""

    CMD_ID = 0x3650

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class SelfTest(Transfer):
    """
    The sensor will run an on-chip self-test. A successful self-test will return zero.
    The 16-bit result of a sensor self-test is a combination of possible error states, encoded as bits
    (starting with lsb):

    - 0-1: Memory error
    - 2: VDD out of range
    - 3-8: Measurement value error
    - 9: Difference between externally supplied temperature (see 2.3.4) and internally measured
      temperatures exceeds the accuracy specifications.

    In case of a successful self-test the sensor returns 0x0000 with correct CRC.
    """

    CMD_ID = 0x365b

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.022, slave_address=None, ignore_ack=False)
    rx = RxData('>H')


class PrepareProductIdentifier(Transfer):
    """Prepare for reading the product identifier and sensor serial number."""

    CMD_ID = 0x367c

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H')


class ReadProductIdentifier(Transfer):
    """Read the product identifier and sensor serial number."""

    CMD_ID = 0xe102

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.01, slave_address=None, ignore_ack=False)
    rx = RxData('>III')


class EnterSleepMode(Transfer):
    """
    Put sensor into sleep mode.
    In sleep mode the sensor uses the minimum amount of current. The mode can only be entered from idle
    mode, i.e. when the sensor is not measuring. This mode is particularly useful for battery operated
    devices. To minimize the current in this mode, the complexity of the sleep mode circuit has been
    reduced as much as possible, which is mainly reflected by the way the sensor exits the sleep mode.
    The sleep command can be sent after the result have been read out and the sensor is in idle mode.
    """

    CMD_ID = 0x3677

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class ExitSleepMode(Transfer):
    """
    Exit the sleep mode.
    The sensor exits the sleep mode and enters the idle mode when it receives the valid I2C address and
    a write bit (‘0’). Note that the I2C address is not acknowledged. It is possible to poll the sensor
    to see whether the sensor has received the address and has woken up. This takes maximum 12ms.
    """

    CMD_ID = 0x0

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>B', device_busy_delay=0.012, slave_address=None, ignore_ack=False)


class EnableWeakFilter(Transfer):
    """
    The STC31 has two built-in noise filters that run an exponential smoothing over the past measurement points.
    By default, no filter is applied to the data. If weak smoothing is desired, the following command(s) must be executed
    once upon starting the sensor. When enabled, the weak filter is applied for all subsequent concentration
    measurements.
    """

    CMD_ID = 0x3fc8

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class DisableWeakFilter(Transfer):
    """disable the weak smoothing filter"""

    CMD_ID = 0x3f49

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class EnableStrongFilter(Transfer):
    """
    The STC31 has two built-in noise filters that run an exponential smoothing over the past measurement points.
    By default, no filter is applied to the data. If strong smoothing is desired, the following command(s) must be executed
    once upon starting the sensor. When enabled, the strong filter is applied for all subsequent concentration
    measurements.
    """

    CMD_ID = 0x3fd5

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.001, slave_address=None, ignore_ack=False)


class DisableStrongFilter(Transfer):
    """disable the strong smoothing filter"""

    CMD_ID = 0x3f54

    def pack(self):
        return self.tx_data.pack([])

    tx = TxData(CMD_ID, '>H', device_busy_delay=0.001, slave_address=None, ignore_ack=False)
