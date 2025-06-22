# 🤖 UNICH Automation Project (PhoenixCrypto_PC)

[![Phoenix Crypto Channel](https://img.shields.io/badge/Telegram%20Channel-PhoenixCrypto__PC-blue?logo=telegram)](https://t.me/PhoenixCrypto_PC)
[![Phoenix Chat Group](https://img.shields.io/badge/Telegram%20Group-Phoenix__Channeli-blueviolet?logo=telegram)](https://t.me/Phoenix_Channeli)

---

## 🚀 Introduction

A complete automation project for generating Gmail dot trick emails, fully automated Unich airdrop registration, automatic mining activation, with full support for captcha solving and OTP reading from email—all in a fast, user-friendly interface.

---

## ✨ Main Features

- ♾️ **Generate unlimited Gmail dot trick emails**
- 🤖 **Fully automated Unich registration (Selenium or API)**
- ⛏️ **Automatic mining activation for all accounts**
- 🔐 **Automatic OTP reading from Gmail**
- 🧩 **Automatic captcha solving (2Captcha)**
- 📊 **Organized logs and result files**
- 🛠️ **Customizable and easy to modify**

---

## 🗂️ Table of Contents

- [⚡️ Quick Install & Run](#️-quick-install--run)
- [⚙️ config.py Setup](#️-configpy-setup)
- [Features Explained](#features-explained)
- [File Structure](#file-structure)
- [FAQ](#faq)
- [Support & Contact](#support--contact)
- [License](#license)

---

## ⚡️ Quick Install & Run

### 🪟 Windows
```bat
install.bat
run.bat
```

### 🐧 Linux/Mac
```bash
chmod +x install.sh run.sh
./install.sh
./run.sh
```

---

## ⚙️ config.py Setup

Before running, configure `config.py` for correct operation. Key settings:

```python
CONFIG = {
    # Email settings for automatic OTP reading
    'EMAIL': {
        'IMAP_EMAIL': 'your_email@gmail.com',
        'IMAP_PASSWORD': 'your_app_password',  # Use Google App Password
        'IMAP_HOST': 'imap.gmail.com',
        'IMAP_PORT': 993
    },
    # 2Captcha settings
    'CAPTCHA': {
        'API_KEY': 'your_2captcha_api_key_here',  # Put your key here
        'TIMEOUT': 120,
        'MAX_RETRIES': 3
    },
    # Your referral code
    'REFERRAL_CODE': 'ABC123'
    # ... other settings as needed
}
```

- **Note:**  
  - To get a Google App Password, enable 2FA and create an app-specific password.
  - To get a 2Captcha key, register at [2Captcha](https://2captcha.com/) and copy your API Key.

---

## 📝 Features Explained

### 1. Gmail dot trick email generation
- Enter username and password.
- Generates thousands of unique emails (all go to the same inbox).
- Saved in `data/accounts.txt`.

### 2. Automated registration (Selenium)
- Opens Chrome browser automatically.
- Registers each email in Unich with manual captcha solving.
- Reads OTP from Gmail automatically.

### 3. Fast registration (API + 2Captcha)
- Registers accounts directly via API.
- Solves captcha automatically (2Captcha).
- Reads OTP from Gmail automatically.
- Much faster than browser mode.

### 4. Mining activation for all accounts
- Reads accounts from `data/done.txt`.
- Activates mining for each account automatically.
- Logs results in `logs/mining_api.log`.

---

## 📁 File Structure

| File/Folder                  | Description                                  |
|------------------------------|----------------------------------------------|
| main.py                      | Main menu and feature launcher               |
| modules/automation.py        | Selenium-based registration logic            |
| modules/api_interaction.py   | Fast API-based registration logic            |
| modules/mining_api.py        | Automatic mining activation                  |
| modules/gmail_dot_generator.py | Gmail dot trick email generator           |
| config.py                    | Project settings (email, captcha, etc.)      |
| data/accounts.txt            | Emails and passwords for registration        |
| data/done.txt                | Successfully registered accounts             |
| logs/mining_api.log          | Mining operations log                        |
| requirements.txt             | Required Python packages                     |

---

## ❓ FAQ

- **OTP not received?**
  - Check Gmail settings in config.py.
  - Try another email or check spam/junk folder.
- **Captcha not solved automatically?**
  - Make sure your 2Captcha key is set in config.py.
- **Browser not opening?**
  - Ensure ChromeDriver matches your Chrome version.
- **Other errors?**
  - See TROUBLESHOOTING.md or contact us.

---

## 📞 Support & Contact

- Updates Channel: [PhoenixCrypto_PC](https://t.me/PhoenixCrypto_PC)
- Discussion Group: [Phoenix_Channeli](https://t.me/Phoenix_Channeli)
- YouTube: [@PhoenixCrypto_PC](https://www.youtube.com/@PhoenixCrypto_PC)

---

## ⚖️ License & Disclaimer

- This project is open source for educational and experimental use only.
- Use at your own risk.
- All rights reserved © PhoenixCrypto_PC 