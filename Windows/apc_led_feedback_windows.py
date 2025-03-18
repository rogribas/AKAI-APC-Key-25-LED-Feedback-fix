#!/usr/bin/env python
from __future__ import print_function
import sys
import time
import mido
from mido import Message

# Helper function to list available ports
def list_midi_ports():
    print("Available MIDI input ports:")
    for i, port in enumerate(mido.get_input_names()):
        print(f"  [{i}] {port}")
    
    print("\nAvailable MIDI output ports:")
    for i, port in enumerate(mido.get_output_names()):
        print(f"  [{i}] {port}")

# Print available MIDI ports
print("Scanning available MIDI ports...")
list_midi_ports()

# Auto-detect ports
try:
    # Try to find APC Key in available output ports
    apc_index = None
    for i, port in enumerate(mido.get_output_names()):
        if 'APC' in port:
            apc_index = i
            break
    
    if apc_index is not None:
        print(f"\nFound APC device: {mido.get_output_names()[apc_index]}")
        portname_send = mido.get_output_names()[apc_index]
    else:
        print("\nNo APC device found automatically. Please select output port by number:")
        portname_send = mido.get_output_names()[int(input("Enter output port number: "))]
    
    # Try to find loopMIDI in available input ports
    loopmidi_index = None
    for i, port in enumerate(mido.get_input_names()):
        if 'loopMIDI' in port:
            loopmidi_index = i
            break
    
    if loopmidi_index is not None:
        print(f"\nFound loopMIDI device: {mido.get_input_names()[loopmidi_index]}")
        portname = mido.get_input_names()[loopmidi_index]
    else:
        print("\nNo loopMIDI device found automatically. Please select input port by number:")
        portname = mido.get_input_names()[int(input("Enter input port number: "))]
    
    print(f"\nUsing input port: {portname}")
    print(f"Using output port: {portname_send}")

except (ValueError, IndexError):
    print("Invalid selection. Please run the script again.")
    sys.exit(1)

# Main program loop
while True:
    try:
        if portname_send not in mido.get_output_names() \
                or portname not in mido.get_input_names():
            print('Required MIDI ports not detected. Checking again in 5 seconds...')
            time.sleep(5)
            list_midi_ports()  # Show updated list of ports
            continue
        
        print(f"Opening output port: {portname_send}")
        with mido.open_output(portname_send, autoreset=True) as port_send:
            print("Output port opened successfully!")
            
            print(f"Opening input port: {portname}")
            with mido.open_input(portname) as port:
                print("Input port opened successfully!")
                print('Waiting for messages...')
                
                for message in port:
                    print(f'Received {message}')
                    if message.type == 'note_off' and message.velocity == 64:
                        # velocity = 3 -> RED Color
                        on = Message('note_on', note=message.note, velocity=3)
                        try:
                            port_send.send(on)
                            print(f'Sent: {on}')
                        except Exception as e:
                            print(f"Error sending message: {e}")
                        sys.stdout.flush()
                    if message.type == 'note_on' and message.velocity == 127:
                        # velocity = 1 -> RED Color
                        on = Message('note_on', note=message.note, velocity=1)
                        try:
                            port_send.send(on)
                            print(f'Sent: {on}')
                        except Exception as e:
                            print(f"Error sending message: {e}")
                        sys.stdout.flush()

    
    except OSError as e:
        print(f"Error opening MIDI port: {e}")
        print("This could be because:")
        print("1. Another application is using the port")
        print("2. The port name doesn't match exactly")
        print("3. The device isn't properly connected")
        print("\nTrying again in 5 seconds...")
        time.sleep(5)
    
    except KeyboardInterrupt:
        print("\nExiting program")
        break
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
