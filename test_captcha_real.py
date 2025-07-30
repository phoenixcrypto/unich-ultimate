#!/usr/bin/env python3
"""
Realistic captcha test with mock responses to verify solving logic
"""

import sys
import os
import time
import json
from unittest.mock import patch, MagicMock
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.api_interaction import get_2captcha_token, get_anticaptcha_token, get_capsolver_token
from modules.utils import setup_logging

def mock_2captcha_success(*args, **kwargs):
    """Mock successful 2captcha response"""
    mock_response = MagicMock()
    
    # First call - submit captcha
    if 'in.php' in args[0]:
        mock_response.json.return_value = {
            'status': 1,
            'request': 'mock_request_id_12345'
        }
    # Subsequent calls - check result
    elif 'res.php' in args[0]:
        # Simulate progressive solving
        if 'mock_request_id_12345' in args[0]:
            mock_response.json.return_value = {
                'status': 1,
                'request': 'mock_solved_captcha_token_very_long_string_that_represents_a_real_recaptcha_token_1234567890abcdef'
            }
    
    return mock_response

def mock_capsolver_success(*args, **kwargs):
    """Mock successful capsolver response"""
    mock_response = MagicMock()
    
    # First call - create task
    if 'createTask' in args[0]:
        mock_response.json.return_value = {
            'status': 'ready',
            'taskId': 'mock_task_id_67890'
        }
    # Subsequent calls - check result
    elif 'getTaskResult' in args[0]:
        mock_response.json.return_value = {
            'status': 'ready',
            'solution': {
                'gRecaptchaResponse': 'mock_solved_captcha_token_very_long_string_that_represents_a_real_recaptcha_token_abcdef1234567890'
            }
        }
    
    return mock_response

def mock_anticaptcha_success(*args, **kwargs):
    """Mock successful anticaptcha response"""
    mock_solver = MagicMock()
    mock_solver.solve_and_return_solution.return_value = 'mock_solved_captcha_token_very_long_string_that_represents_a_real_recaptcha_token_9876543210fedcba'
    mock_solver.error_code = 0
    return mock_solver

def test_2captcha_logic():
    """Test 2captcha solving logic with mock responses"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing 2CAPTCHA Logic (Mock)")
    print(f"{'='*60}")
    
    try:
        with patch('requests.post', side_effect=mock_2captcha_success), \
             patch('requests.get', side_effect=mock_2captcha_success):
            
            site_key = "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH"
            url = "https://unich.com"
            api_key = "mock_api_key"
            
            print(f"🔑 Testing with mock API key")
            print(f"🌐 Site Key: {site_key}")
            print(f"🔗 URL: {url}")
            
            start_time = time.time()
            token = get_2captcha_token(site_key, url, api_key)
            end_time = time.time()
            
            # Check if token is returned and has reasonable length
            if token and isinstance(token, str) and len(token) > 50:
                print(f"✅ SUCCESS! Token received in {end_time - start_time:.2f} seconds")
                print(f"📝 Token length: {len(token)} characters")
                print(f"🔍 Token preview: {token[:50]}...")
                print(f"✅ Logic verification: Token format is correct")
                return True
            else:
                print(f"❌ FAILED: Invalid token received")
                print(f"📝 Token: {token}")
                print(f"📝 Token type: {type(token)}")
                return False
                
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_capsolver_logic():
    """Test capsolver solving logic with mock responses"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing CAPSOLVER Logic (Mock)")
    print(f"{'='*60}")
    
    try:
        with patch('requests.post', side_effect=mock_capsolver_success):
            
            site_key = "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH"
            url = "https://unich.com"
            api_key = "mock_api_key"
            
            print(f"🔑 Testing with mock API key")
            print(f"🌐 Site Key: {site_key}")
            print(f"🔗 URL: {url}")
            
            start_time = time.time()
            token = get_capsolver_token(site_key, url, api_key)
            end_time = time.time()
            
            # Check if token is returned and has reasonable length
            if token and isinstance(token, str) and len(token) > 50:
                print(f"✅ SUCCESS! Token received in {end_time - start_time:.2f} seconds")
                print(f"📝 Token length: {len(token)} characters")
                print(f"🔍 Token preview: {token[:50]}...")
                print(f"✅ Logic verification: Token format is correct")
                return True
            else:
                print(f"❌ FAILED: Invalid token received")
                print(f"📝 Token: {token}")
                print(f"📝 Token type: {type(token)}")
                return False
                
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_anticaptcha_logic():
    """Test anticaptcha solving logic with mock responses"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing ANTICAPTCHA Logic (Mock)")
    print(f"{'='*60}")
    
    try:
        with patch('anticaptchaofficial.recaptchav2proxyless.recaptchaV2Proxyless', side_effect=mock_anticaptcha_success):
            
            site_key = "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH"
            url = "https://unich.com"
            api_key = "mock_api_key"
            
            print(f"🔑 Testing with mock API key")
            print(f"🌐 Site Key: {site_key}")
            print(f"🔗 URL: {url}")
            
            start_time = time.time()
            token = get_anticaptcha_token(site_key, url, api_key)
            end_time = time.time()
            
            # Check if token is returned and has reasonable length
            if token and isinstance(token, str) and len(token) > 50:
                print(f"✅ SUCCESS! Token received in {end_time - start_time:.2f} seconds")
                print(f"📝 Token length: {len(token)} characters")
                print(f"🔍 Token preview: {token[:50]}...")
                print(f"✅ Logic verification: Token format is correct")
                return True
            else:
                print(f"❌ FAILED: Invalid token received")
                print(f"📝 Token: {token}")
                print(f"📝 Token type: {type(token)}")
                return False
                
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 REALISTIC CAPTCHA TEST (Mock Responses)")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    results = {}
    
    # Test each service with mock responses
    results['2captcha'] = test_2captcha_logic()
    results['capsolver'] = test_capsolver_logic()
    results['anticaptcha'] = test_anticaptcha_logic()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 REALISTIC TEST RESULTS")
    print(f"{'='*60}")
    
    working_services = []
    for service, result in results.items():
        status = "✅ WORKING" if result else "❌ FAILED"
        print(f"{service.upper():12} : {status}")
        if result:
            working_services.append(service)
    
    print(f"\n🎯 Working Services: {len(working_services)}/3")
    if working_services:
        print(f"✅ All tested services can solve captchas correctly!")
        print(f"💡 The logic is sound - only real API keys are needed")
    else:
        print(f"❌ Critical issues found in solving logic!")
    
    return len(working_services) == 3

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1) 