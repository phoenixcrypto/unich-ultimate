import time
import random
from fake_useragent import UserAgent
from colorama import Fore

def get_random_user_agent():
    """
    Generate a random user agent string using fake_useragent library
    """
    try:
        ua = UserAgent()
        return ua.random
    except Exception as e:
        print(f"⚠️ Error generating random user agent: {str(e)}")
        # Fallback to a list of common user agents if fake_useragent fails
        common_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        return random.choice(common_agents)

def random_delay(min_seconds=5, max_seconds=15):
    """
    Add a random delay between actions to avoid detection, with a visible countdown
    """
    import sys
    delay = random.uniform(min_seconds, max_seconds)
    try:
    for remaining in range(int(delay), 0, -1):
        sys.stdout.write(f"\r[⏱️] Sleeping for {delay:.2f} seconds. Time left: {remaining:3d} seconds ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " "*60 + "\r")
    # For any remaining fraction of a second
    if delay - int(delay) > 0:
        time.sleep(delay - int(delay))
    except KeyboardInterrupt:
        sys.stdout.write("\r" + " "*60 + "\r")
        print(f"\n{Fore.YELLOW}⚠️ Delay interrupted by user")
        raise

def create_chrome_options():
    """
    Create Chrome options with random user agent and other anti-detection settings, and spoof JS properties
    """
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument(f"user-agent={get_random_user_agent()}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    # تعطيل Google Password Manager (غير مدعوم في undetected_chromedriver)
    # options.add_experimental_option("prefs", {
    #     "credentials_enable_service": False,
    #     "profile.password_manager_enabled": False
    # })
    # WebRTC leak prevention
    options.add_argument("--disable-webrtc")
    # JS spoofing script (to be injected after driver creation)
    options.js_spoof_script = '''
        Object.defineProperty(navigator, 'platform', {get: () => ['Win32','Linux x86_64','MacIntel'][Math.floor(Math.random()*3)]});
        Object.defineProperty(navigator, 'deviceMemory', {get: () => [4, 8, 16][Math.floor(Math.random()*3)]});
        Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => [2, 4, 8][Math.floor(Math.random()*3)]});
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            // Spoof WebGL vendor
            if (parameter === 37445) return 'NVIDIA Corporation';
            if (parameter === 37446) return 'NVIDIA GeForce GTX 1050/PCIe/SSE2';
            return getParameter.call(this, parameter);
        };
        // Disable WebRTC leaks
        if (window.RTCPeerConnection) {
            window.RTCPeerConnection = undefined;
        }
    '''
    return options 