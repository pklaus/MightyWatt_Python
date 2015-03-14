#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import struct
import time
from pprint import pprint
import threading

class MightyWatt(object):

    LE = "\r\n"            # line ending
    IDN_q = b"\x1F"        # identify query byte
    IDN_r = "Mighty Watt"  # expected identify answer
    QDC_q = b"\x1E"        # query command byte
    QDC_r = [              # meaning of the answer lines
        ('FW_VERSION', str),
        ('BOARD_REVISION', str),
        ('maxIdac', lambda x: int(x)/1000.),
        ('maxIadc', lambda x: int(x)/1000.),
        ('maxVdac', lambda x: int(x)/1000.),
        ('maxVadc', lambda x: int(x)/1000.),
        ('MAX_POWER', lambda p: int(p)/1000.),
        ('DVM_INPUT_RESISTANCE', int),
        ('temperatureThreshold', int),
        ('MAX_TEMPERATURE', int),
        ('MIN_TEMPERATURE', int),
    ]
    STATUS = {
        0: 'READY',
        1: 'CURRENT_OVERLOAD',
        2: 'VOLTAGE_OVERLOAD',
        4: 'POWER_OVERLOAD',
        8: 'OVERHEAT'
    }
    UPD_fmt = '>HHBBBB'
    UPD_r = [              # update response
        ('current', lambda i: i/1000.),
        ('voltage', lambda v: v/1000.),
        ('temperature', int),
        ('temperatureThreshold', int),
        ('remoteStatus', lambda rs: bool(rs & 0x01)),
        ('currentStatus', lambda x: x)
    ]
    MODE_CC =   0 | 0x80 | (2 << 5)
    MODE_CV =   1 | 0x80 | (2 << 5)
    MODE_CP =   2 | 0x80 | (3 << 5)
    MODE_CR =   3 | 0x80 | (3 << 5)
    TEMPERATURE_THRESHOLD_ID = 4 | 0x80 | (1 << 5)
    REMOTE_ID = 5 | 0x80 | (1 << 5)

    update_rate = 5
    props = None
    message_size = 0
    identity = None
    idn_tries = 20
    qdc_tries = 20

    def __init__(self, port, verbose=False):
        self.port = port
        self.verbose = verbose
        self.message_size = struct.calcsize(MightyWatt.UPD_fmt)
        self._connect()
        if self.verbose: self.print_device_summary()
        self.timer = PerpetualTimer(1/self.update_rate, self.update)
        self.timer.start()

    def _connect(self):
        try:
            self._c = serial.Serial(self.port, 115200, timeout=0.1)
        except (serial.serialutil.SerialException, FileNotFoundError):
            raise MightyWattCommunicationException()
        #time.sleep(0.001)
        self._identify()
        self._read_properties()
        self.update()

    def _identify(self):
        while not self.identity and self.idn_tries > 0:
            answer = ''
            try:
                self._write(MightyWatt.IDN_q)
                time.sleep(0.02)
                answer = self._readline()
                assert answer == MightyWatt.IDN_r + MightyWatt.LE, "strange answer: " + answer
                self.identity = answer.strip()
                return
            except AssertionError:
                if self.verbose: print('Not a valid IDN response: ' + str(answer))
                self.idn_tries -= 1
                time.sleep(0.1)
        raise MightyWattCommunicationException("Didn't get a proper IDN response.")

    def _write(self, *args, **kwargs):
        try:
            return self._c.write(*args, **kwargs)
        except (OSError, serial.serialutil.SerialException):
            raise MightyWattCommunicationException()

    def _read(self, *args, **kwargs):
        try:
            return self._c.read(*args, **kwargs)
        except (OSError, serial.serialutil.SerialException):
            raise MightyWattCommunicationException()

    def _readline(self):
        try:
            return self._c.readline().decode('ascii')
        except (OSError, serial.serialutil.SerialException):
            raise MightyWattCommunicationException()

    def _read_properties(self):
        while not self.props and self.qdc_tries > 0:
            response = []
            try:
                self._write(MightyWatt.QDC_q)
                time.sleep(0.02)
                #response = self._read(200).decode('ascii')
                #response = response.strip()
                #response = response.split(MightyWatt.LE)
                response = [self._readline() for i in range(len(MightyWatt.QDC_r))]
                assert len(response) == len(MightyWatt.QDC_r)
                props = {}
                for i in range(len(MightyWatt.QDC_r)):
                    value = MightyWatt.QDC_r[i][1](response[i])
                    props[MightyWatt.QDC_r[i][0]] = value
                self.props = props
                return
            except (AssertionError, ValueError):
                if self.verbose: print("Not a valid QDC response: " + str(response))
                self.qdc_tries -= 1
                time.sleep(0.1)
        raise MightyWattCommunicationException("Didn't get a proper QDC response.")

    def print_device_summary(self):
        print("Connected to a MightyWatt on port {}".format(self.port))
        print("Properties:")
        pprint(self.props)

    def update(self):
        self._write(b"\x8F")
        self._update_status()

    def set_update_rate(self, rate):
        assert rate < 30 and rate > 1.2
        self.timer.wait_time = 1/self.update_rate

    def _update_status(self):
        time.sleep(0.02)
        try:
            response = self._read(self.message_size)
        except (OSError, serial.serialutil.SerialException):
            raise MightyWattCommunicationException()
        if len(response) != self.message_size:
            raise MightyWattCommunicationException()
        self._set_status(response)

    def set_cc(self, current):
        current = int(round(current*1000.))
        self._write(struct.pack('>BH', MightyWatt.MODE_CC, current))
        self._update_status()

    def set_cv(self, voltage):
        voltage = int(round(voltage*1000.))
        self._write(struct.pack('>BH', MightyWatt.MODE_CV, voltage))
        self._update_status()

    def set_cp(self, power):
        power = int(round(power*1000.))
        power = three_bytes(power)
        self._write(struct.pack('>BBBB', MightyWatt.MODE_CP, *power))
        self._update_status()

    def set_cr(self, resistance):
        resistance = int(round(resistance*1000.))
        resistance = three_bytes(resistance)
        self._write(struct.pack('>BBBB', MightyWatt.MODE_CR, *resistance))
        self._update_status()

    def set_remote(self, remote=True):
        self._write(struct.pack('>BB', MightyWatt.REMOTE_ID, int(remote)))
        self._update_status()

    def set_local(self, local=True):
        self.set_remote(not local)

    def _set_status(self, response):
        response = struct.unpack(MightyWatt.UPD_fmt, response)
        status = dict()
        for i in range(len(MightyWatt.UPD_r)):
            value = MightyWatt.UPD_r[i][1](response[i])
            status[MightyWatt.UPD_r[i][0]] = value
        self.status = status

    def print_status(self):
        pprint(self.status)

    def stop(self):
        self.set_cc(0.0)
        self.set_local()

    def close(self):
        try:
            self.stop()
        except:
            pass
        try:
            self.timer.stop()
        except:
            pass

    def __del__(self):
        self.close()

