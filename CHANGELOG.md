# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-01-XX

### Added
- Initial release of UNICH-REF Automation tool
- Gmail dot trick email generator
- Automated referral registration for Unich platform
- Manual CAPTCHA solving support
- OTP reading from Gmail
- Account management system (successful/failed accounts tracking)
- Cross-platform support (Windows/Linux)
- Colorful interactive interface
- Comprehensive logging system
- Anti-detection browser settings
- Easy installation scripts for Windows and Linux

### Fixed
- Fixed indentation error in `modules/automation.py`
- Added `setuptools` dependency for Python 3.13 compatibility
- Updated `undetected-chromedriver` to version 3.5.4
- Fixed import issues with `distutils` in Python 3.13

### Technical Details
- Compatible with Python 3.8 - 3.13
- Uses Selenium WebDriver with undetected-chromedriver
- IMAP integration for Gmail OTP reading
- BeautifulSoup for email parsing
- Colorama for terminal colors
- Fake-useragent for browser fingerprinting

### Installation
- Windows: Run `install.bat`
- Linux: Run `./install.sh`
- Manual: Follow README.md instructions

### Usage
- Windows: Run `run.bat`
- Linux: Run `./run.sh`
- Manual: `python main.py` 