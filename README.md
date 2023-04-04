# Ancient Cyclops Timer

Getting tired of trying to keep track of the in game time for the AC pop?
Trying to figure out how much time you have before the next pop? O dam you missed it again!
Me too!! Thats why I made this handy little program!

AC Timer will read the in game time and start a timer for next AC pop in South Ro.

### Features
* Automatically detects the active toon 
* Automatically change the log file to active toon
* Automatically restarts the timer at 9pm game time
* Detects when /time is used in game and sets timer
* Voice notification at the five, ten minute mark and at pop time

### Requirements
* `Python3`
* `espeak`

### Set Up
1. Install `python3` - Skip this if its already installed
2. Install `espeak` - Use your package manager
3. Open `actimer.py` in your favorite editor.
4. Edit the `log_path` variable to the directory of your EQ log folder

### Usage
`python3 actimer.py` to start the program
`/time` while in game to start the timer

#### Note:
One hour of in game time is three minutes real time. Due to this its best if you /time right at the
start an in game hour. If you dont the timer could be a up to three minutes off.

#### About espeak
You can change the voice that espeak uses. Just do a `espeak --help` or `man espeak` for more info. 


