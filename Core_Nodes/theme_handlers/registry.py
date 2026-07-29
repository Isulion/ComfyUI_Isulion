"""
Theme Handler Registry - Declarative registration system for theme handlers.
Replaces fragile `import *` + manual mapping with explicit @register_handler decorator.
"""
from __future__ import annotations
from typing import Dict, Type, Optional
from .base_handler import BaseThemeHandler


_HANDLER_REGISTRY: Dict[str, Type[BaseThemeHandler]] = {}
_HANDLER_INSTANCES: Dict[str, BaseThemeHandler] = {}


def register_handler(internal_name: str):
    """
    Decorator to register a theme handler class.
    
    Args:
        internal_name: Internal identifier (e.g., "cyberpunk", "anime", "s300")
    """
    def decorator(cls: Type[BaseThemeHandler]) -> Type[BaseThemeHandler]:
        if not issubclass(cls, BaseThemeHandler):
            raise TypeError(f"{cls.__name__} must inherit from BaseThemeHandler")
        if internal_name in _HANDLER_REGISTRY:
            raise ValueError(f"Handler already registered for '{internal_name}': {_HANDLER_REGISTRY[internal_name].__name__}")
        _HANDLER_REGISTRY[internal_name] = cls
        return cls
    return decorator


def get_handler_class(internal_name: str) -> Optional[Type[BaseThemeHandler]]:
    """Get handler class by internal name (lazy, no instantiation)."""
    return _HANDLER_REGISTRY.get(internal_name)


def get_handler_instance(internal_name: str, config_manager) -> Optional[BaseThemeHandler]:
    """
    Get or create handler instance (lazy instantiation with caching).
    
    Args:
        internal_name: Internal identifier
        config_manager: ConfigManager instance to pass to handler constructor
        
    Returns:
        Handler instance or None if not registered
    """
    if internal_name in _HANDLER_INSTANCES:
        return _HANDLER_INSTANCES[internal_name]
    
    handler_class = _HANDLER_REGISTRY.get(internal_name)
    if handler_class is None:
        return None
    
    try:
        instance = handler_class(config_manager)
        _HANDLER_INSTANCES[internal_name] = instance
        return instance
    except Exception as e:
        print(f"[ThemeRegistry] Failed to instantiate handler '{internal_name}': {e}")
        return None


def list_handlers() -> Dict[str, Type[BaseThemeHandler]]:
    """Get all registered handler classes (read-only copy)."""
    return dict(_HANDLER_REGISTRY)


def clear_instance_cache() -> None:
    """Clear instantiated handler cache (useful for testing or config reload)."""
    _HANDLER_INSTANCES.clear()


def get_registered_names() -> list[str]:
    """Get list of all registered internal names."""
    return list(_HANDLER_REGISTRY.keys())