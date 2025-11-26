"""
Simple tool registry with explicit imports.
"""
from typing import Dict, Type
from backend.core.base_tool import BaseTool
from backend.lib.errors import ToolNotFoundError

# Direct imports of all tools
from backend.tools.RAD.ingestor.timeline_tool import TimelineTool
from backend.tools.RAD.ingestor.force_load_tool import ForceLoadTool


class Registry:
    """
    Simple tool registry with explicit tool mapping.

    All tools are explicitly imported and registered in a dictionary.
    """

    def __init__(self):
        """Initialize registry with explicit tool mapping."""
        # Dictionary mapping tool paths to tool classes
        self._tools: Dict[str, Type[BaseTool]] = {
            'RAD/ingestor/timeline': TimelineTool,
            'RAD/ingestor/force_load': ForceLoadTool,
        }

        # Build navigation structure from tool paths
        self._structure = self._build_structure()

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
        structure = {}

        for path in self._tools.keys():
            parts = path.split('/')

            # Navigate/create structure
            current = structure
            for part in parts[:-1]:  # All but last (tool name)
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Add tool name to _tools list
            if '_tools' not in current:
                current['_tools'] = []
            current['_tools'].append(parts[-1])

        return structure

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
