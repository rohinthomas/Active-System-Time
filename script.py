import os
import csv
from datetime import datetime, timedelta
from pynput import keyboard
from dotenv import load_dotenv
import platform

# Load environment variables from .env file
load_dotenv()

# File to store the log
log_file = "time_log.csv"

# Active time tracking
script_start_time = datetime.now()
last_active_time = script_start_time
daily_total = timedelta()
is_locked = False  # Flag to track system lock state

# Ensure CSV file has headers
if not os.path.exists(log_file):
    with open(log_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Timestamp", "Event", "Session Time (HH:MM:SS)", "Total Active Time Today (HH:MM:SS)"])

# Get OS type
system_os = platform.system()

# Function to load shortcuts based on OS
def get_shortcut_keys():
    if system_os == "Darwin":  # macOS
        return os.getenv("LOCK_KEY_1"), os.getenv("LOCK_KEY_2"), os.getenv("LOCK_KEY"), os.getenv("UNLOCK_KEY_1"), os.getenv("UNLOCK_KEY_2"), os.getenv("UNLOCK_KEY")
    elif system_os == "Windows":  # Windows
        return os.getenv("WIN_LOCK_KEY_1"), None, os.getenv("WIN_LOCK_KEY_2"), os.getenv("WIN_UNLOCK_KEY_1"), None, os.getenv("WIN_UNLOCK_KEY_2")
    elif system_os == "Linux":  # Ubuntu (Linux)
        return os.getenv("LINUX_LOCK_KEY_1"), None, os.getenv("LINUX_LOCK_KEY_2"), os.getenv("LINUX_UNLOCK_KEY_1"), None, os.getenv("LINUX_UNLOCK_KEY_2")
    else:
        return None, None, None, None, None, None  # Unsupported OS

LOCK_KEY_1, LOCK_KEY_2, LOCK_KEY, UNLOCK_KEY_1, UNLOCK_KEY_2, UNLOCK_KEY = get_shortcut_keys()

# Function to format timedelta as HH:MM:SS
def format_time(delta):
    total_seconds = int(delta.total_seconds())
    return f"{total_seconds // 3600:02}:{(total_seconds % 3600) // 60:02}:{total_seconds % 60:02}"

# Function to log events
# Function to log events
def log_event(event, session_time=None):
    global daily_total
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Read existing rows
    rows = []
    if os.path.exists(log_file):
        with open(log_file, mode="r", newline="") as file:
            reader = list(csv.reader(file))
            if reader:
                rows = reader

    # Format time correctly
    session_time_str = format_time(session_time) if session_time else ""
    daily_total_str = format_time(daily_total)

    # Always log system lock events
    rows.append([today_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), event, session_time_str, daily_total_str])

    # Write back to the CSV file
    with open(log_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


# Key combination trackers
current_keys = set()

# Convert string key names to `pynput.keyboard` Key objects
def get_key(key_name):
    try:
        return getattr(keyboard.Key, key_name)
    except AttributeError:
        return key_name.lower()  # Return lowercase string for regular keys

# Callback for key press
def on_press(key):
    global last_active_time, daily_total, is_locked
    try:
        if isinstance(key, keyboard.KeyCode):
            key = key.char

        current_keys.add(key)

        # Detect system unlock shortcut
        if get_key(UNLOCK_KEY_1) in current_keys and (UNLOCK_KEY_2 is None or get_key(UNLOCK_KEY_2) in current_keys) and UNLOCK_KEY in current_keys:
            if is_locked:
                is_locked = False
                last_active_time = datetime.now()
                log_event("System Unlocked (Tracking Active Time)")
                print(f"System Unlocked: Active Session Started at {last_active_time.strftime('%H:%M:%S')}")

        # Detect system lock shortcut
        if get_key(LOCK_KEY_1) in current_keys and (LOCK_KEY_2 is None or get_key(LOCK_KEY_2) in current_keys) and LOCK_KEY in current_keys:
            if not is_locked:
                end_time = datetime.now()
                session_duration = end_time - last_active_time
                daily_total += session_duration
                is_locked = True

                log_event("System Locked (Paused Active Time)", session_duration)
                print(f"System Locked: Active Time Counted - {format_time(session_duration)} | Total Today: {format_time(daily_total)}")

    except Exception as e:
        print(f"Error: {e}")

# Callback for key release
def on_release(key):
    try:
        if isinstance(key, keyboard.KeyCode):
            key = key.char
        current_keys.discard(key)
    except Exception as e:
        print(f"Error: {e}")

# Log the script start time
log_event("Script Started (Tracking Active Time)")

# Start listening
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Listening for shortcuts... Press Ctrl+C to exit.")
    listener.join()
