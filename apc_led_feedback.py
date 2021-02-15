#!/usr/bin/env python
from __future__ import print_function
import sys
import time
import mido
from mido import Message

portname = 'IAC Driver Bus 1' # The virtual midi input port
portname_send = 'APC Key 25'

while True:
    if portname_send not in mido.get_output_names() \
            or portname not in mido.get_input_names():
        # APC Key 25 not detected
        print('apc not detected')
        time.sleep(10)
        continue

    try:
        with mido.open_output(portname_send, autoreset=True) as port_send:
            try:
                with mido.open_input(portname) as port:
                    print('Using {}'.format(port))
                    print('Waiting for messages...')
                    for message in port:
                        print('Received {}'.format(message))
                        if message.type == 'note_off' and message.velocity == 64:
                            on = Message('note_on', note=message.note, velocity=3)
                            port_send.send(on)
                            sys.stdout.flush()
            except KeyboardInterrupt:
                pass
    except KeyboardInterrupt:
        pass