class MightyWattException(Exception):
    pass

class MightyWattCommunicationException(MightyWattException):
    pass

class PerpetualTimer(threading.Thread):
    def __init__(self, wait_time, func, *args):
        self.wait_time = wait_time
        self.func = func
        self.args = args
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            self.func(*self.args)
            self.event.wait(self.wait_time)

    def stop(self):
        self.event.set()

def three_bytes(value):
    return (value >> 16 & 0xFF, value >> 8 & 0xFF, value & 0xFF)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Mighty Watt tool')
    parser.add_argument('serial_port', help='The serial port to connect to')
    parser.add_argument('--verbose', '-v', action='store_true', help='Generate verbose output')
    args = parser.parse_args()
    try:
        try:
            mw = MightyWatt(args.serial_port, verbose=args.verbose)
        except MightyWattCommunicationException:
            parser.error('An error occured, could not establish a connection to the device.')
        mw.update()
        mw.print_status()
        mw.set_cc(1.00)
        mw.print_status()
        time.sleep(0.5)
        mw.set_cc(1.00)
        mw.print_status()
        time.sleep(0.5)
        mw.update()
        mw.print_status()
        #mw.set_remote()
        mw.print_status()
        time.sleep(0.5)
        mw.update()
        mw.print_status()
        mw.set_cp(2.5)
        mw.print_status()
        time.sleep(0.7)
        mw.update()
        mw.print_status()
        time.sleep(2.5)
        mw.update()
        mw.print_status()
        mw.set_cv(5.1)
        mw.print_status()
        time.sleep(0.7)
        mw.set_cv(5.1)
        time.sleep(0.7)
        mw.update()
        mw.print_status()
        time.sleep(2.5)
        mw.update()
        mw.print_status()
        mw.close()
    except KeyboardInterrupt:
        try:
            mw.close()
        except:
            pass

if __name__ == "__main__":
    main()
