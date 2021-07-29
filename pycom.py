from abc import ABCMeta
from typing import Tuple, Any
from enum import Enum, IntFlag
from datetime import datetime
from collections import namedtuple
from collections.abc import Callable
import serial

class OperatingMode(Enum):
    AM   = 0
    AM_N = 1

class SquelchStatus(Enum):
    CLOSED = 0
    OPEN   = 1

class PyCom:
    def __init__(self, debug: bool = False):
        self._ser = serial.Serial('/dev/ttyUSB0')
        self._debug = debug
        if self._debug:
            print(self._ser.name)
            print(self._ser.baudrate)

    def _send_command(self, command, data=b'', preamble=b'') -> Tuple[int, int, bytes]:

        self._ser.write(preamble + b'\xfe\xfe\x92\xe0' + command + data + b'\xfd')

        # Our cable reads what we send, so we have to remove this from the buffer first
        self._ser.read_until(expected=b'\xfd')

        # Now we are reading replies
        reply = self._ser.read_until(expected=b'\xfd')

        return reply

    def power_on(self):
        wakeup_preamble_count = 8
        if self._ser.baudrate == 19200:
            wakeup_preamble_count = 27
        elif self._ser.baudrate == 9600:
            wakeup_preamble_count = 14

        self._send_command(b'\x18\x01', preamble=b'\xfe' * wakeup_preamble_count)

    def power_off(self):
        self._send_command(b'\x18\x00')

    def read_transceiver_id(self):
        reply = self._send_command(b'\x19\x00')
        return reply

    def read_operating_frequency(self):
        reply = self._send_command(b'\x03')
        return reply
    
    def read_operating_mode(self):
        reply = self._send_command(b'\x04')
        return reply

    def send_operating_frequency(self, frequency: float):
        reply = self._send_command(b'\x03')
        return reply
    
    def read_operating_mode(self):
        reply = self._send_command(b'\x04')
        return reply

    def read_squelch_status(self):
        reply = self._send_command(b'\x15\x01')
        return reply

    def read_squelch_status2(self):
        reply = self._send_command(b'\x15\x05')
        return reply