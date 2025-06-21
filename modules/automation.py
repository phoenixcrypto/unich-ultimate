if __name__ == "__main__":
    print("\n❌ Running this file directly is considered fraudulent!\nPlease run the main script using: python main.py\n")
    exit(1)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
import time
import os
import random
import logging
from datetime import datetime, timedelta
from config import CONFIG
import imaplib
import email
import re
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from modules.utils import create_chrome_options, random_delay
from colorama import Fore, Style, init
import threading

# إعداد التسجيل
if CONFIG['LOGGING']['ENABLED']:
    logging.basicConfig(
        filename=CONFIG['FILES']['LOGS'],
        level=getattr(logging, CONFIG['LOGGING']['LEVEL']),
        format=CONFIG['LOGGING']['FORMAT'],
        datefmt=CONFIG['LOGGING']['DATE_FORMAT']
    )

init(autoreset=True)

def setup_driver():
    """
    Create a new Chrome driver instance with anti-detection settings
    """
    try:
        options = create_chrome_options()
        driver = uc.Chrome(
            options=options,
            use_subprocess=True,
            # version_main=137  # Commented out to allow auto-detection of Chrome version
        )
        driver.set_page_load_timeout(CONFIG['BROWSER']['TIMEOUT'])
        # Inject JS spoofing if present
        if hasattr(options, 'js_spoof_script'):
            try:
                driver.execute_script(options.js_spoof_script)
            except Exception as e:
                print(f"⚠️ Could not inject JS spoofing: {e}")
        return driver
    except Exception as e:
        print(f"❌ Error setting up Chrome driver: {str(e)}")
        raise

def log_error(email, error):
    with open(CONFIG['FILES']['ERRORS'], 'a') as file:
        timestamp = datetime.now().strftime(CONFIG['LOGGING']['DATE_FORMAT'])
        file.write(f"{timestamp} - {email}: {str(error)}\n")

def read_accounts(filename, done_file, error_file):
    accounts = []
    done_accounts = set()
    error_accounts = set()
    if os.path.exists(done_file):
        with open(done_file, 'r') as f:
            done_accounts = set(line.strip().split(':')[0] for line in f if line.strip())
    if os.path.exists(error_file):
        with open(error_file, 'r') as f:
            error_accounts = set(line.strip().split(':')[0] for line in f if line.strip())
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                email, password = line.strip().split(':')
                if email not in done_accounts and email not in error_accounts:
                    accounts.append((email, password))
    return accounts

def read_done_accounts(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, 'r') as file:
        return set(line.strip() for line in file)

def save_done_account(email):
    print(f"⏳ Attempting to save {email} to {CONFIG['FILES']['DONE']}") # Debug print before writing
    with open(CONFIG['FILES']['DONE'], 'a') as file:
        file.write(f"{email}\n")
        file.flush() # Force flushing the buffer
        try:
            os.fsync(file.fileno()) # Force writing to disk
            print(f"✅ Successfully wrote {email} to {CONFIG['FILES']['DONE']} and synced.") # Confirmation after sync
        except OSError as e:
            print(f"⚠️ Could not sync file {CONFIG['FILES']['DONE']}: {e}") # Handle potential sync errors

