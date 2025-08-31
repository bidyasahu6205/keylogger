#KEY LOGGER

Files and their description:

- main.py → Entry point of the program. Starts the keylogger, sets up logging, and registers the on_press function.
- handleKey.py → Handles all keystroke events, manages special key handling, logging, and triggers email sending & cleanup.
- mail.py → Responsible for sending the captured keystrokes via email with attachments using SMTP.
- settingUp.py → Handles startup persistence by adding the script to Windows Registry. Also defines global variables for buffer, log file path, and timestamps.
- cleanup.py → Removes traces of the keylogger by deleting log files and removing the registry startup entry.
- .env → Stores sensitive information such as email address and password securely (used for sending logs).

Features:
- Captures all keystrokes including special keys (Shift, Ctrl, Alt, Enter, etc.).
- Logs keystrokes to a hidden file (C:\Users\Public\Keylogs.txt).
- Sends logs via email automatically at set intervals.
- Runs silently in the background.
- Persistence: Automatically adds itself to Windows Startup for continuous execution.
- Cleanup functionality: Deletes logs and removes itself from startup on command.

Requirements:
- Python 3.10+
- Required libraries:
- pynput
- smtplib (standard library)
- logging (standard library)
- dotenv
- Operating System: Windows (due to registry-based persistence).

⚠️ Disclaimer: This project is strictly for educational purposes only (e.g., studying malware analysis, learning persistence techniques, or testing defensive tools). Misuse for unauthorized surveillance or malicious intent is illegal.
