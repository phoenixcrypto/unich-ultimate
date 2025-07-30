import requests
import time
import random
from colorama import Fore, Style, init
from config import CONFIG, validate_config
import imaplib
import email
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from modules.utils import log_success, log_error, log_warning, log_info, log_progress

init(autoreset=True)

# Validate config on import
validate_config()

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
]

def retry_with_backoff(func, max_retries=3, base_delay=1):
    """
    Retry function with exponential backoff and intelligent logging
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                # Last attempt failed, raise the exception
                log_error(f"All {max_retries} attempts failed. Final error: {str(e)}")
                raise e
            
            # Calculate delay with exponential backoff and jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            
            # Log the retry with more details
            if "timeout" in str(e).lower() or "too long" in str(e).lower():
                log_warning(f"Attempt {attempt + 1} failed due to timeout: {str(e)}. Retrying in {delay:.2f} seconds...")
            else:
                log_warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay:.2f} seconds...")
            
            time.sleep(delay)

# === Official function to get reCAPTCHA v2 token from 2captcha ===
def get_2captcha_token(site_key, url, api_key):
    """حل reCAPTCHA V2 باستخدام 2captcha"""
    def _solve_captcha():
        # Step 1: Submit captcha for solving
        req = requests.post('http://2captcha.com/in.php', data={
            'key': api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': url,
            'json': 1
        })
        
        response_data = req.json()
        if response_data.get('status') != 1:
            raise Exception(f"2captcha submission error: {response_data.get('error_text', 'Unknown error')}")
        
        rid = response_data.get('request')
        if not rid:
            raise Exception(f"2captcha error: {req.text}")
        
        log_info(f"2captcha: Captcha submitted successfully. Request ID: {rid}")
        
        # Step 2: Wait for solution with intelligent polling
        max_wait_time = 600  # 10 minutes maximum
        check_interval = 10  # Check every 10 seconds initially
        total_wait_time = 0
        
        while total_wait_time < max_wait_time:
            time.sleep(check_interval)
            total_wait_time += check_interval
            
            try:
                res = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={rid}&json=1')
                result_data = res.json()
                
                if result_data.get('status') == 1:
                    # Success! Captcha solved
                    log_success(f"2captcha: Captcha solved successfully in {total_wait_time} seconds")
                    return result_data['request']
                
                elif result_data.get('request') == 'CAPCHA_NOT_READY':
                    # Still processing, continue waiting
                    if total_wait_time % 60 == 0:  # Log every minute
                        log_info(f"2captcha: Still waiting for solution... ({total_wait_time}s elapsed)")
                    continue
                
                else:
                    # Error occurred
                    error_msg = result_data.get('request', 'Unknown error')
                    raise Exception(f"2captcha solving error: {error_msg}")
                    
            except requests.RequestException as e:
                log_warning(f"2captcha: Network error while checking solution: {e}")
                continue
        
        # Timeout reached
        raise Exception(f'2captcha: Captcha solving timeout after {max_wait_time} seconds')
    
    return retry_with_backoff(_solve_captcha, max_retries=2, base_delay=2)

def get_anticaptcha_token(site_key, url, api_key):
    """حل reCAPTCHA V2 باستخدام anticaptcha"""
    def _solve_captcha():
        from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
        
        solver = recaptchaV2Proxyless()
        solver.set_key(api_key)
        solver.set_website_url(url)
        solver.set_website_key(site_key)
        solver.set_soft_id(0)
        
        log_info("Anticaptcha: Starting captcha solving...")
        
        g_response = solver.solve_and_return_solution()
        
        if g_response != 0:
            log_success("Anticaptcha: Captcha solved successfully")
            return g_response
        else:
            error_code = solver.error_code
            error_msg = solver.error_code_description if hasattr(solver, 'error_code_description') else f"Error code: {error_code}"
            raise Exception(f"Anticaptcha error: {error_msg}")
    
    return retry_with_backoff(_solve_captcha, max_retries=2, base_delay=2)

def get_capsolver_token(site_key, url, api_key):
    """حل reCAPTCHA V2 باستخدام capsolver"""
    def _solve_captcha():
        # Step 1: Create task
        create_payload = {
            "clientKey": api_key,
            "task": {
                "type": "RecaptchaV2TaskProxyless",
                "websiteURL": url,
                "websiteKey": site_key
            }
        }
        
        r = requests.post("https://api.capsolver.com/createTask", json=create_payload)
        response_data = r.json()
        
        if response_data.get("status") != "ready":
            error_msg = response_data.get("errorDescription", "Unknown error")
            raise Exception(f"Capsolver createTask error: {error_msg}")
        
        task_id = response_data.get("taskId")
        if not task_id:
            raise Exception(f"Capsolver createTask error: {r.text}")
        
        log_info(f"Capsolver: Task created successfully. Task ID: {task_id}")
        
        # Step 2: Wait for solution with intelligent polling
        max_wait_time = 600  # 10 minutes maximum
        check_interval = 10  # Check every 10 seconds initially
        total_wait_time = 0
        
        while total_wait_time < max_wait_time:
            time.sleep(check_interval)
            total_wait_time += check_interval
            
            try:
                res = requests.post("https://api.capsolver.com/getTaskResult", json={
                    "clientKey": api_key, 
                    "taskId": task_id
                })
                data = res.json()
                
                if data.get("status") == "ready":
                    # Success! Captcha solved
                    log_success(f"Capsolver: Captcha solved successfully in {total_wait_time} seconds")
                    return data["solution"]["gRecaptchaResponse"]
                
                elif data.get("status") == "processing":
                    # Still processing, continue waiting
                    if total_wait_time % 60 == 0:  # Log every minute
                        log_info(f"Capsolver: Still waiting for solution... ({total_wait_time}s elapsed)")
                    continue
                
                else:
                    # Error occurred
                    error_msg = data.get("errorDescription", "Unknown error")
                    raise Exception(f"Capsolver solving error: {error_msg}")
                    
            except requests.RequestException as e:
                log_warning(f"Capsolver: Network error while checking solution: {e}")
                continue
        
        # Timeout reached
        raise Exception(f"Capsolver: Captcha solving timeout after {max_wait_time} seconds")
    
    return retry_with_backoff(_solve_captcha, max_retries=2, base_delay=2)

def get_captcha_token(site_key, url, force_provider=None):
    """Unified function: chooses the first available provider from config.py, or uses forced provider if set."""
    cap = CONFIG['CAPTCHA']
    if force_provider:
        provider = force_provider.lower()
        if provider == '2captcha':
            key = cap.get('API_KEY_2CAPTCHA')
            if not key:
                raise Exception('2captcha API_KEY_2CAPTCHA is not set in config.py')
            return get_2captcha_token(site_key, url, key)
        elif provider == 'anticaptcha':
            key = cap.get('API_KEY_ANTICAPTCHA')
            if not key:
                raise Exception('anticaptcha API_KEY_ANTICAPTCHA is not set in config.py')
            return get_anticaptcha_token(site_key, url, key)
        elif provider == 'capsolver':
            key = cap.get('API_KEY_CAPSOLVER')
            if not key:
                raise Exception('capsolver API_KEY_CAPSOLVER is not set in config.py')
            return get_capsolver_token(site_key, url, key)
        else:
            raise Exception(f'Unknown forced CAPTCHA provider: {force_provider}')
    # Auto-detect as before
    if cap.get('API_KEY_2CAPTCHA'):
        return get_2captcha_token(site_key, url, cap['API_KEY_2CAPTCHA'])
    elif cap.get('API_KEY_ANTICAPTCHA'):
        return get_anticaptcha_token(site_key, url, cap['API_KEY_ANTICAPTCHA'])
    elif cap.get('API_KEY_CAPSOLVER'):
        return get_capsolver_token(site_key, url, cap['API_KEY_CAPSOLVER'])
    else:
        raise Exception('No API key set for any captcha provider in config.py')

class UnichAPI:
    def __init__(self):
        self.base_url = "https://api.unich.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://unich.com',
            'Referer': 'https://unich.com/en/airdrop/sign-up',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        })
        self.recaptcha_site_key = "6LdEl4grAAAAAB8fg8oGNPZhhcUbR4uuM8VQI0H0"
        self.recaptcha_url = "https://unich.com/en/airdrop/sign-up"

    def read_otp_from_gmail(self, target_email):
        try:
            log_info("Reading OTP from Gmail...")
            mail = imaplib.IMAP4_SSL(CONFIG['EMAIL']['IMAP_HOST'], CONFIG['EMAIL']['IMAP_PORT'])
            mail.login(CONFIG['EMAIL']['IMAP_EMAIL'], CONFIG['EMAIL']['IMAP_PASSWORD'])
            mail.select('inbox')
            search_date = (datetime.now() - timedelta(minutes=10)).strftime("%d-%b-%Y")
            search_criteria = f'(FROM "noreply@unich.com" TO "{target_email}" SINCE "{search_date}")'
            status, email_ids_raw = mail.search(None, search_criteria)
            if status != 'OK' or not email_ids_raw or not email_ids_raw[0]:
                search_criteria = f'(TO "{target_email}" SINCE "{search_date}")'
                status, email_ids_raw = mail.search(None, search_criteria)
                if status != 'OK' or not email_ids_raw or not email_ids_raw[0]:
                    raise Exception("No emails found for this address in the last 10 minutes")
            email_id_list = email_ids_raw[0].split()
            if not email_id_list:
                raise Exception("No email IDs found.")
            latest_email_id = email_id_list[-1]
            status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
            if status != 'OK' or not msg_data or not msg_data[0]:
                raise Exception("Failed to fetch email data or invalid email data format.")
            raw_email = msg_data[0][1] if isinstance(msg_data[0], tuple) else msg_data[0]
            if isinstance(raw_email, str):
                raw_email_bytes = raw_email.encode('utf-8')
            else:
                raw_email_bytes = raw_email
            msg = email.message_from_bytes(raw_email_bytes)
            otp_code = None
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == 'text/html':
                    html_payload = part.get_payload(decode=True)
                    if isinstance(html_payload, bytes):
                        html_body = html_payload.decode('utf-8', errors='replace')
                        soup = BeautifulSoup(html_body, 'html.parser')
                        otp_match = re.search(r'\b\d{6}\b', soup.get_text())
                        if otp_match:
                            otp_code = otp_match.group(0)
                            break
            if otp_code is None:
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        plain_payload = part.get_payload(decode=True)
                        if isinstance(plain_payload, bytes):
                            body = plain_payload.decode('utf-8', errors='replace')
                            otp_match = re.search(r'\b\d{6}\b', body)
                            if otp_match:
                                otp_code = otp_match.group(0)
                                break
            mail.logout()
            if not otp_code:
                raise Exception("OTP code not found in email content")
            log_success(f"OTP found: {otp_code}")
            return otp_code
        except Exception as e:
            log_error("Error reading OTP from Gmail", str(e))
            raise
    
    def request_otp(self, email, force_captcha_provider=None):
        try:
            log_info(f"Requesting OTP for {email}...")
            recaptcha_token = get_captcha_token(self.recaptcha_site_key, self.recaptcha_url, force_provider=force_captcha_provider)
            payload = {
                "action": "REGISTER",
                "email": email,
                "g-recaptcha-response": recaptcha_token
            }
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/auth/otp/request",
                json=payload,
            )
            if response.status_code in [200, 201]:
                data = response.json()
                log_info(f"Response: {data}")
                if data.get('code') == 'OK':
                    otp_sent = data.get('data', {}).get('otpSent')
                    log_info(f"OTP sent value: {otp_sent} (type: {type(otp_sent)})")
                    if otp_sent == True:
                        log_success("OTP request sent successfully!")
                        return True
                    else:
                        raise Exception(f"OTP not sent: {data}")
                else:
                    raise Exception(f"API error: {data}")
            else:
                raise Exception(f"HTTP error: {response.status_code} - {response.text}")
        except Exception as e:
            log_error("OTP request failed", str(e))
            raise
    
    def verify_otp(self, email, otp, force_captcha_provider=None):
        try:
            log_info("Verifying OTP...")
            recaptcha_token = get_captcha_token(self.recaptcha_site_key, self.recaptcha_url, force_provider=force_captcha_provider)
            payload = {
                "email": email,
                "otp": otp,
                "g-recaptcha-response": recaptcha_token
            }
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/auth/otp/resolve",
                json=payload,
            )
            if response.status_code in [200, 201]:
                data = response.json()
                log_info(f"OTP verification response: {data}")
                if data.get('code') == 'OK':
                    otp_token = data.get('data', {}).get('otpToken')
                    if otp_token:
                        log_success("OTP verified successfully!")
                        return otp_token
                    else:
                        raise Exception(f"No OTP token received: {data}")
                else:
                    raise Exception(f"OTP verification failed: {data.get('message')}")
            else:
                raise Exception(f"OTP verification failed: {response.text}")
        except Exception as e:
            log_error("OTP verification failed", str(e))
            raise
    
    def sign_up(self, email, password, otp_token, force_captcha_provider=None):
        try:
            log_info("Completing registration...")
            recaptcha_token = get_captcha_token(self.recaptcha_site_key, self.recaptcha_url, force_provider=force_captcha_provider)
            payload = {
                "email": email,
                "password": password,
                "otpToken": otp_token,
                "g-recaptcha-response": recaptcha_token
            }
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/auth/sign-up",
                json=payload,
            )
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get('code') == 'OK':
                    access_token = data.get('data', {}).get('accessToken')
                    if access_token:
                        log_success("Account registered successfully!")
                        return access_token
                    else:
                        raise Exception("No access token received")
                else:
                    raise Exception(f"Registration failed: {data.get('message')}")
            else:
                raise Exception(f"Registration failed: {response.text}")
        except Exception as e:
            log_error("Registration failed", str(e))
            raise
    
    def apply_referral(self, access_token, referral_code):
        try:
            log_info("Applying referral code...")
            payload = {"code": referral_code}
            headers = self.session.headers.copy()
            headers['Authorization'] = f"Bearer {access_token}"
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/ref/refer-sign-up",
                json=payload,
                headers=headers
            )
            log_info(f"Referral Response Status: {response.status_code}")
            try:
                log_info(f"Referral Response Body: {response.json()}")
            except Exception:
                log_info(f"Referral Response Body (non-JSON): {response.text}")
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get('code') == 'OK':
                    log_success("Referral code applied successfully!")
                    return True
                else:
                    raise Exception(f"Referral application failed: {data.get('message')}")
            else:
                raise Exception(f"Referral application failed: {response.text}")
        except Exception as e:
            log_error("Referral application failed", str(e))
            raise
    
    def start_mining(self, access_token):
        try:
            log_info("Starting mining...")
            headers = self.session.headers.copy()
            headers['Authorization'] = f"Bearer {access_token}"
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/mining/start",
                headers=headers
            )
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get('code') == 'OK':
                    log_success("Mining started successfully!")
                    return True
                else:
                    raise Exception(f"Mining start failed: {data.get('message')}")
            else:
                raise Exception(f"Mining start failed: {response.text}")
        except Exception as e:
            log_error("Mining start failed", str(e))
            raise

def process_account_api(email, password, retry_count=0, force_captcha_provider=None):
    """Process a single account using API, with optional forced captcha provider."""
    api = UnichAPI()
    try:
        log_info(f"{'='*50}")
        log_info(f"Processing account: {email}")
        log_info(f"{'='*50}")
        # Step 1: Request OTP
        if not api.request_otp(email, force_captcha_provider=force_captcha_provider):
            raise Exception("Failed to request OTP")
        # Minimal wait for OTP delivery
        log_info("Waiting for OTP delivery...")
        time.sleep(5)  # Only short, essential wait
        # Step 2: Read OTP from Gmail
        otp_code = api.read_otp_from_gmail(email)
        # Step 3: Verify OTP
        otp_token = api.verify_otp(email, otp_code, force_captcha_provider=force_captcha_provider)
        # Step 4: Complete registration
        access_token = api.sign_up(email, password, otp_token, force_captcha_provider=force_captcha_provider)
        # Step 5: Apply referral code
        api.apply_referral(access_token, CONFIG['REFERRAL_CODE'])
        log_info("All steps completed, preparing to save account info...")
        account_info = {
            "email": email,
            "password": password,
            "token": access_token,
            "created_at": datetime.now().isoformat()
        }
        return account_info
    except KeyboardInterrupt:
        log_warning("Process interrupted by user")
        raise
    except Exception as e:
        error_msg = f"Error processing account {email}: {str(e)}"
        log_error(error_msg)
        
        # Save error to errors.txt file
        try:
            with open(CONFIG['FILES']['ERRORS'], 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().isoformat()} - {email} - {str(e)}\n")
        except Exception as save_error:
            log_error(f"Failed to save error to file: {save_error}")
        
        if "OTP_BLOCK_BETWEEN_2_TIMES" in str(e):
            log_warning("OTP blocked, waiting longer before retry...")
            time.sleep(60)
        if retry_count < CONFIG['SECURITY']['MAX_RETRIES']:
            log_warning(f"Retrying... (Attempt {retry_count + 1}/{CONFIG['SECURITY']['MAX_RETRIES']})")
            return process_account_api(email, password, retry_count + 1, force_captcha_provider=force_captcha_provider)
        else:
            log_error(f"Max retries reached for account {email}")
            return None
    finally:
        pass  # No random_delay between accounts

def save_account_info(account_info, output_file="data/done.txt"):
    """Save account information to done.txt file and remove it from accounts file"""
    try:
        import os
        # Create directory if not exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        # Format: email:password:token:created_at
        account_line = f"{account_info['email']}:{account_info['password']}:{account_info['token']}:{account_info['created_at']}\n"
        # Append to done.txt file
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(account_line)
        log_success(f"Account saved to {output_file}")
        # Remove the email from accounts file
        accounts_file = CONFIG['FILES']['ACCOUNTS']
        with open(accounts_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(accounts_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if not line.strip().lower().startswith(account_info['email'].lower() + ':'):
                    f.write(line)
    except Exception as e:
        log_error("Error saving account", str(e))

def main_api(force_captcha_provider=None):
    """Main function for API-based registration, with optional forced captcha provider."""
    log_info(f"{'='*50}")
    log_info("UNICH API Registration System")
    log_info(f"{'='*50}")
    
    # Read already done emails
    done_emails = set()
    try:
        with open('data/done.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    parts = line.strip().split(':')
                    if parts:
                        done_emails.add(parts[0].strip().lower())
    except FileNotFoundError:
        pass
    
    # Read accounts from file
    accounts = []
    try:
        with open(CONFIG['FILES']['ACCOUNTS'], 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    email, password = line.strip().split(':', 1)
                    if email.strip().lower() not in done_emails:
                        accounts.append((email.strip(), password.strip()))
    except Exception as e:
        log_error("Error reading accounts file", str(e))
        return
    
    log_success(f"Loaded {len(accounts)} accounts (skipping {len(done_emails)} already done)")
    
    success_count = 0
    failed_count = 0
    
    for i, (email, password) in enumerate(accounts, 1):
        log_info(f"\n{'='*50}")
        log_progress(i, len(accounts), f"Processing account {i}/{len(accounts)}")
        log_info(f"{'='*50}")
        
        try:
            account_info = process_account_api(email, password, force_captcha_provider=force_captcha_provider)
            if account_info:
                save_account_info(account_info)
                success_count += 1
                log_success(f"Account {i} completed successfully!")
            else:
                failed_count += 1
                log_error(f"Account {i} failed")
        except KeyboardInterrupt:
            log_warning("\nProcess interrupted by user")
            break
        except Exception as e:
            log_error(f"Unexpected error for account {i}", str(e))
            failed_count += 1
            # Continue with next account instead of stopping
            continue
    
    # Final summary
    log_info(f"\n{'='*50}")
    log_info("Final Summary")
    log_info(f"{'='*50}")
    log_success(f"Successful: {success_count}")
    log_error(f"Failed: {failed_count}")
    log_info(f"Total: {len(accounts)}")
    log_info(f"{'='*50}")

if __name__ == "__main__":
    log_error("This module should be run from main.py")
    exit(1) 