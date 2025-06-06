# AKAI APC Key 25 LED Feedback fix
Solution to fix bug in AKAI APC light feedback

## AKAI APC Key 25 problem/bug:
In Ableton Live I midi mapped some of the grid buttons of the APC Key 25 to toggle controls, it works fine but the led colors do not change so you can't know whether the midi mapped controls are ON or OFF.
Doing some research on the internet I found out that Ableton sends the midi information through the "Remote" midi ports but the AKAI does not react to it.
Each button of the APC Key grid corresponds to a note, the midi message to change the led color is:
</br>```NOTE_ON + <note_of_the_button> + VELOCITY_VALUE```
The velocity value defines which color the led should be:
* 0=off,
* 1=green,
* 2=green blink,
* 3=red,
* 4=red blink,
* 5=yellow,
* 6=yellow blink,
* 7-127=green

Ableton Live sends the following message when the midi mapped control is OFF:</br>```NOTE_OFF + <note_of_the_button> + 64```
This python script detects when this type of messages are sent by Ableton Live to the Midi Remote Output Ports using a virtual midi port, then I translate those to midi messages that makes the APC Key 25 change the led color correctly:<br/>```NOTE_ON + <note_of_the_button> + 3 (RED COLOR)```

## Installation for Mac
* Download repo
* Create python env with the requirements.txt
* Activate IAC driver on Midi Studio in Mac
* Update the .plist with the env and script paths
* Copy the .plist to ~/Library/LaunchAgents
* Configure the Ableton midi following the screenshot
* Reboot(?) and enjoy

## Ableton Live configuration (Mac)
You have to use a virtual midi port (in my case I use the Mac OSX default "IAC Driver (Bus 1)") and enable "Remote" in its Output port in Ableton Live's settings:
![plot](./screenshot_ableton.png)
![plot](./screenshot_midi_mac.png)

## Mac OSX .plist (in order to run it in background and forget about it)
I've added a .plist config that should be placed in ```~/Library/LaunchAgents/``` folder in order run the script when the computer starts and keep it running in background.</br>
It must be updated with the virtual environment python binary path (can be created using ```virtualenv midi_apc_env; pip install -r requirements.txt```) and the path of the ```apc_led_feedback.py``` script.

## Installation for Windows
The files for Windows will be inside a Windows folder.

* Download repo
* Create python virtualenv
* Install requirements with `pip install -r requirements.txt`
* For installing the python package python-rtmidi a C++ compiler is needed, you can install:
  * [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  * When installing Visual Studio Build Tools, you only need these core components:
    * MSVC C++ build tools (the compiler itself)
    * Windows SDK
    * C++ CMake tools for Windows (helpful but not strictly required)
* Install loopMIDI and create a loopMIDI Port
* Configure Ableton Midi like shown in the screenshots

## Running on Windows
1. Start your computer
2. loopMIDI will autostart
3. Connect APC Key 25
4. Run the script
5. Open Ableton

## Windows configuration screenshots
![plot](./Windows/ableton_windows.png)
![plot](./Windows/loopmidi_windows.png)
![plot](./Windows/script_windows.png)

## Libraries used
MIDO: ```https://github.com/mido/mido```

## Some links from sources that helped me understand and fix this problem
https://www.youtube.com/watch?v=RYMRiGQtTz0
</br>https://forum.ableton.com/viewtopic.php?t=149974

## NOTE: I do not have time to provide any support on this
