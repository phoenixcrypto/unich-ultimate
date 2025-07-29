import psutil
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List
from modules.utils import log_info, log_warning, log_error

class PerformanceMonitor:
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.performance_data = []
        self.max_data_points = 1000
        self.monitor_interval = 30  # seconds
        
        # Thresholds
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'network_errors': 10
        }
        
        # Alerts
        self.alerts = []
        self.max_alerts = 100
    
    def start_monitoring(self):
        """Start performance monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            log_info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        log_info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                self._collect_metrics()
                self._check_thresholds()
                time.sleep(self.monitor_interval)
            except Exception as e:
                log_error(f"Error in performance monitoring: {e}")
                time.sleep(5)
    
    def _collect_metrics(self):
        """Collect system metrics"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Network
            network_stats = psutil.net_io_counters()
            
            # Process info
            process = psutil.Process()
            process_memory = process.memory_info().rss / 1024 / 1024  # MB
            process_cpu = process.cpu_percent()
            
            metrics = {
                'timestamp': datetime.now(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent,
                'process_memory_mb': process_memory,
                'process_cpu_percent': process_cpu,
                'network_bytes_sent': network_stats.bytes_sent,
                'network_bytes_recv': network_stats.bytes_recv
            }
            
            self.performance_data.append(metrics)
            
            # Keep only recent data points
            if len(self.performance_data) > self.max_data_points:
                self.performance_data = self.performance_data[-self.max_data_points:]
                
        except Exception as e:
            log_error(f"Error collecting metrics: {e}")
    
    def _check_thresholds(self):
        """Check if metrics exceed thresholds"""
        if not self.performance_data:
            return
        
        latest = self.performance_data[-1]
        
        # Check CPU
        if latest['cpu_percent'] > self.thresholds['cpu_percent']:
            self._add_alert('HIGH_CPU', f"CPU usage: {latest['cpu_percent']:.1f}%")
        
        # Check Memory
        if latest['memory_percent'] > self.thresholds['memory_percent']:
            self._add_alert('HIGH_MEMORY', f"Memory usage: {latest['memory_percent']:.1f}%")
        
        # Check Disk
        if latest['disk_percent'] > self.thresholds['disk_percent']:
            self._add_alert('HIGH_DISK', f"Disk usage: {latest['disk_percent']:.1f}%")
    
    def _add_alert(self, alert_type: str, message: str):
        """Add performance alert"""
        alert = {
            'timestamp': datetime.now(),
            'type': alert_type,
            'message': message
        }
        
        self.alerts.append(alert)
        
        # Keep only recent alerts
        if len(self.alerts) > self.max_alerts:
            self.alerts = self.alerts[-self.max_alerts:]
        
        log_warning(f"Performance alert: {message}")
    
    def get_current_metrics(self) -> Dict:
        """Get current system metrics"""
        if not self.performance_data:
            return {}
        
        return self.performance_data[-1]
    
    def get_performance_summary(self, hours: int = 1) -> Dict:
        """Get performance summary for the last N hours"""
        if not self.performance_data:
            return {}
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_data = [
            data for data in self.performance_data
            if data['timestamp'] > cutoff_time
        ]
        
        if not recent_data:
            return {}
        
        # Calculate averages
        avg_cpu = sum(d['cpu_percent'] for d in recent_data) / len(recent_data)
        avg_memory = sum(d['memory_percent'] for d in recent_data) / len(recent_data)
        avg_disk = sum(d['disk_percent'] for d in recent_data) / len(recent_data)
        
        # Calculate max values
        max_cpu = max(d['cpu_percent'] for d in recent_data)
        max_memory = max(d['memory_percent'] for d in recent_data)
        max_disk = max(d['disk_percent'] for d in recent_data)
        
        return {
            'period_hours': hours,
            'data_points': len(recent_data),
            'avg_cpu_percent': round(avg_cpu, 2),
            'avg_memory_percent': round(avg_memory, 2),
            'avg_disk_percent': round(avg_disk, 2),
            'max_cpu_percent': round(max_cpu, 2),
            'max_memory_percent': round(max_memory, 2),
            'max_disk_percent': round(max_disk, 2),
            'alerts_count': len([a for a in self.alerts if a['timestamp'] > cutoff_time])
        }
    
    def print_performance_summary(self, hours: int = 1):
        """Print performance summary"""
        summary = self.get_performance_summary(hours)
        if not summary:
            log_info("No performance data available")
            return
        
        log_info(f"📊 Performance Summary (Last {hours}h):")
        log_info(f"   Data Points: {summary['data_points']}")
        log_info(f"   Avg CPU: {summary['avg_cpu_percent']}%")
        log_info(f"   Avg Memory: {summary['avg_memory_percent']}%")
        log_info(f"   Avg Disk: {summary['avg_disk_percent']}%")
        log_info(f"   Max CPU: {summary['max_cpu_percent']}%")
        log_info(f"   Max Memory: {summary['max_memory_percent']}%")
        log_info(f"   Max Disk: {summary['max_disk_percent']}%")
        log_info(f"   Alerts: {summary['alerts_count']}")
    
    def get_recent_alerts(self, hours: int = 1) -> List[Dict]:
        """Get recent alerts"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [
            alert for alert in self.alerts
            if alert['timestamp'] > cutoff_time
        ]
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()
        log_info("Performance alerts cleared")
    
    def set_thresholds(self, **kwargs):
        """Set performance thresholds"""
        for key, value in kwargs.items():
            if key in self.thresholds:
                self.thresholds[key] = value
                log_info(f"Updated threshold {key}: {value}")

# Global performance monitor instance
performance_monitor = PerformanceMonitor() 