#!/usr/bin/env python3
"""
Setup Configuration Script
Allows modifying config.py settings from console
"""

import os
import sys
import json
from pathlib import Path

def print_banner():
    print("="*60)
    print("UNICH Configuration Setup")
    print("="*60)

def get_input(prompt, default=""):
    """Get user input with default value"""
    if default:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def update_config_file():
    """Update config.py file with user inputs"""
    
    print_banner()
    print("Basic Settings Configuration:")
    print()
    
    # Get user inputs
    referral_code = get_input("Enter referral code", "phoenix-zeyad")
    gmail_email = get_input("Enter Gmail email", "zeyad60win@gmail.com")
    gmail_password = get_input("Enter Gmail app password", "fkhu nkdt unxx rsnu")
    
    print("\nCaptcha API Keys Setup:")
    print("(Leave empty if you don't want to use this service)")
    
    api_2captcha = get_input("Enter 2captcha API key", "")
    api_anticaptcha = get_input("Enter Anticaptcha API key", "")
    api_capsolver = get_input("Enter Capsolver API key", "")
    
    # Create new config content
    config_content = f'''import os
from pathlib import Path

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables for sensitive data
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', '{gmail_password}')  # Default fallback
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', '{gmail_email}')  # Default fallback

CONFIG = {{
    # Referral code used for registration
    'REFERRAL_CODE': '{referral_code}',

    # File paths
    'FILES': {{
        'ACCOUNTS': os.path.join(SCRIPT_DIR, 'data', 'accounts.txt'),
        'DONE': os.path.join(SCRIPT_DIR, 'data', 'done.txt'),
        'ERRORS': os.path.join(SCRIPT_DIR, 'data', 'errors.txt'),
        'LOGS': os.path.join(SCRIPT_DIR, 'logs', 'logs.txt')
    }},

    # Email settings for OTP verification
    'EMAIL': {{
        'IMAP_EMAIL': GMAIL_EMAIL,
        'IMAP_PASSWORD': GMAIL_PASSWORD,
        'IMAP_HOST': 'imap.gmail.com',
        'IMAP_PORT': 993,
        'USE_TLS': True,
        'OTP_TIMEOUT': 60000,
        'OTP_SEARCH_WINDOW': 300000,
        'SMTP_SERVER': 'smtp.gmail.com',
        'SMTP_PORT': 587,
        'SENDER_EMAIL': 'your-email@gmail.com',
        'SENDER_PASSWORD': 'your-app-password',
        'RECIPIENT_EMAIL': 'recipient@email.com'
    }},

    # Captcha service settings
    'CAPTCHA': {{
        'API_KEY_2CAPTCHA': os.getenv('API_KEY_2CAPTCHA', '{api_2captcha or "your_2captcha_api_key_here"}'),      # 2captcha API key
        'API_KEY_ANTICAPTCHA': os.getenv('API_KEY_ANTICAPTCHA', '{api_anticaptcha or "your_anticaptcha_api_key_here"}'),  # Anticaptcha API key
        'API_KEY_CAPSOLVER': os.getenv('API_KEY_CAPSOLVER', '{api_capsolver or "your_capsolver_api_key_here"}'),    # Capsolver API key
        'TIMEOUT': 120,
        'MAX_RETRIES': 3
    }},

    # Delays and timing
    'DELAYS': {{
        'PAGE_LOAD': 2,
        'AFTER_ACTION': 0.5,
        'BETWEEN_ACCOUNTS': 0.5,
        'RANDOM_DELAY': {{
            'ENABLED': True,
            'MIN': 1,
            'MAX': 2
        }},
        'AFTER_RESET': 3
    }},

    # Security and retry settings
    'SECURITY': {{
        'MAX_RETRIES': 3,
        'RETRY_DELAY': 10,
        'MAX_ACCOUNTS_PER_SESSION': 50,
        'SESSION_BREAK': 300
    }}
}}

def validate_config():
    """Validate configuration and create necessary directories/files"""
    # Create necessary directories
    for file_path in CONFIG['FILES'].values():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Create empty files if they don't exist
    for file_path in CONFIG['FILES'].values():
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                pass
    
    # Validate email settings
    if not CONFIG['EMAIL']['IMAP_PASSWORD'] or CONFIG['EMAIL']['IMAP_PASSWORD'] == 'your-app-password':
        print("Warning: Gmail password not set. Please set GMAIL_PASSWORD environment variable.")
    
    # Validate captcha settings
    captcha_keys = CONFIG['CAPTCHA']
    if not any([captcha_keys['API_KEY_2CAPTCHA'], captcha_keys['API_KEY_ANTICAPTCHA'], captcha_keys['API_KEY_CAPSOLVER']]):
        print("Warning: No captcha API keys set. Please set environment variables for captcha services.")
'''
    
    # Write to config.py (in parent directory)
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.py')
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("\nSuccessfully updated config.py file!")
        print("\nConfiguration Summary:")
        print(f"   Referral Code: {referral_code}")
        print(f"   Gmail Email: {gmail_email}")
        print(f"   2Captcha API: {'OK' if api_2captcha else 'NOT SET'}")
        print(f"   Anticaptcha API: {'OK' if api_anticaptcha else 'NOT SET'}")
        print(f"   Capsolver API: {'OK' if api_capsolver else 'NOT SET'}")
        
        return True
        
    except Exception as e:
        print(f"\nError updating file: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
UNICH Configuration Setup

Usage:
    python modules/setup_config.py          # Interactive setup
    python modules/setup_config.py --help   # Show this help

This script will help you configure:
- Referral code
- Gmail email and password
- Captcha API keys (2captcha, Anticaptcha, Capsolver)

The configuration will be saved to config.py
        """)
        return
    
    success = update_config_file()
    if success:
        print("\nYou can now run the main script:")
        print("   python main.py")
    else:
        print("\nFailed to setup configuration")

if __name__ == "__main__":
    main() 