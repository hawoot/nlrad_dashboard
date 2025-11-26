"""
Shared resource management.

Provides lazy-loading and caching for expensive resources like
database connections, configuration files, etc.
"""
from typing import Dict, Any, Callable


class ModelLoader:
    """
    Singleton resource loader with lazy initialization.

    Use this to share expensive resources across tool executions:
    - Database connections
    - Configuration files
    - Heavy data structures
    - Cache instances

    Example:
        loader = get_model_loader()
        db = loader.get("db", lambda: create_db_connection())
    """

    def __init__(self):
        """Initialize empty cache."""
        self._cache = {}

    def get(self, key, factory):
        """
        Get or create a resource.

        If the resource doesn't exist in cache, calls factory() to create it
        and stores it for future use.

        Args:
            key: Unique identifier for this resource
            factory: Callable that creates the resource (no arguments)

        Returns:
            The cached or newly created resource

        Example:
            db = loader.get("db", lambda: psycopg2.connect(conn_string))
        """
        if key not in self._cache:
            self._cache[key] = factory()
        return self._cache[key]

    def set(self, key, value):
        """
        Explicitly set a cached resource.

        Useful for testing or manual resource management.

        Args:
            key: Resource identifier
            value: Resource to cache
        """
        self._cache[key] = value

    def clear(self, key=None):
        """
        Clear cached resources.

        Args:
            key: Specific resource to clear. If None, clears all resources.
        """
        if key is None:
            self._cache.clear()
        elif key in self._cache:
            del self._cache[key]

    def has(self, key):
        """
        Check if a resource is cached.

        Args:
            key: Resource identifier

        Returns:
            True if resource is cached
        """
        return key in self._cache


# Global singleton instance
_model_loader = None


def get_model_loader():
    """
    Get the global ModelLoader instance.

    Returns:
        Singleton ModelLoader instance
    """
    global _model_loader
    if _model_loader is None:
        _model_loader = ModelLoader()
    return _model_loader
