import os
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
from modules.utils import log_info, log_success, log_error, log_warning

class BackupManager:
    def __init__(self, backup_dir="backups"):
        self.backup_dir = backup_dir
        self.data_dir = "data"
        self.backup_interval_hours = 6  # Backup every 6 hours
        self.max_backups = 10  # Keep last 10 backups
        self.last_backup_file = os.path.join(backup_dir, "last_backup.json")
        
        # Create backup directory
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def should_backup(self) -> bool:
        """Check if backup is needed"""
        if not os.path.exists(self.last_backup_file):
            return True
        
        try:
            with open(self.last_backup_file, 'r') as f:
                last_backup_data = json.load(f)
            
            last_backup_time = datetime.fromisoformat(last_backup_data['timestamp'])
            time_since_backup = datetime.now() - last_backup_time
            
            return time_since_backup.total_seconds() > (self.backup_interval_hours * 3600)
        except Exception as e:
            log_error(f"Error checking backup status: {e}")
            return True
    
    def create_backup(self, force: bool = False) -> bool:
        """Create a backup of data files"""
        if not force and not self.should_backup():
            log_info("Backup not needed yet")
            return True
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Create backup directory
            os.makedirs(backup_path, exist_ok=True)
            
            # Copy data files
            data_files = ['accounts.txt', 'done.txt', 'errors.txt', 'statistics.json']
            copied_files = []
            
            for file_name in data_files:
                source_path = os.path.join(self.data_dir, file_name)
                if os.path.exists(source_path):
                    dest_path = os.path.join(backup_path, file_name)
                    shutil.copy2(source_path, dest_path)
                    copied_files.append(file_name)
            
            # Save backup metadata
            backup_metadata = {
                'timestamp': datetime.now().isoformat(),
                'backup_name': backup_name,
                'files_copied': copied_files,
                'backup_size': self._get_directory_size(backup_path)
            }
            
            metadata_path = os.path.join(backup_path, 'backup_info.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(backup_metadata, f, indent=2, ensure_ascii=False)
            
            # Update last backup info
            with open(self.last_backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_metadata, f, indent=2, ensure_ascii=False)
            
            log_success(f"Backup created: {backup_name} ({len(copied_files)} files)")
            
            # Clean old backups
            self._cleanup_old_backups()
            
            return True
            
        except Exception as e:
            log_error(f"Error creating backup: {e}")
            return False
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore from a specific backup"""
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            if not os.path.exists(backup_path):
                log_error(f"Backup {backup_name} not found")
                return False
            
            # Create restore backup first
            restore_backup_name = f"restore_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            restore_backup_path = os.path.join(self.backup_dir, restore_backup_name)
            os.makedirs(restore_backup_path, exist_ok=True)
            
            # Backup current data before restore
            data_files = ['accounts.txt', 'done.txt', 'errors.txt', 'statistics.json']
            for file_name in data_files:
                source_path = os.path.join(self.data_dir, file_name)
                if os.path.exists(source_path):
                    dest_path = os.path.join(restore_backup_path, file_name)
                    shutil.copy2(source_path, dest_path)
            
            # Restore from backup
            for file_name in data_files:
                source_path = os.path.join(backup_path, file_name)
                if os.path.exists(source_path):
                    dest_path = os.path.join(self.data_dir, file_name)
                    shutil.copy2(source_path, dest_path)
                    log_info(f"Restored: {file_name}")
            
            log_success(f"Restore completed from {backup_name}")
            log_info(f"Current data backed up to: {restore_backup_name}")
            
            return True
            
        except Exception as e:
            log_error(f"Error restoring backup: {e}")
            return False
    
    def list_backups(self) -> list:
        """List all available backups"""
        backups = []
        
        if not os.path.exists(self.backup_dir):
            return backups
        
        for item in os.listdir(self.backup_dir):
            if item.startswith('backup_'):
                backup_path = os.path.join(self.backup_dir, item)
                if os.path.isdir(backup_path):
                    backup_info = self._get_backup_info(backup_path)
                    if backup_info:
                        backups.append(backup_info)
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        return backups
    
    def _get_backup_info(self, backup_path: str) -> dict:
        """Get backup information"""
        try:
            info_path = os.path.join(backup_path, 'backup_info.json')
            if os.path.exists(info_path):
                with open(info_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Fallback: create basic info from directory
            backup_name = os.path.basename(backup_path)
            files = [f for f in os.listdir(backup_path) if f != 'backup_info.json']
            
            return {
                'backup_name': backup_name,
                'timestamp': datetime.fromtimestamp(os.path.getctime(backup_path)).isoformat(),
                'files_copied': files,
                'backup_size': self._get_directory_size(backup_path)
            }
        except Exception as e:
            log_error(f"Error getting backup info: {e}")
            return None
    
    def _get_directory_size(self, directory: str) -> int:
        """Get directory size in bytes"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
        except Exception:
            pass
        return total_size
    
    def _cleanup_old_backups(self):
        """Remove old backups to save space"""
        backups = self.list_backups()
        
        if len(backups) > self.max_backups:
            backups_to_remove = backups[self.max_backups:]
            
            for backup in backups_to_remove:
                backup_path = os.path.join(self.backup_dir, backup['backup_name'])
                try:
                    shutil.rmtree(backup_path)
                    log_info(f"Removed old backup: {backup['backup_name']}")
                except Exception as e:
                    log_error(f"Error removing backup {backup['backup_name']}: {e}")
    
    def print_backup_status(self):
        """Print backup status"""
        backups = self.list_backups()
        
        log_info("📦 Backup Status:")
        log_info(f"   Total Backups: {len(backups)}")
        log_info(f"   Max Backups: {self.max_backups}")
        log_info(f"   Backup Interval: {self.backup_interval_hours} hours")
        
        if backups:
            latest_backup = backups[0]
            log_info(f"   Latest Backup: {latest_backup['backup_name']}")
            log_info(f"   Latest Backup Time: {latest_backup['timestamp']}")
            log_info(f"   Files in Latest: {len(latest_backup['files_copied'])}")
        
        if self.should_backup():
            log_warning("   Backup needed!")
        else:
            log_success("   Backup up to date")
    
    def auto_backup(self) -> bool:
        """Automatic backup if needed"""
        if self.should_backup():
            log_info("🔄 Starting automatic backup...")
            return self.create_backup()
        return True

# Global backup manager instance
backup_manager = BackupManager() 