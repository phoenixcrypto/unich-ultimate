#!/usr/bin/env python3
"""
Quick check script to verify captcha API keys and connectivity
"""

import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import CONFIG

def check_2captcha_balance(api_key):
    """Check 2captcha balance and API key validity"""
    try:
        response = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=getbalance&json=1')
        data = response.json()
        
        if data.get('status') == 1:
            balance = float(data.get('request', 0))
            return True, f"Balance: ${balance:.2f}"
        else:
            error = data.get('request', 'Unknown error')
            return False, f"Error: {error}"
    except Exception as e:
        return False, f"Connection error: {e}"

def check_anticaptcha_balance(api_key):
    """Check anticaptcha balance and API key validity"""
    try:
        response = requests.post('https://api.anti-captcha.com/getBalance', json={
            'clientKey': api_key
        })
        data = response.json()
        
        if data.get('errorId') == 0:
            balance = float(data.get('balance', 0))
            return True, f"Balance: ${balance:.2f}"
        else:
            error = data.get('errorDescription', 'Unknown error')
            return False, f"Error: {error}"
    except Exception as e:
        return False, f"Connection error: {e}"

def check_capsolver_balance(api_key):
    """Check capsolver balance and API key validity"""
    try:
        response = requests.post('https://api.capsolver.com/getBalance', json={
            'clientKey': api_key
        })
        data = response.json()
        
        if data.get('status') == 'ready':
            balance = float(data.get('balance', 0))
            return True, f"Balance: ${balance:.2f}"
        else:
            error = data.get('errorDescription', 'Unknown error')
            return False, f"Error: {error}"
    except Exception as e:
        return False, f"Connection error: {e}"

def main():
    """Main check function"""
    print("🔍 QUICK CAPTCHA API CHECK")
    print("=" * 50)
    
    cap = CONFIG['CAPTCHA']
    
    # Check 2captcha
    print(f"\n🧪 2CAPTCHA:")
    api_key = cap.get('API_KEY_2CAPTCHA')
    if api_key and api_key != "YOUR_API_KEY_HERE":
        print(f"   Key: {api_key[:10]}...{api_key[-4:]}")
        success, message = check_2captcha_balance(api_key)
        status = "✅" if success else "❌"
        print(f"   {status} {message}")
    else:
        print("   ❌ API key not configured")
    
    # Check Anticaptcha
    print(f"\n🧪 ANTICAPTCHA:")
    api_key = cap.get('API_KEY_ANTICAPTCHA')
    if api_key and api_key != "YOUR_API_KEY_HERE":
        print(f"   Key: {api_key[:10]}...{api_key[-4:]}")
        success, message = check_anticaptcha_balance(api_key)
        status = "✅" if success else "❌"
        print(f"   {status} {message}")
    else:
        print("   ❌ API key not configured")
    
    # Check Capsolver
    print(f"\n🧪 CAPSOLVER:")
    api_key = cap.get('API_KEY_CAPSOLVER')
    if api_key and api_key != "YOUR_API_KEY_HERE":
        print(f"   Key: {api_key[:10]}...{api_key[-4:]}")
        success, message = check_capsolver_balance(api_key)
        status = "✅" if success else "❌"
        print(f"   {status} {message}")
    else:
        print("   ❌ API key not configured")
    
    print(f"\n💡 To test actual captcha solving, run: python test_captcha_services.py")

if __name__ == "__main__":
    main() 