import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from modules.utils import log_info, log_success, log_error

class StatisticsManager:
    def __init__(self, stats_file="data/statistics.json"):
        self.stats_file = stats_file
        self.stats = self.load_stats()
    
    def load_stats(self) -> Dict:
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                log_error(f"Error loading statistics: {e}")
                return self.get_default_stats()
        return self.get_default_stats()
    
    def get_default_stats(self) -> Dict:
        """Get default statistics structure"""
        return {
            "total_accounts": 0,
            "successful_registrations": 0,
            "failed_registrations": 0,
            "success_rate": 0.0,
            "captcha_success": 0,
            "captcha_failed": 0,
            "otp_success": 0,
            "otp_failed": 0,
            "mining_started": 0,
            "mining_failed": 0,
            "daily_stats": {},
            "hourly_stats": {},
            "errors": [],
            "start_time": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            self.stats["last_updated"] = datetime.now().isoformat()
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Error saving statistics: {e}")
    
    def update_registration_stats(self, success: bool, captcha_provider: str = None):
        """Update registration statistics"""
        self.stats["total_accounts"] += 1
        
        if success:
            self.stats["successful_registrations"] += 1
        else:
            self.stats["failed_registrations"] += 1
        
        self.stats["success_rate"] = (
            self.stats["successful_registrations"] / self.stats["total_accounts"] * 100
        )
        
        # Update daily stats
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.stats["daily_stats"]:
            self.stats["daily_stats"][today] = {"success": 0, "failed": 0}
        
        if success:
            self.stats["daily_stats"][today]["success"] += 1
        else:
            self.stats["daily_stats"][today]["failed"] += 1
        
        # Update hourly stats
        hour = datetime.now().strftime("%Y-%m-%d %H:00")
        if hour not in self.stats["hourly_stats"]:
            self.stats["hourly_stats"][hour] = {"success": 0, "failed": 0}
        
        if success:
            self.stats["hourly_stats"][hour]["success"] += 1
        else:
            self.stats["hourly_stats"][hour]["failed"] += 1
        
        self.save_stats()
    
    def update_captcha_stats(self, success: bool, provider: str):
        """Update captcha statistics"""
        if success:
            self.stats["captcha_success"] += 1
        else:
            self.stats["captcha_failed"] += 1
        self.save_stats()
    
    def update_otp_stats(self, success: bool):
        """Update OTP statistics"""
        if success:
            self.stats["otp_success"] += 1
        else:
            self.stats["otp_failed"] += 1
        self.save_stats()
    
    def update_mining_stats(self, success: bool):
        """Update mining statistics"""
        if success:
            self.stats["mining_started"] += 1
        else:
            self.stats["mining_failed"] += 1
        self.save_stats()
    
    def add_error(self, error: str, account: str = None):
        """Add error to statistics"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "account": account
        }
        self.stats["errors"].append(error_entry)
        
        # Keep only last 100 errors
        if len(self.stats["errors"]) > 100:
            self.stats["errors"] = self.stats["errors"][-100:]
        
        self.save_stats()
    
    def get_summary(self) -> Dict:
        """Get statistics summary"""
        return {
            "total_accounts": self.stats["total_accounts"],
            "successful": self.stats["successful_registrations"],
            "failed": self.stats["failed_registrations"],
            "success_rate": f"{self.stats['success_rate']:.2f}%",
            "captcha_success_rate": self._calculate_rate(self.stats["captcha_success"], self.stats["captcha_success"] + self.stats["captcha_failed"]),
            "otp_success_rate": self._calculate_rate(self.stats["otp_success"], self.stats["otp_success"] + self.stats["otp_failed"]),
            "mining_success_rate": self._calculate_rate(self.stats["mining_started"], self.stats["mining_started"] + self.stats["mining_failed"]),
            "uptime": self._calculate_uptime(),
            "recent_errors": len([e for e in self.stats["errors"] if datetime.fromisoformat(e["timestamp"]) > datetime.now() - timedelta(hours=1)])
        }
    
    def _calculate_rate(self, success: int, total: int) -> str:
        """Calculate success rate"""
        if total == 0:
            return "0.00%"
        return f"{(success / total * 100):.2f}%"
    
    def _calculate_uptime(self) -> str:
        """Calculate uptime"""
        try:
            start_time = datetime.fromisoformat(self.stats["start_time"])
            uptime = datetime.now() - start_time
            days = uptime.days
            hours = uptime.seconds // 3600
            minutes = (uptime.seconds % 3600) // 60
            return f"{days}d {hours}h {minutes}m"
        except:
            return "Unknown"
    
    def print_summary(self):
        """Print statistics summary"""
        summary = self.get_summary()
        log_info("📊 Statistics Summary:")
        log_info(f"   Total Accounts: {summary['total_accounts']}")
        log_info(f"   Successful: {summary['successful']}")
        log_info(f"   Failed: {summary['failed']}")
        log_info(f"   Success Rate: {summary['success_rate']}")
        log_info(f"   Captcha Success Rate: {summary['captcha_success_rate']}")
        log_info(f"   OTP Success Rate: {summary['otp_success_rate']}")
        log_info(f"   Mining Success Rate: {summary['mining_success_rate']}")
        log_info(f"   Uptime: {summary['uptime']}")
        log_info(f"   Recent Errors (1h): {summary['recent_errors']}")

# Global statistics manager instance
stats_manager = StatisticsManager() 