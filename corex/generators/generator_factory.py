"""
CoreX Generator Factory
Factory for creating generator instances
"""

from typing import Dict, Any, Optional
from pathlib import Path

from .base_generator import BaseGenerator
from .project_generator import ProjectGenerator
from .app_generator import AppGenerator
from .template_cache import TemplateCache


class GeneratorFactory:
    """Factory for creating generator instances"""
    
    def __init__(self, cache_enabled: bool = True):
        self.cache_enabled = cache_enabled
        self.cache: Optional[TemplateCache] = TemplateCache() if cache_enabled else None
        self._generators = {}
    
    def create_project_generator(self) -> ProjectGenerator:
        """Create a project generator instance"""
        generator = ProjectGenerator()
        if self.cache_enabled and self.cache:
            # Wrap generator with caching functionality
            original_render_template = generator._render_template
            
            def cached_render_template(template_name: str, context: Dict) -> str:
                # Try to get from cache first
                template_path = generator.templates_dir / template_name
                if self.cache:
                    cached_content = self.cache.get(template_path, context)
                    if cached_content is not None:
                        return cached_content
                
                # Render template and cache it
                content = original_render_template(template_name, context)
                if self.cache:
                    self.cache.set(template_path, context, content)
                return content
            
            generator._render_template = cached_render_template
        
        return generator
    
    def create_app_generator(self) -> AppGenerator:
        """Create an app generator instance"""
        generator = AppGenerator()
        if self.cache_enabled and self.cache:
            # Wrap generator with caching functionality
            original_render_template = generator._render_template
            
            def cached_render_template(template_name: str, context: Dict) -> str:
                # Try to get from cache first
                template_path = generator.templates_dir / template_name
                if self.cache:
                    cached_content = self.cache.get(template_path, context)
                    if cached_content is not None:
                        return cached_content
                
                # Render template and cache it
                content = original_render_template(template_name, context)
                if self.cache:
                    self.cache.set(template_path, context, content)
                return content
            
            generator._render_template = cached_render_template
        
        return generator
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if self.cache:
            return self.cache.get_stats()
        return {"cache_enabled": False}
    
    def clear_cache(self) -> None:
        """Clear the template cache"""
        if self.cache:
            self.cache.clear()