from colorama import Fore, Style, init
import sys
import time
init(autoreset=True)

# Import generation and automation functions
from modules.gmail_dot_generator import save_gmail_variants_to_accounts
import importlib
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import questionary
from modules.api_interaction import main_api
from modules.mining_api import start_mining_all_accounts
from config import CONFIG

def print_logo():
    console = Console()
    logo = '''
[bold magenta]
 █    ██  ███▄    █  ██▓ ▄████▄   ██░ ██     ██▓███   ██░ ██  ▒█████  ▓█████  ███▄    █  ██▓▒██   ██▒
 ██  ▓██▒ ██ ▀█   █ ▓██▒▒██▀ ▀█  ▓██░ ██▒   ▓██░  ██▒▓██░ ██▒▒██▒  ██▒▓█   ▀  ██ ▀█   █ ▓██▒▒▒ █ █ ▒░
▓██  ▒██░▓██  ▀█ ██▒▒██▒▒▓█    ▄ ▒██▀▀██░   ▓██░ ██▓▒▒██▀▀██░▒██░  ██▒▒███   ▓██  ▀█ ██▒▒██▒░░  █   ░
▓▓█  ░██░▓██▒  ▐▌██▒░██░▒▓▓▄ ▄██▒░▓█ ░██    ▒██▄█▓▒ ▒░▓█ ░██ ▒██   ██░▒▓█  ▄ ▓██▒  ▐▌██▒░██░ ░ █ █ ▒ 
▒▒█████▓ ▒██░   ▓██░░██░▒ ▓███▀ ░░▓█▒░██▓   ▒██▒ ░  ░░▓█▒░██▓░ ████▓▒░░▒████▒▒██░   ▓██░░██░▒██▒ ▒██▒
░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ░▓  ░ ░▒ ▒  ░ ▒ ░░▒░▒   ▒▓▒░ ░  ░ ▒ ░░▒░▒░ ▒░▒░▒░ ░░ ▒░ ░░ ▒░   ▒ ▒ ░▓  ▒▒ ░ ░▓ ░
░░▒░ ░ ░ ░ ░░   ░ ▒░ ▒ ░  ░  ▒    ▒ ░▒░ ░   ░▒ ░      ▒ ░▒░ ░  ░ ▒ ▒░  ░ ░  ░░ ░░   ░ ▒░ ▒ ░░░   ░▒ ░
 ░░░ ░ ░    ░   ░ ░  ▒ ░░         ░  ░░ ░   ░░        ░  ░░ ░░ ░ ░ ▒     ░      ░   ░ ░  ▒ ░ ░    ░  
   ░              ░  ░  ░ ░       ░  ░  ░             ░  ░  ░    ░ ░     ░  ░         ░  ░   ░    ░  
                        ░                                                                            
[/bold magenta]
    '''
    console.print(logo, justify="center")

def print_features():
    console = Console()
    table = Table(show_header=False, box=None, expand=True)
    table.add_row("[bold yellow]1.[/bold yellow]", "✉️  Generate Gmail Dot Trick Emails")
    table.add_row("[bold yellow]2.[/bold yellow]", "🔌 API Registration (2Captcha/Anticaptcha/Capsolver)")
    table.add_row("[bold yellow]3.[/bold yellow]", "⛏️  Start Mining for All Accounts")
    table.add_row("[bold yellow]4.[/bold yellow]", "📊 View Statistics & Performance")
    table.add_row("[bold yellow]5.[/bold yellow]", "🔍 System Health Check")
    table.add_row("[bold yellow]6.[/bold yellow]", "📦 Backup & Restore Management")
    table.add_row("[bold red]0.[/bold red]", "❌ Exit")
    panel = Panel(table, title="[bold cyan]🔥 Features[/bold cyan]", subtitle="by PhoenixCrypto_PC", style="bold cyan", padding=(1,2))
    console.print("\n" + "="*60)
    console.print("[bold cyan]-🤖 UNICH Project Automation by PhoenixCrypto_PC 🤖-".center(60))
    console.print("="*60 + "\n")
    console.print(panel)
    console.print("[magenta]📢 Telegram Channel: [white]@PhoenixCrypto_PC")
    console.print("[blue]🔗 https://t.me/PhoenixCrypto_PC\n")

def run_automation(chromedriver_arch='win64'):
    print(Fore.GREEN + Style.BRIGHT + "\n🚀 Starting referral automation...\n")
    automation = importlib.import_module("modules.automation")
    automation.main(chromedriver_arch=chromedriver_arch)

def run_api_automation():
    print(Fore.GREEN + Style.BRIGHT + "\n🔌 Starting API direct registration...\n")
    # استيراد دالة main_api من وحدة API
    main_api()

