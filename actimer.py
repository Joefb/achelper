import os
import time
import threading

### Enter the log path to the EQ log file ###
log_path = "/home/home_name/.wine/drive_c/Program Files (x86)/EverQuest/Logs/"
### No need to modify below this line #########################################
###############################################################################



### Get the active toon by checking the current modified file ###
def get_active_toon():
    toon_logs = []
    os.chdir(log_path)
    files_list = os.listdir()
    for file in files_list:
        if file[:6] == 'eqlog_':
            toon_logs.append([file, os.stat(file).st_mtime])
    toon_logs = sorted(toon_logs,key=lambda l:l[1], reverse=True)
    toon = toon_logs[0][0]
    return toon

### Read the log file ###
def read_log(log_loc, last_pos):
    with open(log_loc, "r") as f:
        f.seek(last_pos)
        new_lines = f.readlines()
        last_pos = f.tell()
    return new_lines, last_pos

### init vars ###
def init_vars():
    toon = get_active_toon()
    last_toon = toon
    log_loc = log_path + toon
    file_size = os.path.getsize(log_loc)
    last_pos = file_size
    return toon, last_toon, log_loc, file_size, last_pos

### Calculate Time ###
def calc_time(t):
    hour, ampm = t[-5:].split()
    hour = int(hour)

    if ampm == "PM" and hour != 12:
        hour += 12
    
    
    hour_until = 21 - hour
    if hour_until < 0:
        hour_until += 24

    return hour_until * 3 * 60

def ac_timer(t):
    while t > 0:
        if cancel_event.is_set():
            return

        os.system("clear")
        mins, secs = divmod(t, 60)
        print(f'''
        AC Timer 
        ==============================================================
         AC Pop in: {mins:02d}:{secs:02d}
         Active Toon: {toon[6:-16]} 
        ==============================================================
                ''')
        time.sleep(1)
        if mins == 10 and secs == 0:
            os.system("espeak -v or -s 185 \"Ten minutes to AC pop!\"")
            t -= 1

        if mins == 5 and secs == 0:
            os.system("espeak -v or -s 185 \"Five minutes to AC pop!\"")
            t -= 1

        t -= 1

    os.system("espeak -v or -s 185 \"AC pop!\"")
    ac_timer(24 * 3 * 60)

def start_timer(t):
    global timer_thread, cancel_event

    if timer_thread is not None and timer_thread.is_alive():
        cancel_event.set()
        timer_thread.join()

    cancel_event = threading.Event()
    timer_thread = threading.Thread(target=ac_timer, args=(t,))
    timer_thread.start()

def intro_scrn():
    os.system("clear")
    print(f'''
    AC Timer 
    ==============================================================
     Use the /time in game to start AC Timer. 
     The timer will restart with the correcct time anytime you /time.
     Due to how one game hour is three real minutes, /time right
     at the start on a new game hour so its not off a few minutes.  

     Active Toon: {toon[6:-16]} 
    ==============================================================
            ''')
    return

### init vars ###
toon, last_toon, log_loc, file_size, last_pos = init_vars()
timer_thread = None
cancel_event = threading.Event()

### Load intro screen
intro_scrn()

#### Main loop ###
while True:
    ### If active toon changes, re init vars ###
    toon = get_active_toon()
    if toon != last_toon:
        last_toon = toon
        time.sleep(5)
        toon, last_toon, log_loc, file_size, last_pos = init_vars()

    time.sleep(0.5)
    log_loc = log_path + toon
    file_size = os.path.getsize(log_loc)
    
    if file_size != last_pos:
        new_lines, last_pos = read_log(log_loc, last_pos)
        for line in new_lines:
            line = line.strip()
            if "Game Time:" in line:
                start_timer(calc_time(line))
        last_pos = file_size