def read_otp_from_gmail(dot_trick_email):
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(CONFIG['EMAIL']['IMAP_HOST'], CONFIG['EMAIL']['IMAP_PORT'])
        mail.login(CONFIG['EMAIL']['IMAP_EMAIL'], CONFIG['EMAIL']['IMAP_PASSWORD'])
        mail.select('inbox')

        # Calculate the search date (5 minutes ago)
        search_date = (datetime.now() - timedelta(minutes=5)).strftime("%d-%b-%Y")
        
        # Search for emails with specific criteria (from noreply@unich.com first)
        search_criteria = f'(FROM "noreply@unich.com" TO "{dot_trick_email}" SINCE "{search_date}")'
        status, email_ids_raw = mail.search(None, search_criteria)
        
        # If no results from specific sender, try a broader search (only by 'TO' address)
        if status != 'OK' or not email_ids_raw or not email_ids_raw[0]:
            print(f"🔍 Searching for emails to {dot_trick_email} from the last 5 minutes (broader search)...")
            search_criteria = f'(TO "{dot_trick_email}" SINCE "{search_date}")'
            status, email_ids_raw = mail.search(None, search_criteria)
            
            if status != 'OK' or not email_ids_raw or not email_ids_raw[0]:
                raise Exception("No emails found for this address in the last 5 minutes")

        email_id_list = email_ids_raw[0].split()
        if not email_id_list:
            raise Exception("No email IDs found.")
            
        # Get the latest email
        latest_email_id = email_id_list[-1]
        status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        
        # Check if email data was fetched successfully and ensure it's bytes
        if status != 'OK' or not msg_data or not msg_data[0] or not isinstance(msg_data[0][1], bytes):
            raise Exception("Failed to fetch email data or invalid email data format.")

        raw_email_bytes = msg_data[0][1]
        msg = email.message_from_bytes(raw_email_bytes)
        
        otp_code = None
        
        # Prioritize HTML content for OTP extraction
        for part in msg.walk():
            ctype = part.get_content_type()
            
            if ctype == 'text/html':
                html_payload = part.get_payload(decode=True)
                if isinstance(html_payload, bytes):
                    html_body = html_payload.decode('utf-8', errors='replace')
                    soup = BeautifulSoup(html_body, 'html.parser')
                    # Search for exactly 6-digit numbers in the text extracted from HTML
                    otp_match = re.search(r'\b\d{6}\b', soup.get_text())
                    if otp_match:
                        otp_code = otp_match.group(0)
                        break # Found in HTML, exit loop
        
        # If OTP not found in HTML, try plain text parts
        if otp_code is None:
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    plain_payload = part.get_payload(decode=True)
                    if isinstance(plain_payload, bytes):
                        body = plain_payload.decode('utf-8', errors='replace')
                        otp_match = re.search(r'\b\d{6}\b', body)
                        if otp_match:
                            otp_code = otp_match.group(0)
                            break # Found in plain text, exit loop

        mail.logout()
        
        if not otp_code:
            raise Exception("OTP code not found in email content")
            
        print(f"📧 Found OTP code in email: {otp_code}")
        return otp_code
            
    except Exception as e:
        print(f"❌ Error reading OTP from Gmail: {str(e)}")
        raise

