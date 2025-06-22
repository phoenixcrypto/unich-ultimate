import requests
import json
import time
import random
import logging
from datetime import datetime, timedelta
from colorama import Fore, Style, init
from modules.utils import random_delay, create_chrome_options
from config import CONFIG
import imaplib
import email
import re
from bs4 import BeautifulSoup
import threading

init(autoreset=True)

# Expanded and updated lists for better anonymity
USER_AGENTS = [
    # Chrome on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    # Chrome on macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    # Firefox on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    # Firefox on macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
    # Edge on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.2592.87',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.2535.92'
]

ACCEPT_LANGUAGES = [
    'en-US,en;q=0.9', 'en-GB,en;q=0.8', 'fr-FR,fr;q=0.9', 'de-DE,de;q=0.9',
    'es-ES,es;q=0.9', 'it-IT,it;q=0.9', 'nl-NL,nl;q=0.8', 'ja-JP,ja;q=0.7',
    'ar-SA,ar;q=0.9', 'ru-RU,ru;q=0.8', 'pt-BR,pt;q=0.9'
]

SEC_CH_UA_LIST = [
    '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    '"Not/A)Brand";v="8", "Chromium";v="125", "Google Chrome";v="125"',
    '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"'
]

class UnichAPI:
    def __init__(self):
        self.base_url = "https://api.unich.com"
        self.session = requests.Session()
        # Each instance gets a unique, consistent set of headers
        self.unique_headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept-Language': random.choice(ACCEPT_LANGUAGES),
            'sec-ch-ua': random.choice(SEC_CH_UA_LIST)
        }
        self.setup_session()
        
    def setup_session(self):
        """Setup session with a unique and consistent header set for the instance."""
        base_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://unich.com',
            'Referer': 'https://unich.com/en/airdrop/sign-up',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }
        # Combine base headers with the unique headers for this session
        self.session.headers.update(base_headers)
        self.session.headers.update(self.unique_headers)
    
    def get_random_headers(self):
        """DEPRECATED: This method is no longer needed as headers are set per-session."""
        # This function is kept for compatibility in case it's called somewhere else,
        # but it now just returns the session's headers.
        return self.session.headers
    
    def solve_captcha(self, url="https://unich.com/en/airdrop/sign-up"):
        """Solve GeeTest V4 captcha using 2Captcha"""
        try:
            print(f"{Fore.YELLOW}🔍 Solving captcha...")
            
            # Check if captcha API key is provided
            api_key = CONFIG.get('CAPTCHA', {}).get('API_KEY', '')
            if not api_key:
                print(f"{Fore.YELLOW}⚠️ No 2Captcha API key provided. Skipping captcha for testing...")
                # Return dummy captcha solution for testing
                return {
                    'lot_number': 'test_lot_number',
                    'captcha_output': 'test_captcha_output',
                    'pass_token': 'test_pass_token',
                    'gen_time': str(int(time.time()))
                }
            
            # Get captcha values from geetest
            callback = 'geetest_' + str(int(time.time() * 1000))
            captcha_id = 'e7baa772ac1ae5dceccd7273ad5f57bd'
            load_url = f"https://gcaptcha4.geetest.com/load?callback={callback}&captcha_id={captcha_id}&client_type=web&pt=1&lang=eng"
            
            load_res = requests.get(load_url, headers={
                'Referer': url,
                'User-Agent': self.session.headers['User-Agent']
            })
            
            # Extract JSON from JSONP response - improved parsing
            jsonp = load_res.text
            try:
                # Try to find the JSON part more accurately
                start_idx = jsonp.find('(')
                end_idx = jsonp.rfind(')')
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    json_str = jsonp[start_idx + 1:end_idx]
                else:
                    # Fallback: try to remove callback name
                    json_str = jsonp.replace(f'{callback}(', '').replace(');', '')
                
                data = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"{Fore.RED}❌ JSON parsing error: {str(e)}")
                print(f"{Fore.YELLOW}🔍 Raw response: {jsonp[:200]}...")
                raise Exception("Failed to parse GeeTest response")
            
            if not data.get('data') or not data['data'].get('lot_number'):
                raise Exception("Failed to get captcha values")
            
            # Prepare 2Captcha payload
            payload = {
                "clientKey": api_key,
                "task": {
                    "type": "GeeTestTaskProxyless",
                    "websiteURL": url,
                    "version": 4,
                    "initParameters": {
                        "captcha_id": captcha_id,
                        "lot_number": data['data']['lot_number'],
                        "process_token": data['data']['process_token']
                    }
                }
            }
            
            # Submit to 2Captcha
            submit_res = requests.post('https://api.2captcha.com/createTask', json=payload)
            submit_data = submit_res.json()
            
            if submit_data.get('errorId') != 0:
                raise Exception(f"2Captcha error: {submit_data.get('errorDescription')}")
            
            task_id = submit_data['taskId']
            print(f"{Fore.BLUE}⏳ Waiting for captcha solution...")
            
            # Poll for solution
            for i in range(24):  # Max 2 minutes
                time.sleep(5)
                result_res = requests.post('https://api.2captcha.com/getTaskResult', json={
                    "clientKey": api_key,
                    "taskId": task_id
                })
                result_data = result_res.json()
                
                if result_data.get('status') == 'ready':
                    solution = result_data.get('solution', {})
                    print(f"{Fore.GREEN}✅ Captcha solved successfully!")
                    return solution
                elif result_data.get('status') == 'failed':
                    raise Exception(f"2Captcha failed: {result_data.get('errorDescription')}")
            
            raise Exception("Captcha solving timed out")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Captcha solving failed: {str(e)}")
            raise
    
    def read_otp_from_gmail(self, target_email):
        """Read OTP code from Gmail automatically (robust, like automation.py)"""
        try:
            print(f"{Fore.BLUE}📧 Reading OTP from Gmail...")
            mail = imaplib.IMAP4_SSL(CONFIG['EMAIL']['IMAP_HOST'], CONFIG['EMAIL']['IMAP_PORT'])
            mail.login(CONFIG['EMAIL']['IMAP_EMAIL'], CONFIG['EMAIL']['IMAP_PASSWORD'])
            mail.select('inbox')

            # ابحث في آخر 10 دقائق
            search_date = (datetime.now() - timedelta(minutes=10)).strftime("%d-%b-%Y")

            # جرب البحث من noreply@unich.com أولاً
            search_criteria = f'(FROM "noreply@unich.com" TO "{target_email}" SINCE "{search_date}")'
            status, email_ids_raw = mail.search(None, search_criteria)

            # إذا لم تجد نتائج، جرب البحث الأوسع
            if status != 'OK' or not email_ids_raw or not email_ids_raw[0]:
                print(f"🔍 Searching for emails to {target_email} from the last 10 minutes (broader search)...")
                search_criteria = f'(TO "{target_email}" SINCE "{search_date}")'
                status, email_ids_raw = mail.search(None, search_criteria)
                if status != 'OK' or not email_ids_raw or not email_ids_raw[0]:
                    raise Exception("No emails found for this address in the last 10 minutes")

            email_id_list = email_ids_raw[0].split()
            if not email_id_list:
                raise Exception("No email IDs found.")

            # جلب أحدث رسالة
            latest_email_id = email_id_list[-1]
            status, msg_data = mail.fetch(latest_email_id, '(RFC822)')

            # دعم كل حالات البيانات
            if status != 'OK' or not msg_data or not msg_data[0]:
                raise Exception("Failed to fetch email data or invalid email data format.")
            raw_email = msg_data[0][1] if isinstance(msg_data[0], tuple) else msg_data[0]
            if isinstance(raw_email, str):
                raw_email_bytes = raw_email.encode('utf-8')
            else:
                raw_email_bytes = raw_email
            msg = email.message_from_bytes(raw_email_bytes)

            otp_code = None
            # أولوية للـ HTML
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
            # إذا لم يجد في HTML جرب النص العادي
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
            print(f"{Fore.GREEN}✅ OTP found: {otp_code}")
            return otp_code
        except Exception as e:
            print(f"{Fore.RED}❌ Error reading OTP from Gmail: {str(e)}")
            raise
    
    def request_otp(self, email):
        """Request OTP code"""
        try:
            print(f"{Fore.BLUE}📤 Requesting OTP for {email}...")
            
            # Solve captcha first
            captcha_solution = self.solve_captcha()
            
            # Prepare OTP request payload
            payload = {
                "action": "REGISTER",
                "email": email,
                "lot_number": captcha_solution.get('lot_number'),
                "captcha_output": captcha_solution.get('captcha_output'),
                "pass_token": captcha_solution.get('pass_token'),
                "gen_time": captcha_solution.get('gen_time')
            }
            
            # Send request using the consistent session headers
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/auth/otp/request",
                json=payload,
            )
            
            if response.status_code in [200, 201]:  # Accept both 200 and 201 as success
                data = response.json()
                print(f"{Fore.BLUE}📡 Response: {data}")
                
                # Check if OTP was sent successfully
                if data.get('code') == 'OK':
                    otp_sent = data.get('data', {}).get('otpSent')
                    print(f"{Fore.BLUE}🔍 OTP sent value: {otp_sent} (type: {type(otp_sent)})")
                    
                    if otp_sent == True:
                        print(f"{Fore.GREEN}✅ OTP request sent successfully!")
                        return True
                    else:
                        raise Exception(f"OTP not sent: {data}")
                else:
                    raise Exception(f"API error: {data}")
            else:
                raise Exception(f"HTTP error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ OTP request failed: {str(e)}")
            raise
    
    def verify_otp(self, email, otp):
        """Verify OTP code"""
        try:
            print(f"{Fore.BLUE}🔐 Verifying OTP...")
            
            # Solve captcha again
            captcha_solution = self.solve_captcha()
            
            # Prepare verification payload
            payload = {
                "email": email,
                "otp": otp,
                "lot_number": captcha_solution.get('lot_number'),
                "captcha_output": captcha_solution.get('captcha_output'),
                "pass_token": captcha_solution.get('pass_token'),
                "gen_time": captcha_solution.get('gen_time')
            }
            
            # Send request using the consistent session headers
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/auth/otp/resolve",
                json=payload,
            )
            
            if response.status_code in [200, 201]:  # Accept both 200 and 201 as success
                data = response.json()
                print(f"{Fore.BLUE}📡 OTP verification response: {data}")
                
                if data.get('code') == 'OK':
                    otp_token = data.get('data', {}).get('otpToken')
                    if otp_token:
                        print(f"{Fore.GREEN}✅ OTP verified successfully!")
                        return otp_token
                    else:
                        raise Exception(f"No OTP token received: {data}")
                else:
                    raise Exception(f"OTP verification failed: {data.get('message')}")
            else:
                raise Exception(f"OTP verification failed: {response.text}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ OTP verification failed: {str(e)}")
            raise
    
    def sign_up(self, email, password, otp_token):
        """Complete account registration"""
        try:
            print(f"{Fore.BLUE}📝 Completing registration...")
            
            # Solve captcha again
            captcha_solution = self.solve_captcha()
            
            # Prepare signup payload
            payload = {
                "email": email,
                "password": password,
                "otpToken": otp_token,
                "lot_number": captcha_solution.get('lot_number'),
                "captcha_output": captcha_solution.get('captcha_output'),
                "pass_token": captcha_solution.get('pass_token'),
                "gen_time": captcha_solution.get('gen_time')
            }
            
            # Send request using the consistent session headers
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/auth/sign-up",
                json=payload,
            )
            
            if response.status_code in [200, 201]:  # Accept both 200 and 201 as success
                data = response.json()
                if data.get('code') == 'OK':
                    access_token = data.get('data', {}).get('accessToken')
                    if access_token:
                        print(f"{Fore.GREEN}✅ Account registered successfully!")
                        return access_token
                    else:
                        raise Exception("No access token received")
                else:
                    raise Exception(f"Registration failed: {data.get('message')}")
            else:
                raise Exception(f"Registration failed: {response.text}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Registration failed: {str(e)}")
            raise
    
    def apply_referral(self, access_token, referral_code):
        """Apply referral code to account"""
        try:
            print(f"{Fore.BLUE}🎯 Applying referral code...")
            
            # Prepare referral payload
            payload = {"code": referral_code}
            
            # Use the consistent session headers and just add Authorization
            headers = self.session.headers.copy()
            headers['Authorization'] = f"Bearer {access_token}"
            
            # Send request
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/ref/refer-sign-up",
                json=payload,
                headers=headers
            )
            print(f"{Fore.BLUE}📡 Referral Response Status: {response.status_code}")
            try:
                print(f"{Fore.BLUE}📡 Referral Response Body: {response.json()}")
            except json.JSONDecodeError:
                print(f"{Fore.BLUE}📡 Referral Response Body (non-JSON): {response.text}")
            
            if response.status_code in [200, 201]:  # Accept both 200 and 201 as success
                data = response.json()
                if data.get('code') == 'OK':
                    print(f"{Fore.GREEN}✅ Referral code applied successfully!")
                    return True
                else:
                    raise Exception(f"Referral application failed: {data.get('message')}")
            else:
                raise Exception(f"Referral application failed: {response.text}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Referral application failed: {str(e)}")
            raise
    
    def start_mining(self, access_token):
        """Start mining for account"""
        try:
            print(f"{Fore.BLUE}⛏️ Starting mining...")
            
            # Use the consistent session headers and just add Authorization
            headers = self.session.headers.copy()
            headers['Authorization'] = f"Bearer {access_token}"
            
            # Send request
            response = self.session.post(
                f"{self.base_url}/airdrop/user/v1/mine/request",
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get('code') == 'OK':
                    print(f"{Fore.GREEN}✅ Mining started successfully!")
                    return True
                else:
                    raise Exception(f"Mining start failed: {data.get('message')}")
            else:
                raise Exception(f"Mining start failed: {response.text}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Mining start failed: {str(e)}")
            raise

def process_account_api(email, password, retry_count=0):
    """Process a single account using API"""
    api = UnichAPI()
    
    try:
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}🔄 Processing account: {email}")
        print(f"{Fore.CYAN}{'='*50}")
        
        # Step 1: Request OTP
        if not api.request_otp(email):
            raise Exception("Failed to request OTP")
        
        # Add longer delay to avoid OTP blocking
        print(f"{Fore.BLUE}⏳ Waiting to avoid OTP blocking...")
        time.sleep(30)  # Wait 30 seconds to avoid blocking
        
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])
        
        # Step 2: Read OTP from Gmail
        otp_code = api.read_otp_from_gmail(email)
        
        # Add delay after reading OTP
        print(f"{Fore.BLUE}⏳ Waiting after OTP reading...")
        time.sleep(15)  # Wait 15 seconds after reading OTP
        
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])
        
        # Step 3: Verify OTP
        otp_token = api.verify_otp(email, otp_code)
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])
        
        # Step 4: Complete registration
        access_token = api.sign_up(email, password, otp_token)
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])
        
        # Step 5: Apply referral code
        api.apply_referral(access_token, CONFIG['REFERRAL_CODE'])
        random_delay(CONFIG['DELAYS']['AFTER_ACTION'], CONFIG['DELAYS']['AFTER_ACTION'])
        
        print(f"{Fore.MAGENTA}✅ All steps completed, preparing to save account info...")
        
        # Save account info
        account_info = {
            "email": email,
            "password": password,
            "token": access_token,
            "created_at": datetime.now().isoformat()
        }
        
        return account_info
        
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}⚠️ Process interrupted by user")
        raise
    except Exception as e:
        print(f"{Fore.RED}❌ Error processing account {email}: {str(e)}")
        logging.error(f"Error processing account {email}: {str(e)}")
        
        # Special handling for OTP blocking
        if "OTP_BLOCK_BETWEEN_2_TIMES" in str(e):
            print(f"{Fore.YELLOW}⚠️ OTP blocked, waiting longer before retry...")
            time.sleep(60)  # Wait 1 minute for OTP block to clear
        
        if retry_count < CONFIG['SECURITY']['MAX_RETRIES']:
            print(f"{Fore.YELLOW}🔄 Retrying... (Attempt {retry_count + 1}/{CONFIG['SECURITY']['MAX_RETRIES']})")
            random_delay(CONFIG['DELAYS']['BETWEEN_ACCOUNTS'], CONFIG['DELAYS']['BETWEEN_ACCOUNTS'])
            return process_account_api(email, password, retry_count + 1)
        else:
            print(f"{Fore.RED}❌ Max retries reached for account {email}")
            return None
    finally:
        try:
            random_delay(CONFIG['DELAYS']['BETWEEN_ACCOUNTS'], CONFIG['DELAYS']['BETWEEN_ACCOUNTS'])
        except KeyboardInterrupt:
            pass

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
        print(f"{Fore.GREEN}✅ Account saved to {output_file}")
        # Remove the email from accounts file
        accounts_file = CONFIG['FILES']['ACCOUNTS']
        with open(accounts_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(accounts_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if not line.strip().lower().startswith(account_info['email'].lower() + ':'):
                    f.write(line)
    except Exception as e:
        print(f"{Fore.RED}❌ Error saving account: {str(e)}")

def main_api():
    """Main function for API-based registration"""
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}🚀 UNICH API Registration System")
    print(f"{Fore.CYAN}{'='*50}")
    
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
        print(f"{Fore.RED}❌ Error reading accounts file: {str(e)}")
        return
    
    print(f"{Fore.GREEN}📧 Loaded {len(accounts)} accounts (skipping {len(done_emails)} already done)")
    
    # Check if captcha API key is provided
    api_key = CONFIG.get('CAPTCHA', {}).get('API_KEY', '')
    if not api_key:
        print(f"{Fore.YELLOW}⚠️ Warning: No 2Captcha API key provided!")
        print(f"{Fore.YELLOW}   The system will use dummy captcha values for testing.")
        print(f"{Fore.YELLOW}   Add your 2Captcha API key in config.py for full functionality.")
        print()
    
    success_count = 0
    failed_count = 0
    
    for i, (email, password) in enumerate(accounts, 1):
        print(f"{Fore.CYAN}\n{'='*50}")
        print(f"{Fore.CYAN}📊 Progress: {i}/{len(accounts)}")
        print(f"{Fore.CYAN}{'='*50}")
        
        try:
            account_info = process_account_api(email, password)
            if account_info:
                save_account_info(account_info)
                success_count += 1
                print(f"{Fore.GREEN}🎉 Account {i} completed successfully!")
            else:
                failed_count += 1
                print(f"{Fore.RED}❌ Account {i} failed")
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\n⚠️ Process interrupted by user")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error for account {i}: {str(e)}")
            failed_count += 1
            # Continue with next account instead of stopping
            continue
    
    # Final summary
    print(f"{Fore.CYAN}\n{'='*50}")
    print(f"{Fore.CYAN}📋 Final Summary")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.GREEN}✅ Successful: {success_count}")
    print(f"{Fore.RED}❌ Failed: {failed_count}")
    print(f"{Fore.BLUE}📧 Total: {len(accounts)}")
    print(f"{Fore.CYAN}{'='*50}")

if __name__ == "__main__":
    print(f"{Fore.RED}❌ This module should be run from main.py")
    exit(1) 