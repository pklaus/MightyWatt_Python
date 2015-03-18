# -*- coding: utf-8 -*-

import serial
import struct
import time
from pprint import pprint
import threading
import queue

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

    identity = None
    props = None
    _status = None
    _update_rate = 10
    _message_size = 0
    _idn_tries = 20
    _qdc_tries = 20
    _min_update_interval = 0.005
    _message_queue = None

    def __init__(self, port, verbose=False):
        self.port = port
        self.verbose = verbose
        self._message_size = struct.calcsize(MightyWatt.UPD_fmt)
        self._message_queue = queue.Queue()
        self._start = clock()
        self._connect()
        self._update()
        if self.verbose: self.print_device_summary()
        self._timer = PerpetualTimer(1/self._update_rate, self._update)
        self._timer.start()

    def _connect(self):
        try:
            self._c = serial.Serial(self.port, 115200, timeout=0.1)
        except (serial.serialutil.SerialException, FileNotFoundError):
            raise MightyWattCommunicationException()
        self._identify()
        self._read_properties()

    def _identify(self):
        while not self.identity and self._idn_tries > 0:
            answer = ''
            try:
                self._write(MightyWatt.IDN_q)
                answer = self._readline()
                assert answer == MightyWatt.IDN_r + MightyWatt.LE, "strange answer: " + answer
                self.identity = answer.strip()
                return
            except AssertionError:
                if self.verbose: print('Not a valid IDN response: ' + str(answer))
                self._idn_tries -= 1
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
        except (TypeError, OSError, serial.serialutil.SerialException):
            raise MightyWattCommunicationException()

    def _readline(self):
        try:
            return self._c.readline().decode('ascii')
        except (OSError, serial.serialutil.SerialException):
            raise MightyWattCommunicationException()

    def _read_properties(self):
        while not self.props and self._qdc_tries > 0:
            response = []
            try:
                self._write(MightyWatt.QDC_q)
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
                self._qdc_tries -= 1
                time.sleep(0.1)
        raise MightyWattCommunicationException("Didn't get a proper QDC response.")

    def print_device_summary(self):
        print("Connected to a MightyWatt on port {}".format(self.port))
        print("Properties:")
        pprint(self.props)

    def _update(self):
        try:
            message = self._message_queue.get(block=False)
        except:
            message = b"\x8F"
        self._write(message)
        response = self._read(self._message_size)
        if len(response) != self._message_size:
            raise MightyWattCommunicationException()
        self._set_status(response)

    def set_update_rate(self, rate):
        assert (rate > 1.2) and (1/rate >= self._min_update_interval)
        self._update_rate = rate
        self._timer.wait_time = 1/self._update_rate

    def set_cc(self, current):
        current = int(round(current*1000.))
        self._message_queue.put(struct.pack('>BH', MightyWatt.MODE_CC, current))

    def set_cv(self, voltage):
        voltage = int(round(voltage*1000.))
        self._message_queue.put(struct.pack('>BH', MightyWatt.MODE_CV, voltage))

    def set_cp(self, power):
        power = int(round(power*1000.))
        power = three_bytes(power)
        self._message_queue.put(struct.pack('>BBBB', MightyWatt.MODE_CP, *power))

    def set_cr(self, resistance):
        resistance = int(round(resistance*1000.))
        resistance = three_bytes(resistance)
        self._message_queue.put(struct.pack('>BBBB', MightyWatt.MODE_CR, *resistance))

    def set_remote(self, remote=True):
        self._message_queue.put(struct.pack('>BB', MightyWatt.REMOTE_ID, int(remote)))

    def set_local(self, local=True):
        self.set_remote(not local)

    @property
    def status(self):
        assert self.ms_since_last_update < 1000.0
        return self._status.copy()

    def _set_status(self, response):
        response = struct.unpack(MightyWatt.UPD_fmt, response)
        status = dict()
        for i in range(len(MightyWatt.UPD_r)):
            value = MightyWatt.UPD_r[i][1](response[i])
            status[MightyWatt.UPD_r[i][0]] = value
        status['remote'] = status['remoteStatus']
        status['power'] = status['voltage'] * status['current']
        if status['current'] != 0.0:
            status['resistance'] = status['voltage'] / status['current']
        else:
            status['resistance'] = self.props['DVM_INPUT_RESISTANCE']
        status['time'] = clock() - self._start
        self._status = status

    def print_status(self):
        pprint(self.status)

    @property
    def ms_since_last_update(self):
        return ((clock() - self._start) - self._status['time']) * 1000.

    def stop(self):
        self.set_cc(0.0)

    def close(self):
        self._timer.stop()
        self._timer.join()
        self.set_cc(0.0)
        self._update()
        self.set_local()
        self._update()
        self._c.close()

    def __del__(self):
        try:
            self.close()
        except:
            pass

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

try:
    clock = time.perf_counter
except AttributeError:
    clock = time.time

def three_bytes(value):
    return (value >> 16 & 0xFF, value >> 8 & 0xFF, value & 0xFF)
