import os
from pathlib import Path

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables for sensitive data
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', 'fkhu nkdt unxx rsnu')  # Default fallback
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', 'zeyad60win@gmail.com')  # Default fallback

CONFIG = {
    # Referral code used for registration
    'REFERRAL_CODE': 'phoenix-zeyad',

    # File paths
    'FILES': {
        'ACCOUNTS': os.path.join(SCRIPT_DIR, 'data', 'accounts.txt'),
        'DONE': os.path.join(SCRIPT_DIR, 'data', 'done.txt'),
        'ERRORS': os.path.join(SCRIPT_DIR, 'data', 'errors.txt'),
        'LOGS': os.path.join(SCRIPT_DIR, 'logs', 'logs.txt')
    },

    # Email settings for OTP verification
    'EMAIL': {
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
    },

    # Captcha service settings
    'CAPTCHA': {
        'API_KEY_2CAPTCHA': os.getenv('API_KEY_2CAPTCHA', 'your_2captcha_api_key_here'),      # 2captcha API key
        'API_KEY_ANTICAPTCHA': os.getenv('API_KEY_ANTICAPTCHA', 'your_anticaptcha_api_key_here'),  # Anticaptcha API key
        'API_KEY_CAPSOLVER': os.getenv('API_KEY_CAPSOLVER', 'your_capsolver_api_key_here'),    # Capsolver API key
        'TIMEOUT': 120,
        'MAX_RETRIES': 3
    },

    # Delays and timing
    'DELAYS': {
        'PAGE_LOAD': 2,
        'AFTER_ACTION': 0.5,
        'BETWEEN_ACCOUNTS': 0.5,
        'RANDOM_DELAY': {
            'ENABLED': True,
            'MIN': 1,
            'MAX': 2
        },
        'AFTER_RESET': 3
    },

    # Security and retry settings
    'SECURITY': {
        'MAX_RETRIES': 3,
        'RETRY_DELAY': 10,
        'MAX_ACCOUNTS_PER_SESSION': 50,
        'SESSION_BREAK': 300
    }
}

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
        print("⚠️  Warning: Gmail password not set. Please set GMAIL_PASSWORD environment variable.")
    
    # Validate captcha settings
    captcha_keys = CONFIG['CAPTCHA']
    if not any([captcha_keys['API_KEY_2CAPTCHA'], captcha_keys['API_KEY_ANTICAPTCHA'], captcha_keys['API_KEY_CAPSOLVER']]):
        print("⚠️  Warning: No captcha API keys set. Please set environment variables for captcha services.")
