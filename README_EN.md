# 🚀 UNICH Project Automation

A comprehensive tool for generating Gmail dot trick emails and automating referral registrations on the Unich platform, with full automation support, CAPTCHA solving, and account management.

## ⭐️ Features

- Generate unlimited Gmail dot trick emails
- Fully automated referral registration for Unich
- Manual CAPTCHA solving support
- OTP reading from Gmail
- Automatic account management (successful/failed tracking)
- Detailed logs for all operations and errors
- Colorful interactive interface
- Full support for Windows and Linux systems
- Anti-detection browser settings

## 🛠️ Requirements

### Windows System
- Python 3.8 or higher
- Google Chrome or Chromium browser
- Git (optional)

### Linux System (Ubuntu/Debian)
- Python 3.8 or higher
- Google Chrome or Chromium browser
- Git (optional)

## ⚙️ Installation and Setup

### Quick Installation

#### Windows
```bash
# Run the installer
install.bat

# Or run the automation
run.bat
```

#### Linux
```bash
# Make scripts executable
chmod +x install.sh run.sh

# Run the installer
./install.sh

# Or run the automation
./run.sh
```

### Manual Installation

#### Windows

1. **Clone the project:**
```bash
git clone https://github.com/phoenixcrypto/UNICH-REF.git
cd UNICH-REF
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. **Install required libraries:**
```bash
pip install -r requirements.txt
```

4. **Install Chrome/Chromium browser:**
- Download Chrome from: https://www.google.com/chrome/
- Or download Chromium from: https://www.chromium.org/getting-involved/download-chromium/

#### Linux (Ubuntu/Debian)

1. **Install basic requirements:**
```bash
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-pip python3-venv wget unzip
```

2. **Clone the project:**
```bash
git clone https://github.com/phoenixcrypto/UNICH-REF.git
cd UNICH-REF
```

3. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

4. **Install required libraries:**
```bash
pip install -r requirements.txt
```

5. **Install Chrome/Chromium browser:**
```bash
# To install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install

# Or to install Chromium
sudo apt install chromium-browser
```

## 📱 Usage

1. **Activate virtual environment:**
```bash
# On Windows
.\venv\Scripts\activate

# On Linux
source venv/bin/activate
```

2. **Run the script:**
```bash
python main.py
```

3. **Choose from the menu:**
- Option 1: Generate Gmail dot trick emails
- Option 2: Run referral automation
- Option 0: Exit

## ⚙️ Configuration

You can modify the `config.py` file to customize:
- Referral link and code
- Email settings
- Browser settings
- Delays and timing
- Security settings
- Registration preferences

## 📁 Project Structure

```
UNICH-REF/
├── data/
│   ├── accounts.txt         # Accounts to be processed
│   ├── done.txt            # Successful accounts
│   └── errors.txt          # Failed accounts
├── logs/
│   └── logs.txt            # Operation logs
├── modules/
│   ├── automation.py       # Automation logic
│   ├── gmail_dot_generator.py # Email generation
│   ├── system_utils.py     # System utilities
│   └── utils.py            # Helper utilities
├── drivers/                # Browser files
├── backups/                # Backups
├── config.py              # Configuration file
├── main.py                # Main file
└── requirements.txt       # Required libraries
```

## 🔧 Troubleshooting

### Common Issues

1. **Chrome/Chromium not found:**
- Ensure browser is installed
- Check path in config.py
- Try using Chromium instead of Chrome

2. **ModuleNotFoundError:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

3. **Permission issues (Linux):**
```bash
chmod -R 755 .
```

4. **UnicodeEncodeError:**
```bash
# On Windows
set PYTHONIOENCODING=utf-8

# On Linux
export PYTHONIOENCODING=utf-8
```

## 🤝 Contributing

1. Fork the project
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, join the Telegram channel: [@PhoenixCrypto_PC](https://t.me/PhoenixCrypto_PC)

## ⚠️ Important Notes

- This script is educational and used at your own responsibility
- Do not share your data with any untrusted parties
- Follow the Telegram channel for latest updates and tutorials 