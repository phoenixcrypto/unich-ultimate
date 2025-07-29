import time
import random
import sys
import logging
from datetime import datetime
from colorama import Fore

# Setup logging
def setup_logging(log_file="logs/app.log"):
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    import os
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def get_random_user_agent():
    """
    إرجاع user agent عشوائي من قائمة ثابتة (بدون fake_useragent)
    """
    common_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    return random.choice(common_agents)

def random_delay(min_seconds=5, max_seconds=15):
    """
    إضافة تأخير عشوائي بين العمليات مع عد تنازلي
    """
    if min_seconds > max_seconds:
        min_seconds, max_seconds = max_seconds, min_seconds
    delay = random.uniform(min_seconds, max_seconds)
    try:
        for remaining in range(int(delay), 0, -1):
            sys.stdout.write(f"\r[⏱️] Sleeping for {delay:.2f} seconds. Time left: {remaining:3d} seconds ")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r" + " "*60 + "\r")
        if delay - int(delay) > 0:
            time.sleep(delay - int(delay))
    except KeyboardInterrupt:
        sys.stdout.write("\r" + " "*60 + "\r")
        print(f"\n{Fore.YELLOW}⚠️ Delay interrupted by user")
        logger.warning("Delay interrupted by user")
        raise

def log_success(message):
    """Log success message with color"""
    print(f"{Fore.GREEN}✅ {message}")
    logger.info(f"SUCCESS: {message}")

def log_error(message, error=None):
    """Log error message with color and details"""
    print(f"{Fore.RED}❌ {message}")
    if error:
        print(f"{Fore.YELLOW}Details: {error}")
        logger.error(f"ERROR: {message} - {error}")
    else:
        logger.error(f"ERROR: {message}")

def log_warning(message):
    """Log warning message with color"""
    print(f"{Fore.YELLOW}⚠️ {message}")
    logger.warning(f"WARNING: {message}")

def log_info(message):
    """Log info message with color"""
    print(f"{Fore.BLUE}ℹ️ {message}")
    logger.info(f"INFO: {message}")

def log_progress(current, total, message=""):
    """Log progress with percentage"""
    percentage = (current / total) * 100
    progress_bar = "█" * int(percentage / 2) + "░" * (50 - int(percentage / 2))
    print(f"\r{Fore.CYAN}📊 Progress: [{progress_bar}] {percentage:.1f}% ({current}/{total}) {message}", end="")
    if current == total:
        print()  # New line when complete