def process_account(email, password, retry_count=0):
    """
    Process a single account registration
    """
    driver = None
    try:
        print(f"🔄 Processing account: {email}")
        logging.info(f"Processing account: {email}")
        
        # Create new browser session
        driver = setup_driver()
        
        # Open referral link
        driver.get(CONFIG['REFERRAL_LINK'])
        random_delay(CONFIG['DELAYS']['PAGE_LOAD'], CONFIG['DELAYS']['PAGE_LOAD'])
        
        # Fill email
        email_input = WebDriverWait(driver, CONFIG['BROWSER']['TIMEOUT']).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_input.send_keys(email)
        print("✅ Email entered")
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])
        
        # Accept terms
        terms_checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        terms_checkbox.click()
        print("✅ Terms accepted")
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])
        
        # Click Sign Up
        signup_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign Up')]")
        signup_button.click()
        print("✅ Sign Up button clicked")
        
        # Handle first CAPTCHA
        print("⏳ Please solve the CAPTCHA manually in the browser...")
        input("Press Enter here after you solve the CAPTCHA...")
        
        # Add a small wait to ensure the next page loads
        random_delay(CONFIG['DELAYS']['PAGE_LOAD'], CONFIG['DELAYS']['PAGE_LOAD'])
        
        # --- OTP Reading Logic --- 
        print("⏳ Waiting for OTP code from Gmail...")
        otp_code = read_otp_from_gmail(email)
        print(f"✅ OTP code received: {otp_code}")
        
        # Wait for verification code input fields
        verification_inputs = WebDriverWait(driver, CONFIG['BROWSER']['TIMEOUT']).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[inputmode='numeric']"))
        )
            
        # Send each digit to the corresponding input field
        for i, digit in enumerate(otp_code):
            verification_inputs[i].send_keys(digit)
        print("✅ Verification code entered")
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])

        # Click Next button automatically after entering OTP
        try:
            next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
            next_button.click()
            print("✅ 'Next' button clicked automatically.")
            random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])
        except Exception as e:
            print(f"⚠️ Could not click 'Next' button automatically: {e}")
            input("Please click 'Next' manually, then press Enter here to continue...")

        # Handle second CAPTCHA (after Next, before password)
        print("⏳ Please solve the CAPTCHA manually in the browser...")
        input("Press Enter here after you solve the CAPTCHA...")
        
        # Wait for password input fields
        password_inputs = WebDriverWait(driver, CONFIG['BROWSER']['TIMEOUT']).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        
        # Enter password
        password_inputs[0].send_keys(password)
        password_inputs[1].send_keys(password)
        print("✅ Password entered")
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])

        # Click Confirm before CAPTCHA
        confirm_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
        confirm_button.click()
        print("✅ 'Confirm' button clicked. Waiting for CAPTCHA...")
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])
        
        # Handle third CAPTCHA (after Confirm)
        print("⏳ Please solve the CAPTCHA manually in the browser...")
        input("Press Enter here after you solve the CAPTCHA...")
        
        print("✅ Account successfully registered!")
        # Reset browser state
        driver.delete_all_cookies()
        driver.refresh()
        print(Fore.MAGENTA + Style.BRIGHT + "✅ Browser state reset (cookies deleted and page refreshed)")
        return True
        
    except Exception as e:
        print(f"❌ Error processing account {email}: {str(e)}")
        logging.error(f"Error processing account {email}: {str(e)}")
        if retry_count < CONFIG['SECURITY']['MAX_RETRIES']:
            print(f"🔄 Retrying... (Attempt {retry_count + 1}/{CONFIG['SECURITY']['MAX_RETRIES']})")
            random_delay(CONFIG['DELAYS']['BETWEEN_ACCOUNTS'], CONFIG['DELAYS']['BETWEEN_ACCOUNTS'])
            return process_account(email, password, retry_count + 1)
        else:
            print(f"❌ Max retries reached for account {email}")
            return False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        random_delay(CONFIG['DELAYS']['BETWEEN_ACCOUNTS'], CONFIG['DELAYS']['BETWEEN_ACCOUNTS'])

def move_account_between_files(email, password, src_file, dest_file):
    # Remove from src_file
    if os.path.exists(src_file):
        with open(src_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(src_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if not line.strip().startswith(email + ':'):
                    f.write(line)
    # Add to dest_file if not already present
    if os.path.exists(dest_file):
        with open(dest_file, 'r', encoding='utf-8') as f:
            if any(line.strip().startswith(email + ':') for line in f):
                return
    with open(dest_file, 'a', encoding='utf-8') as f:
        f.write(f"{email}:{password}\n")

def main():
    """
    Main function to process all accounts
    """
    accounts = read_accounts(CONFIG['FILES']['ACCOUNTS'], CONFIG['FILES']['DONE'], CONFIG['FILES']['ERRORS'])
    for email, password in accounts:
        print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50 + "\n")
        try:
            success = process_account(email, password)
            if success:
                move_account_between_files(email, password, CONFIG['FILES']['ACCOUNTS'], CONFIG['FILES']['DONE'])
            else:
                move_account_between_files(email, password, CONFIG['FILES']['ACCOUNTS'], CONFIG['FILES']['ERRORS'])
        except Exception as e:
            print(f"❌ Error in main loop processing {email}: {str(e)}")
            logging.error(f"Error in main loop processing {email}: {str(e)}")
            move_account_between_files(email, password, CONFIG['FILES']['ACCOUNTS'], CONFIG['FILES']['ERRORS'])
        finally:
            random_delay(CONFIG['DELAYS']['BETWEEN_ACCOUNTS'], CONFIG['DELAYS']['BETWEEN_ACCOUNTS'])

if __name__ == "__main__":
    print("\n❌ Running this file directly is considered fraudulent!\nPlease run the main script using: python main.py\n")
    exit(1) 
