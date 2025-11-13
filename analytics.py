"""
analytics.py - Application Usage Analytics
Local tracking system for monitoring application usage

Tracks:
- Application opens (sessions)
- Files generated (conversions)

Data stored locally in: ~/.word2elementor/stats.json
"""

import json
import os
from pathlib import Path
from datetime import datetime


class Analytics:
    """Local analytics tracker for application usage"""
    
    def __init__(self):
        """Initialize analytics with local storage"""
        # Create hidden directory in user home
        self.stats_dir = Path.home() / ".word2elementor"
        self.stats_file = self.stats_dir / "stats.json"
        
        # Ensure directory exists
        self.stats_dir.mkdir(exist_ok=True)
        
        # Initialize stats file if doesn't exist
        if not self.stats_file.exists():
            self._create_stats_file()
    
    def _create_stats_file(self):
        """Create initial stats file"""
        initial_stats = {
            "app_opens": 0,
            "files_generated": 0,
            "first_use": datetime.now().isoformat(),
            "last_use": datetime.now().isoformat(),
            "version": "3.0"
        }
        
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(initial_stats, f, indent=2)
    
    def _read_stats(self):
        """Read current statistics"""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file corrupted or missing, recreate
            self._create_stats_file()
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    def _write_stats(self, stats):
        """Write statistics to file"""
        stats['last_use'] = datetime.now().isoformat()
        
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def increment_opens(self):
        """Increment application open counter"""
        stats = self._read_stats()
        stats['app_opens'] = stats.get('app_opens', 0) + 1
        self._write_stats(stats)
    
    def increment_conversions(self):
        """Increment file conversion counter"""
        stats = self._read_stats()
        stats['files_generated'] = stats.get('files_generated', 0) + 1
        self._write_stats(stats)
    
    def get_stats(self):
        """Get current statistics
        
        Returns:
            dict: Dictionary with app_opens and files_generated
        """
        stats = self._read_stats()
        return {
            'app_opens': stats.get('app_opens', 0),
            'files_generated': stats.get('files_generated', 0),
            'first_use': stats.get('first_use', 'N/A'),
            'last_use': stats.get('last_use', 'N/A'),
            'version': stats.get('version', '3.0')
        }
    
    def get_success_rate(self):
        """Calculate conversion success rate
        
        Returns:
            float: Success rate percentage (0-100)
        """
        stats = self.get_stats()
        opens = stats['app_opens']
        conversions = stats['files_generated']
        
        if opens == 0:
            return 0.0
        
        return round((conversions / opens) * 100, 1)


# Global analytics instance
_analytics_instance = None


def get_analytics():
    """Get global analytics instance
    
    Returns:
        Analytics: Global analytics instance
    """
    global _analytics_instance
    
    if _analytics_instance is None:
        _analytics_instance = Analytics()
    
    return _analytics_instance


def track_app_open():
    """Track application open - call at app startup"""
    analytics = get_analytics()
    analytics.increment_opens()


def track_conversion():
    """Track successful file conversion"""
    analytics = get_analytics()
    analytics.increment_conversions()


def get_current_stats():
    """Get current statistics
    
    Returns:
        dict: Current statistics
    """
    analytics = get_analytics()
    return analytics.get_stats()


def get_stats_summary():
    """Get formatted statistics summary
    
    Returns:
        dict: Formatted statistics for display
    """
    analytics = get_analytics()
    stats = analytics.get_stats()
    success_rate = analytics.get_success_rate()
    
    return {
        'sessions': stats['app_opens'],
        'conversions': stats['files_generated'],
        'success_rate': success_rate,
        'first_use': stats['first_use'],
        'last_use': stats['last_use']
    }