def main():
    # Print logo and features only once
    print_logo()
    print_features()
    
    # Options menu in a loop
    options = [
         "1. ✉️ Generate Gmail Dot Trick Emails",
         "2. 🔌 API Registration (2Captcha/Anticaptcha/Capsolver)",
         "3. ⛏️ Start Mining for All Accounts",
         "4. 📊 View Statistics & Performance",
         "5. 🔍 System Health Check",
         "6. 📦 Backup & Restore Management",
         "0. ❌ Exit"
     ]
    import questionary
    while True:
        answer = questionary.select(
            "? 👉 Choose an option:",
            choices=options
        ).ask()
        if answer is None:
            print("No option selected. Exiting...")
            exit(0)
        if answer.startswith("1"):
            # Call Gmail dot trick email generator
            print(f"{Fore.CYAN}✉️  Gmail Dot Trick Generator{Style.RESET_ALL}")
            print("="*50)
            
            # Get username
            username = questionary.text(
                "Enter Gmail username (before @):",
                validate=lambda text: True if text.strip() else "Username cannot be empty"
            ).ask()
            
            if username is None:
                print("Operation cancelled. Returning to menu.")
                continue
                
            # Get password
            password = questionary.text(
                "Enter password for all emails:",
                validate=lambda text: True if text.strip() else "Password cannot be empty"
            ).ask()
            
            if password is None:
                print("Operation cancelled. Returning to menu.")
                continue
            
            # Generate and save emails
            try:
                save_gmail_variants_to_accounts(username.strip(), password.strip())
                print(f"{Fore.GREEN}✅ Gmail variants generated successfully!")
            except Exception as e:
                print(f"{Fore.RED}❌ Error generating Gmail variants: {e}")
            
            print("\n" + "="*50)
        elif answer.startswith("2"):
            # Ask user which captcha provider to use
            captcha_choices = [
                ("2captcha", "API_KEY_2CAPTCHA"),
                ("anticaptcha", "API_KEY_ANTICAPTCHA"),
                ("capsolver", "API_KEY_CAPSOLVER")
            ]
            provider = questionary.select(
                "Which captcha provider do you want to use?",
                choices=[c[0] for c in captcha_choices]
            ).ask()
            if provider is None:
                print("No captcha provider selected. Returning to menu.")
                continue
            key_name = dict(captcha_choices)[provider]
            api_key = CONFIG['CAPTCHA'].get(key_name, '')
            if not api_key:
                print(f"[ERROR] No API key set for {provider} in config.py! Returning to menu.")
                continue
            print(f"[INFO] Using {provider} for captcha solving.")
            main_api(force_captcha_provider=provider)
        elif answer.startswith("3"):
            # Call mining function
            start_mining_all_accounts()
        elif answer.startswith("4"):
            # View Statistics & Performance
            try:
                from modules.stats import stats_manager
                from modules.performance_monitor import performance_monitor
                
                print(f"{Fore.CYAN}📊 Statistics & Performance Dashboard{Style.RESET_ALL}")
                print("="*60)
                
                # Show statistics
                stats_manager.print_summary()
                print()
                
                # Show performance
                performance_monitor.print_performance_summary()
                print()
                
                # Show recent alerts
                recent_alerts = performance_monitor.get_recent_alerts()
                if recent_alerts:
                    print(f"{Fore.YELLOW}⚠️ Recent Alerts:")
                    for alert in recent_alerts[-5:]:  # Show last 5 alerts
                        print(f"   {alert['timestamp'].strftime('%H:%M:%S')} - {alert['message']}")
                else:
                    print(f"{Fore.GREEN}✅ No recent alerts")
                
                print("="*60)
            except Exception as e:
                print(f"{Fore.RED}❌ Error loading statistics: {e}")
        elif answer.startswith("5"):
            # System Health Check
            try:
                from modules.performance_monitor import performance_monitor
                from modules.session_manager import session_manager
                
                print(f"{Fore.CYAN}🔍 System Health Check{Style.RESET_ALL}")
                print("="*60)
                
                # Start monitoring if not already running
                if not performance_monitor.monitoring:
                    performance_monitor.start_monitoring()
                
                # Get current metrics
                current_metrics = performance_monitor.get_current_metrics()
                if current_metrics:
                    print(f"{Fore.BLUE}Current System Status:")
                    print(f"   CPU: {current_metrics['cpu_percent']:.1f}%")
                    print(f"   Memory: {current_metrics['memory_percent']:.1f}%")
                    print(f"   Disk: {current_metrics['disk_percent']:.1f}%")
                    print(f"   Process Memory: {current_metrics['process_memory_mb']:.1f} MB")
                else:
                    print(f"{Fore.YELLOW}Collecting system metrics...")
                    time.sleep(2)
                    current_metrics = performance_monitor.get_current_metrics()
                    if current_metrics:
                        print(f"{Fore.BLUE}Current System Status:")
                        print(f"   CPU: {current_metrics['cpu_percent']:.1f}%")
                        print(f"   Memory: {current_metrics['memory_percent']:.1f}%")
                        print(f"   Disk: {current_metrics['disk_percent']:.1f}%")
                        print(f"   Process Memory: {current_metrics['process_memory_mb']:.1f} MB")
                
                # Get session stats
                session_stats = session_manager.get_session_stats()
                print(f"\n{Fore.BLUE}Session Status:")
                print(f"   Active Sessions: {session_stats['active_sessions']}")
                print(f"   Total Requests: {session_stats['total_requests']}")
                print(f"   Requests (Last Hour): {session_stats['requests_last_hour']}")
                
                # Show system health status
                print(f"\n{Fore.CYAN}System Health Status:")
                if current_metrics:
                    cpu_status = "🟢 Good" if current_metrics['cpu_percent'] < 80 else "🟡 Warning" if current_metrics['cpu_percent'] < 90 else "🔴 Critical"
                    memory_status = "🟢 Good" if current_metrics['memory_percent'] < 80 else "🟡 Warning" if current_metrics['memory_percent'] < 90 else "🔴 Critical"
                    disk_status = "🟢 Good" if current_metrics['disk_percent'] < 80 else "🟡 Warning" if current_metrics['disk_percent'] < 90 else "🔴 Critical"
                    
                    print(f"   CPU: {cpu_status}")
                    print(f"   Memory: {memory_status}")
                    print(f"   Disk: {disk_status}")
                else:
                    print(f"   ⚠️  Collecting data...")
                
                print("="*60)
                # Add a small delay to prevent text overlap
                time.sleep(1)
            except Exception as e:
                print(f"{Fore.RED}❌ Error during health check: {e}")
        elif answer.startswith("6"):
            # Backup & Restore Management
            try:
                from modules.backup_manager import backup_manager
                 
                print(f"{Fore.CYAN}📦 Backup & Restore Management{Style.RESET_ALL}")
                print("="*60)
                
                backup_options = [
                    "1. Create Backup Now",
                    "2. View Backup Status",
                    "3. List All Backups",
                    "4. Restore from Backup",
                    "5. Auto Backup Check",
                    "0. Back to Main Menu"
                ]
                
                while True:
                    backup_choice = questionary.select(
                        "Choose backup option:",
                        choices=backup_options
                    ).ask()
                    
                    if backup_choice is None:
                        break
                    
                    if backup_choice.startswith("1"):
                        # Create backup
                        success = backup_manager.create_backup(force=True)
                        if success:
                            print(f"{Fore.GREEN}✅ Backup created successfully!")
                        else:
                            print(f"{Fore.RED}❌ Backup failed!")
                    
                    elif backup_choice.startswith("2"):
                        # View status
                        backup_manager.print_backup_status()
                    
                    elif backup_choice.startswith("3"):
                        # List backups
                        backups = backup_manager.list_backups()
                        if backups:
                            print(f"{Fore.BLUE}📋 Available Backups:")
                            for i, backup in enumerate(backups[:5], 1):  # Show last 5
                                print(f"   {i}. {backup['backup_name']} - {backup['timestamp']}")
                                print(f"      Files: {len(backup['files_copied'])}")
                        else:
                            print(f"{Fore.YELLOW}No backups found")
                    
                    elif backup_choice.startswith("4"):
                        # Restore backup
                        backups = backup_manager.list_backups()
                        if backups:
                            backup_names = [b['backup_name'] for b in backups[:5]]
                            selected_backup = questionary.select(
                                "Select backup to restore:",
                                choices=backup_names
                            ).ask()
                            
                            if selected_backup:
                                confirm = questionary.confirm(
                                    f"Are you sure you want to restore from {selected_backup}?"
                                ).ask()
                                
                                if confirm:
                                    success = backup_manager.restore_backup(selected_backup)
                                    if success:
                                        print(f"{Fore.GREEN}✅ Restore completed!")
                                    else:
                                        print(f"{Fore.RED}❌ Restore failed!")
                        else:
                            print(f"{Fore.YELLOW}No backups available for restore")
                    
                    elif backup_choice.startswith("5"):
                        # Auto backup check
                        success = backup_manager.auto_backup()
                        if success:
                            print(f"{Fore.GREEN}✅ Auto backup check completed!")
                        else:
                            print(f"{Fore.RED}❌ Auto backup failed!")
                    
                    elif backup_choice.startswith("0"):
                        break
                
                print("="*60)
            except Exception as e:
                print(f"{Fore.RED}❌ Error in backup management: {e}")
        
        elif answer.startswith("0"):
            print("Exiting...")
            exit(0)
        else:
            print("Unknown option!")
            exit(1)

if __name__ == "__main__":
    main() 