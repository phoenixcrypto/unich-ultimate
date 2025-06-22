from colorama import Fore, Style, init
import sys
init(autoreset=True)

# استيراد دوال التوليد والأتمتة
from modules.gmail_dot_generator import save_gmail_variants_to_accounts
import importlib

def print_menu():
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50)
    print(Fore.CYAN + Style.BRIGHT + "🤖 UNICH Project Automation by PhoenixCrypto_PC 🤖".center(50, "-"))
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print(Fore.WHITE + Style.BRIGHT + "\n" + "🔥 Features:")
    print(Fore.GREEN + Style.BRIGHT + "  • Generate unlimited Gmail dot trick emails")
    print(Fore.GREEN + Style.BRIGHT + "  • Fully automated referral registration for Unich")
    print(Fore.GREEN + Style.BRIGHT + "  • Direct API interaction (Fast & Automated)")
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print(Fore.YELLOW + Style.BRIGHT + "1. ✉️  Generate Gmail Dot Trick Emails")
    print(Fore.YELLOW + Style.BRIGHT + "2. 🚀 Run Referral Automation (Browser)")
    print(Fore.YELLOW + Style.BRIGHT + "3. 🔌 Run API Direct Registration (Fast + 2Captcha)")
    print(Fore.YELLOW + Style.BRIGHT + "4. ⛏️  Start Mining for All Accounts (API)")
    print(Fore.RED + Style.BRIGHT + "0. ❌ Exit")
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print()
    print(Fore.MAGENTA + Style.BRIGHT + "📢 Telegram Channel: " +
          Fore.WHITE + Style.BRIGHT + "@PhoenixCrypto_PC")
    print(Fore.BLUE + Style.BRIGHT + "🔗 https://t.me/PhoenixCrypto_PC")
    print()

def run_automation():
    print(Fore.GREEN + Style.BRIGHT + "\n🚀 Starting referral automation...\n")
    # استيراد دالة main من ملف الأتمتة
    automation = importlib.import_module("modules.automation")
    automation.main()

def run_api_automation():
    print(Fore.GREEN + Style.BRIGHT + "\n🔌 Starting API direct registration...\n")
    # استيراد دالة main_api من وحدة API
    from modules.api_interaction import main_api
    main_api()

def main():
    while True:
        print_menu()
        choice = input(Fore.MAGENTA + Style.BRIGHT + "\n👉 Enter your choice: ").strip()
        if choice == "1":
            print(Fore.BLUE + Style.BRIGHT + "\n[Dot Trick Email Generator]")
            base = input(Fore.YELLOW + Style.BRIGHT + "\n✉️  Enter Gmail username (before @): ").strip()
            while not base:
                print(Fore.RED + Style.BRIGHT + "❌ Username cannot be empty. Please try again.")
                base = input(Fore.YELLOW + Style.BRIGHT + "✉️  Enter Gmail username (before @): ").strip()
            password = input(Fore.YELLOW + Style.BRIGHT + "🔑 Enter password for all emails: ").strip()
            while not password:
                print(Fore.RED + Style.BRIGHT + "❌ Password cannot be empty. Please try again.")
                password = input(Fore.YELLOW + Style.BRIGHT + "🔑 Enter password for all emails: ").strip()
            save_gmail_variants_to_accounts(base, password)
        elif choice == "2":
            run_automation()
        elif choice == "3":
            run_api_automation()
        elif choice == "4":
            from modules.mining_api import start_mining_all_accounts
            start_mining_all_accounts()
        elif choice == "0":
            print(Fore.MAGENTA + Style.BRIGHT + "\n👋 Goodbye! Have a productive day!\n")
            sys.exit(0)
        else:
            print(Fore.RED + Style.BRIGHT + "\n❌ Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main() 