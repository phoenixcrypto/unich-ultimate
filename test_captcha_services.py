#!/usr/bin/env python3
"""
Test script to verify all 3 captcha services are working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.api_interaction import get_2captcha_token, get_anticaptcha_token, get_capsolver_token
from config import CONFIG
from modules.utils import setup_logging, log_info, log_success, log_error, log_warning

def test_captcha_service(service_name, test_func, site_key, url, api_key):
    """Test a specific captcha service"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing {service_name.upper()} Service")
    print(f"{'='*60}")
    
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print(f"❌ {service_name}: API key not configured")
        return False
    
    try:
        print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
        print(f"🌐 Site Key: {site_key}")
        print(f"🔗 URL: {url}")
        print(f"⏳ Starting captcha solving...")
        
        # Test the service
        token = test_func(site_key, url, api_key)
        
        if token and len(token) > 100:  # Valid reCAPTCHA tokens are usually long
            print(f"✅ {service_name}: SUCCESS!")
            print(f"📝 Token length: {len(token)} characters")
            print(f"🔍 Token preview: {token[:50]}...")
            return True
        else:
            print(f"❌ {service_name}: Invalid token received")
            print(f"📝 Token: {token}")
            return False
            
    except Exception as e:
        print(f"❌ {service_name}: FAILED")
        print(f"🚨 Error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 CAPTCHA SERVICES TEST")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    # Test configuration
    cap = CONFIG['CAPTCHA']
    
    # UNICH reCAPTCHA details (example - you may need to update these)
    site_key = "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH"  # UNICH site key
    url = "https://unich.com"  # UNICH website
    
    print(f"🎯 Testing with UNICH reCAPTCHA:")
    print(f"   Site Key: {site_key}")
    print(f"   URL: {url}")
    
    results = {}
    
    # Test 2captcha
    results['2captcha'] = test_captcha_service(
        "2captcha",
        get_2captcha_token,
        site_key,
        url,
        cap.get('API_KEY_2CAPTCHA')
    )
    
    # Test Anticaptcha
    results['anticaptcha'] = test_captcha_service(
        "anticaptcha",
        get_anticaptcha_token,
        site_key,
        url,
        cap.get('API_KEY_ANTICAPTCHA')
    )
    
    # Test Capsolver
    results['capsolver'] = test_captcha_service(
        "capsolver",
        get_capsolver_token,
        site_key,
        url,
        cap.get('API_KEY_CAPSOLVER')
    )
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    
    working_services = []
    for service, result in results.items():
        status = "✅ WORKING" if result else "❌ FAILED"
        print(f"{service.upper():12} : {status}")
        if result:
            working_services.append(service)
    
    print(f"\n🎯 Working Services: {len(working_services)}/3")
    if working_services:
        print(f"✅ Available: {', '.join(working_services)}")
    else:
        print(f"❌ No working services found!")
        print(f"💡 Please check your API keys and configuration")
    
    return len(working_services) > 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1) 