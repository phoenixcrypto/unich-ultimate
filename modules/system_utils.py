import os
import platform
import sys
from pathlib import Path

def get_system_type():
    """Get the current operating system type."""
    return platform.system().lower()

def get_default_download_path():
    """Get the default download path based on the operating system."""
    system = get_system_type()
    return str(Path.home() / "Downloads")

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