#!/usr/bin/env PATH=venv/bin python3
#-*- coding: utf-8 -*-
import re
import serial
import serial.tools.list_ports

re_ansi = re.compile(r'\x1b\[(\d+;)?\d+m')
re_fa = re.compile(r'^\d+ \[D\]\[SubghzFrequencyAnalyzerWorker\] ~:(\d+):[-0-9.]+$')

freqs = {}

#ports = serial.tools.list_ports.comports()
#for port in ports:
#    print(port.device)

s = serial.Serial('/dev/cu.usbmodemFD141', 38400, timeout=0.5)

while 1:
    l = s.readline()
    if len(l) == 0:
        continue

    l = l.decode('utf-8')
    l = l.rstrip('\r\n')
    l = re_ansi.sub('', l)

    if l == '>: ':
        s.write(b'log debug\r')

    if '[D][BtGap] set_non_discoverable success' in l:
        continue

    if 'Application thread stopped.' in l:
        s.write(b'\x03')
        l = s.readline()
        l = s.readline()
        break;

    print(l)

    m = re_fa.match(l)
    if m:
        freq = round(int(m.group(1))/1000)
        print('Found: ', freq)
        freqs[freq] = freqs.get(freq, 0) + 1

for freq in sorted(freqs):
    print(freq, freqs[freq])

s.close()
