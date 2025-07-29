import time
import random
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from modules.utils import log_info, log_warning, log_error

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.rate_limits = {
            'requests_per_minute': 30,
            'requests_per_hour': 1000,
            'min_delay_between_requests': 2,
            'max_delay_between_requests': 5
        }
        self.request_history = []
        self.lock = threading.Lock()
    
    def create_session(self, session_id: str, user_agent: str = None) -> Dict:
        """Create a new session"""
        with self.lock:
            session = {
                'id': session_id,
                'created_at': datetime.now(),
                'last_request': None,
                'request_count': 0,
                'user_agent': user_agent,
                'headers': {},
                'cookies': {},
                'active': True
            }
            self.sessions[session_id] = session
            log_info(f"Created session: {session_id}")
            return session
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, **kwargs):
        """Update session data"""
        with self.lock:
            if session_id in self.sessions:
                self.sessions[session_id].update(kwargs)
                self.sessions[session_id]['last_request'] = datetime.now()
    
    def remove_session(self, session_id: str):
        """Remove session"""
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                log_info(f"Removed session: {session_id}")
    
    def cleanup_inactive_sessions(self, max_age_hours: int = 24):
        """Clean up inactive sessions"""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            inactive_sessions = [
                sid for sid, session in self.sessions.items()
                if session['last_request'] and session['last_request'] < cutoff_time
            ]
            
            for sid in inactive_sessions:
                del self.sessions[sid]
            
            if inactive_sessions:
                log_info(f"Cleaned up {len(inactive_sessions)} inactive sessions")
    
    def check_rate_limit(self, session_id: str) -> bool:
        """Check if request is within rate limits"""
        with self.lock:
            now = datetime.now()
            
            # Remove old requests from history
            self.request_history = [
                req for req in self.request_history
                if now - req['timestamp'] < timedelta(hours=1)
            ]
            
            # Check minute limit
            minute_ago = now - timedelta(minutes=1)
            recent_requests = [
                req for req in self.request_history
                if req['timestamp'] > minute_ago
            ]
            
            if len(recent_requests) >= self.rate_limits['requests_per_minute']:
                log_warning(f"Rate limit exceeded for session {session_id}")
                return False
            
            # Check hour limit
            hour_ago = now - timedelta(hours=1)
            hourly_requests = [
                req for req in self.request_history
                if req['timestamp'] > hour_ago
            ]
            
            if len(hourly_requests) >= self.rate_limits['requests_per_hour']:
                log_warning(f"Hourly rate limit exceeded for session {session_id}")
                return False
            
            return True
    
    def record_request(self, session_id: str, endpoint: str):
        """Record a request"""
        with self.lock:
            request_record = {
                'session_id': session_id,
                'endpoint': endpoint,
                'timestamp': datetime.now()
            }
            self.request_history.append(request_record)
            
            # Update session
            if session_id in self.sessions:
                self.sessions[session_id]['request_count'] += 1
                self.sessions[session_id]['last_request'] = datetime.now()
    
    def get_delay_before_request(self) -> float:
        """Get delay before next request"""
        min_delay = self.rate_limits['min_delay_between_requests']
        max_delay = self.rate_limits['max_delay_between_requests']
        
        # Add some randomness to avoid patterns
        base_delay = random.uniform(min_delay, max_delay)
        
        # Increase delay if we're approaching rate limits
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        recent_requests = [
            req for req in self.request_history
            if req['timestamp'] > minute_ago
        ]
        
        if len(recent_requests) > self.rate_limits['requests_per_minute'] * 0.8:
            base_delay *= 1.5
        
        return base_delay
    
    def wait_for_rate_limit(self, session_id: str):
        """Wait if rate limit is exceeded"""
        while not self.check_rate_limit(session_id):
            delay = self.get_delay_before_request()
            log_warning(f"Rate limit active, waiting {delay:.2f} seconds...")
            time.sleep(delay)
    
    def get_session_stats(self) -> Dict:
        """Get session statistics"""
        with self.lock:
            active_sessions = len([s for s in self.sessions.values() if s['active']])
            total_requests = sum(s['request_count'] for s in self.sessions.values())
            
            return {
                'active_sessions': active_sessions,
                'total_sessions': len(self.sessions),
                'total_requests': total_requests,
                'requests_last_hour': len(self.request_history)
            }
    
    def rotate_user_agents(self, session_id: str):
        """Rotate user agent for session"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        new_agent = random.choice(user_agents)
        self.update_session(session_id, user_agent=new_agent)
        log_info(f"Rotated user agent for session {session_id}")

# Global session manager instance
session_manager = SessionManager() 