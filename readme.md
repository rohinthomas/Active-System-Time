# Active Time Logger

This script logs active system usage time by detecting system lock and unlock events. It records timestamps and calculates total active hours in a CSV file. The script supports **macOS, Windows, and Linux (Ubuntu)** with configurable shortcut keys stored in an `.env` file.

## Features
- Logs system lock/unlock events.
- Calculates total active hours per session and per day.
- Uses keyboard shortcuts to detect system activity.
- Supports **macOS, Windows, and Linux**.
- Configurable shortcut keys via `.env` file.

## Installation
### Prerequisites
Ensure you have **Python 3.6+** installed.

### Install Dependencies
#### Using `requirements.txt`
1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
### Set Shortcut Keys in `.env`
Create a `.env` file in the same directory and configure shortcuts based on your OS.

#### macOS:
```
LOCK_KEY_1=cmd
LOCK_KEY_2=ctrl
LOCK_KEY=q

UNLOCK_KEY_1=cmd
UNLOCK_KEY_2=ctrl
UNLOCK_KEY=w
```

#### Windows:
```
WIN_LOCK_KEY_1=win
WIN_LOCK_KEY_2=l

WIN_UNLOCK_KEY_1=win
WIN_UNLOCK_KEY_2=w
```

#### Linux (Ubuntu):
```
LINUX_LOCK_KEY_1=win
LINUX_LOCK_KEY_2=l

LINUX_UNLOCK_KEY_1=win
LINUX_UNLOCK_KEY_2=w
```

## Usage
Run the script:
```bash
python script.py
```

The script will listen for the configured shortcut keys and log activity in `time_log.csv`.

### CSV File Format:
| Date       | Timestamp           | Event                           | Session Time | Total Active Time Today |
|------------|---------------------|--------------------------------|--------------|-------------------------|
| 2025-03-17 | 11:05:17            | Shortcut Clicked: Command+Q    | 00:09:45     | 02:30:12                |
| 2025-03-17 | 12:10:30            | System Locked                  | -            | 02:30:12                |
| 2025-03-17 | 12:20:45            | Shortcut Clicked: Command+W    | 00:10:15     | 02:40:27                |

## Notes
- **Windows/Linux may require running as administrator (`sudo`) for key listening to work globally.**
- Ensure `time_log.csv` is writable in the script directory.
- The script updates the **total active time** without counting system lock periods.

## License
MIT License

