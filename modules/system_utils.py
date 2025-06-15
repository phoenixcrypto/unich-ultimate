import os
import platform
import sys
from pathlib import Path

def get_system_type():
    """Get the current operating system type."""
    return platform.system().lower()

def get_chrome_path():
    """Get the appropriate Chrome path based on the operating system."""
    system = get_system_type()
    if system == 'windows':
        return r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    elif system == 'linux':
        return "/usr/bin/google-chrome"
    else:
        return None

def get_chromium_path():
    """Get the appropriate Chromium path based on the operating system."""
    system = get_system_type()
    if system == 'windows':
        return r"C:\Program Files\Chromium\Application\chrome.exe"
    elif system == 'linux':
        return "/usr/bin/chromium-browser"
    else:
        return None

def get_default_download_path():
    """Get the default download path based on the operating system."""
    system = get_system_type()
    if system == 'windows':
        return str(Path.home() / "Downloads")
    elif system == 'linux':
        return str(Path.home() / "Downloads")
    else:
        return str(Path.home() / "Downloads")

def get_user_agent():
    """Get the appropriate user agent based on the operating system."""
    system = get_system_type()
    if system == 'windows':
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    elif system == 'linux':
        return 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    else:
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def ensure_directory_exists(path):
    """Ensure that a directory exists, create it if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_script_directory():
    """Get the directory where the script is located."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def setup_environment():
    """Setup the environment for the script."""
    script_dir = get_script_directory()
    
    # Create necessary directories
    directories = [
        'data',
        'logs',
        'drivers',
        'backups'
    ]
    
    for directory in directories:
        ensure_directory_exists(os.path.join(script_dir, directory))
    
    # Create necessary files if they don't exist
    files = [
        'data/accounts.txt',
        'data/done.txt',
        'data/errors.txt',
        'logs/logs.txt'
    ]
    
    for file in files:
        file_path = os.path.join(script_dir, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                pass

def is_windows():
    """Check if the current system is Windows."""
    return get_system_type() == 'windows'

def is_linux():
    """Check if the current system is Linux."""
    return get_system_type() == 'linux' 