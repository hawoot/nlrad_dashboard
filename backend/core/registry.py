"""
Tool registry with auto-discovery.

Walks the backend/tools directory tree and automatically registers
all classes that inherit from BaseTool.
"""
import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Dict, List, Type, Any
from backend.core.base_tool import BaseTool
from backend.lib.errors import ToolNotFoundError


class Registry:
    """
    Tool registry with auto-discovery.

    Discovers all tools in backend/tools/ and provides:
    - Tool lookup by path
    - Hierarchical structure for navigation
    - Category/subcategory queries
    """

    def __init__(self):
        """Initialize and discover tools."""
        self._tools = {}
        self._structure = {}
        self._discover_tools()

    def _discover_tools(self):
        """
        Walk the backend/tools directory and discover all tools.

        Process:
        1. Find all Python modules in backend/tools/
        2. Import each module
        3. Find classes inheriting from BaseTool
        4. Register them with their full path
        5. Build hierarchical structure
        """
        # Get backend/tools directory
        tools_dir = Path(__file__).parent.parent / 'tools'
        if not tools_dir.exists():
            return

        # Walk the package tree
        import backend.tools as tools_package
        self._walk_package(tools_package, tools_dir)

        # Build navigation structure
        self._build_structure()

    def _walk_package(self, package, package_path):
        """
        Recursively walk a package and import all modules.

        Args:
            package: Package object
            package_path: Filesystem path to package
        """
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=[str(package_path)],
            prefix=package.__name__ + '.'
        ):
            try:
                # Import the module
                module = importlib.import_module(modname)

                # Find BaseTool subclasses
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (obj != BaseTool and
                        issubclass(obj, BaseTool) and
                        obj.__module__ == modname):
                        self._register_tool(obj)
            except Exception as e:
                # Log but don't fail on import errors
                print(f"Warning: Failed to import {modname}: {e}")

    def _register_tool(self, tool_class):
        """
        Register a tool class.

        Args:
            tool_class: Tool class to register

        Raises:
            ValueError: If tool path already registered
        """
        # Instantiate to get path (validates category/name)
        try:
            tool_instance = tool_class()
            path = tool_instance.full_path
        except Exception as e:
            print(f"Warning: Cannot instantiate {tool_class.__name__}: {e}")
            return

        # Check for duplicates
        if path in self._tools:
            raise ValueError(
                f"Duplicate tool path '{path}': "
                f"{self._tools[path].__name__} and {tool_class.__name__}"
            )

        # Register
        self._tools[path] = tool_class
        print(f"Registered tool: {path} ({tool_class.__name__})")

    def _build_structure(self):
        """
        Build hierarchical structure for navigation.

        Converts flat tool paths into nested dictionary:
        {
            'RAD': {
                'ingestor': {
                    '_tools': ['timeline', 'force_load']
                }
            }
        }
        """
        self._structure = {}

        for path in self._tools.keys():
            parts = path.split('/')

            # Navigate/create structure
            current = self._structure
            for part in parts[:-1]:  # All but last (tool name)
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Add tool name to _tools list
            if '_tools' not in current:
                current['_tools'] = []
            current['_tools'].append(parts[-1])

    def get_tool(self, path):
        """
        Get a tool instance by path.

        Args:
            path: Tool path (e.g., "RAD/ingestor/timeline")

        Returns:
            Instantiated tool object

        Raises:
            ToolNotFoundError: If path doesn't exist
        """
        if path not in self._tools:
            raise ToolNotFoundError(
                f"Tool not found: {path}. "
                f"Available tools: {list(self._tools.keys())}"
            )

        # Instantiate and return
        return self._tools[path]()

    def get_structure(self):
        """
        Get the full hierarchical structure.

        Returns:
            Nested dictionary of categories and tools
        """
        return self._structure

    def get_categories(self):
        """
        Get top-level categories.

        Returns:
            List of category names (e.g., ["RAD", "DD"])
        """
        return list(self._structure.keys())

    def list_all_tools(self):
        """
        Get list of all tool paths.

        Returns:
            List of tool paths
        """
        return list(self._tools.keys())


# Global singleton
_registry = None


def get_registry():
    """
    Get the global Registry instance.

    Returns:
        Singleton Registry instance
    """
    global _registry
    if _registry is None:
        _registry = Registry()
    return _registry
