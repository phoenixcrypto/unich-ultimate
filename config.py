# Script Configuration
CONFIG = {
    # Referral
    'REFERRAL_LINK': 'https://unich.com/en/airdrop/sign-up?ref=XgRCPPo8k8',
    'REFERRAL_CODE': 'XgRCPPo8k8',

    # File paths
    'FILES': {
        'ACCOUNTS': 'data/accounts.txt',
        'DONE': 'data/done.txt',
        'ERRORS': 'data/errors.txt',
        'LOGS': 'logs/logs.txt'
    },

    # Email settings
    'EMAIL': {
        'IMAP_EMAIL': 'eltmsahzeyad4@gmail.com',
        'IMAP_PASSWORD': 'euhh vngy eylx jdap',
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

    # Browser settings
    'BROWSER': {
        'HEADLESS': False,
        'WINDOW_SIZE': (1920, 1080),
        'TIMEOUT': 20,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'DISABLE_IMAGES': True,
        'DISABLE_GPU': True,
        'DISABLE_EXTENSIONS': True,
        'NO_SANDBOX': True,
        'DISABLE_DEV_SHM': True
    },

    # Delays
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

    # Security
    'SECURITY': {
        'MAX_RETRIES': 3,
        'RETRY_DELAY': 10,
        'MAX_ACCOUNTS_PER_SESSION': 50,
        'SESSION_BREAK': 300
    },

    # Automation
    'AUTOMATION': {
        'DELAY_BETWEEN_ACCOUNTS': 5,
        'MAX_RETRIES': 3,
        'TIMEOUT': 30,
        'WAIT_TIME': 10
    },

    # Logging
    'LOGGING': {
        'ENABLED': True,
        'LEVEL': 'INFO',
        'FORMAT': '%(asctime)s - %(levelname)s - %(message)s',
        'DATE_FORMAT': '%Y-%m-%d %H:%M:%S'
    },

    # Messages
    'MESSAGES': {
        'START': '🔄 Starting registration: {}',
        'SKIP': '⏭️ Skipping account {} - already processed',
        'SUCCESS': '✅ Account created successfully: {}',
        'MILESTONE': '🎉 {} referrals done! Take a break!',
        'PROGRESS': '📈 Accounts processed so far: {}',
        'ERROR': '❌ Error occurred: {}',
        'RETRY': '🔄 Retrying ({}/{}) for account: {}',
        'SESSION_START': '🚀 New session started - remaining accounts: {}',
        'SESSION_END': '⏸️ Session ended - taking a break for {} minutes',
        'SUMMARY': {
            'SUCCESS': '✅ Successful accounts: {}',
            'TOTAL': '📝 Total attempts: {}',
            'FAILED': '❌ Failed accounts: {}',
            'SKIPPED': '⏭️ Skipped accounts: {}'
        }
    },

    # Prompts
    'PROMPTS': {
        'CAPTCHA': '⏳ Press Enter after solving the CAPTCHA...',
        'VERIFICATION': '📧 Enter the verification code sent to your email: ',
        'CONTINUE': 'Press Enter to continue...',
        'RETRY': '🔄 Retry? (y/n): '
    },

    # Monitoring
    'MONITORING': {
        'CHECK_INTERVAL': 60,
        'ALERT_THRESHOLD': 0.8,
        'MAX_FILE_SIZE': 1024 * 1024
    },

    # Backup
    'BACKUP': {
        'INTERVAL': 3600,
        'MAX_BACKUPS': 5,
        'BACKUP_DIR': 'backups'
    },

    # Remote
    'REMOTE': {
        'HOST': 'localhost',
        'PORT': 5000,
        'MAX_CLIENTS': 5
    },

    # Reports
    'REPORTS': {
        'DAILY_TIME': '00:00',
        'WEEKLY_DAY': 'monday',
        'WEEKLY_TIME': '00:00'
    }
} 