"""
CoreX Template Cache
Caches compiled templates for performance
"""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Dict, Optional, Any

from ..utils import print_info, print_warning


class TemplateCache:
    """Cache for compiled templates"""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        if cache_dir is None:
            # Use default cache directory
            cache_dir = Path.home() / ".corex" / "cache"
        
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "template_cache.json"
        self.cache_data = self._load_cache()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load cache data from file"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print_warning(f"Failed to load template cache: {e}")
                return {}
        return {}
    
    def _save_cache(self) -> None:
        """Save cache data to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache_data, f, indent=2)
        except Exception as e:
            print_warning(f"Failed to save template cache: {e}")
    
    def _get_cache_key(self, template_path: Path, context: Dict) -> str:
        """Generate a cache key for a template and context"""
        # Create a hash of the template path and context
        key_data = f"{template_path.absolute()}{json.dumps(context, sort_keys=True)}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def get(self, template_path: Path, context: Dict) -> Optional[str]:
        """Get cached template content"""
        cache_key = self._get_cache_key(template_path, context)
        
        if cache_key in self.cache_data:
            cache_entry = self.cache_data[cache_key]
            
            # Check if cache is still valid (1 hour by default)
            if time.time() - cache_entry.get("timestamp", 0) < 3600:
                print_info(f"Using cached template for {template_path.name}")
                return cache_entry.get("content")
            else:
                # Remove expired entry
                del self.cache_data[cache_key]
                self._save_cache()
        
        return None
    
    def set(self, template_path: Path, context: Dict, content: str) -> None:
        """Cache template content"""
        cache_key = self._get_cache_key(template_path, context)
        
        self.cache_data[cache_key] = {
            "content": content,
            "timestamp": time.time(),
            "template_path": str(template_path.absolute())
        }
        
        self._save_cache()
    
    def clear(self) -> None:
        """Clear all cached templates"""
        self.cache_data = {}
        self._save_cache()
        print_info("Template cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_entries = len(self.cache_data)
        total_size = sum(len(entry.get("content", "")) for entry in self.cache_data.values())
        
        return {
            "total_entries": total_entries,
            "total_size_bytes": total_size,
            "cache_file": str(self.cache_file)
        }