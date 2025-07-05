import json
import os
import time
import random
from colorama import Fore, init
from modules.api_interaction import UnichAPI

init(autoreset=True)

ACCOUNTS_FILE = 'data/done.txt'
LOG_FILE = 'logs/mining_api.log'

ACCEPT_LANGUAGES = [
    'en-US,en;q=0.9',
    'ar-EG,ar;q=0.9,en;q=0.8',
    'fr-FR,fr;q=0.9,en;q=0.8',
    'de-DE,de;q=0.9,en;q=0.8',
    'es-ES,es;q=0.9,en;q=0.8',
    'ru-RU,ru;q=0.9,en;q=0.8',
    'zh-CN,zh;q=0.9,en;q=0.8',
    'tr-TR,tr;q=0.9,en;q=0.8',
    'it-IT,it;q=0.9,en;q=0.8',
    'pt-BR,pt;q=0.9,en;q=0.8'
]
SEC_CH_UA_LIST = [
    '"Chromium";v="124", "Google Chrome";v="124", ";Not A Brand";v="99"',
    '"Google Chrome";v="124", "Chromium";v="124", ";Not A Brand";v="99"',
    '"Microsoft Edge";v="124", "Chromium";v="124", ";Not A Brand";v="99"',
    '"Firefox";v="125", ";Not A Brand";v="99"',
    '"Safari";v="17", ";Not A Brand";v="99"'
]
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
]

def log_to_file(message):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def pick_random(arr):
    return random.choice(arr)

def start_mining_all_accounts():
    print(f"{Fore.CYAN}⛏️ Starting mining for all accounts...")
    log_to_file(f"[START] Mining for all accounts")
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"{Fore.RED}❌ Accounts file not found: {ACCOUNTS_FILE}")
        return
    accounts = []
    with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(':')
                if len(parts) >= 4:
                    accounts.append({
                        'email': parts[0],
                        'password': parts[1], 
                        'token': parts[2],
                        'created_at': parts[3]
                    })
    already_active = 0
    activated = 0
    failed = 0
    for acc in accounts:
        email = acc.get('email')
        token = acc.get('token')
        if not token:
            msg = f"[FAILED] {email} | No token found"
            print(f"{Fore.RED}✖️ Failed: {email} (No token)")
            log_to_file(msg)
            failed += 1
            continue
        headers = {
            'User-Agent': pick_random(USER_AGENTS),
            'Accept-Language': pick_random(ACCEPT_LANGUAGES),
            'sec-ch-ua': pick_random(SEC_CH_UA_LIST),
            'Origin': 'https://unich.com',
            'Referer': 'https://unich.com/en/airdrop/sign-up',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {token}'
        }
        api = UnichAPI()
        api.session.headers.update(headers)
        try:
            # Check mining status
            info_res = api.session.get(f"{api.base_url}/airdrop/user/v1/info/my-info", headers=headers)
            info_data = info_res.json()
            if not isinstance(info_data, dict) or 'data' not in info_data or not isinstance(info_data['data'], dict) or 'mining' not in info_data['data']:
                msg = f"[FAILED] {email} | Unexpected API response: {info_data}"
                print(f"{Fore.RED}✖️ Failed: {email} (Unexpected API response)")
                print(f"{Fore.YELLOW}API response: {info_data}")
                log_to_file(msg)
                failed += 1
                continue
            mining = info_data['data']['mining']
            if mining.get('started'):
                msg = f"[ALREADY ACTIVE] {email}"
                print(f"{Fore.BLUE}⏳ Already active: {email}")
                log_to_file(msg)
                already_active += 1
                continue
            # Start mining
            res = api.session.post(f"{api.base_url}/airdrop/user/v1/mining/start", headers=headers)
            res_data = res.json()
            if res_data.get('code') == 'OK':
                msg = f"[ACTIVATED] {email}"
                print(f"{Fore.GREEN}✔️ Activated: {email}")
                log_to_file(msg)
                activated += 1
            else:
                msg = f"[NOT ACTIVATED] {email} | {res_data}"
                print(f"{Fore.YELLOW}⚠️ Not activated: {email}")
                log_to_file(msg)
                failed += 1
        except Exception as err:
            msg = f"[FAILED] {email} | {str(err)}"
            print(f"{Fore.RED}✖️ Failed: {email}\n{err}")
            log_to_file(msg)
            failed += 1
        time.sleep(2)  # Small delay between accounts
    summary = f"[SUMMARY] Already active: {already_active}, Activated: {activated}, Failed: {failed}, Total: {len(accounts)}"
    print(f"{Fore.CYAN}\n📋 Mining Summary:")
    print(f"{Fore.BLUE}⏳ Already active: {already_active}")
    print(f"{Fore.GREEN}✔️ Activated: {activated}")
    print(f"{Fore.RED}✖️ Failed: {failed}")
    print(f"{Fore.MAGENTA}📧 Total accounts: {len(accounts)}")
    log_to_file(summary) 