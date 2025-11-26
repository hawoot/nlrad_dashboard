"""
Tool UI loader.

Dynamically loads tool UI classes based on tool path.
"""
import importlib
import inspect


class ToolLoader:
    """
    Loads tool UI classes dynamically.

    Given a tool path like "RAD/ingestor/timeline", this will:
    1. Convert to module path: "ui.tools.RAD.ingestor.timeline_ui"
    2. Import the module
    3. Find the UI class (e.g., TimelineUI)
    4. Return the class for instantiation
    """

    def load_tool_ui(self, tool_path):
        """
        Load a tool UI class from its path.

        Args:
            tool_path: Tool path (e.g., "RAD/ingestor/timeline")

        Returns:
            class: Tool UI class (not instantiated)

        Raises:
            ImportError: If tool UI module cannot be found
            ValueError: If no UI class found in module

        Example:
            >>> loader = ToolLoader()
            >>> TimelineUI = loader.load_tool_ui("RAD/ingestor/timeline")
            >>> ui_instance = TimelineUI(executor, "RAD/ingestor/timeline")
        """
        # Convert path to module name
        # "RAD/ingestor/timeline" -> "ui.tools.RAD.ingestor.timeline_ui"
        parts = tool_path.split('/')
        tool_name = parts[-1]  # e.g., "timeline"
        category_path = '/'.join(parts[:-1])  # e.g., "RAD/ingestor"

        # Build module path
        module_path = f"ui.tools.{category_path.replace('/', '.')}.{tool_name}_ui"

        try:
            # Import the module
            # Example: import ui.tools.RAD.ingestor.timeline_ui
            module = importlib.import_module(module_path)

        except ModuleNotFoundError as e:
            raise ImportError(
                f"Could not find UI module for {tool_path}. "
                f"Expected module: {module_path}"
            ) from e

        # Find the UI class in the module
        # By convention, class name should be tool name in TitleCase + "UI"
        # e.g., "timeline" -> "TimelineUI", "force_load" -> "ForceLoadUI"
        expected_class_name = self._get_expected_class_name(tool_name)

        # Look through all classes in the module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Check if class is defined in this module (not imported)
            if obj.__module__ == module.__name__:
                # If name matches expected pattern, return it
                if name == expected_class_name:
                    return obj

        # If we didn't find the expected class, raise error
        raise ValueError(
            f"Could not find UI class '{expected_class_name}' in {module_path}. "
            f"Make sure the class name follows the convention: {expected_class_name}"
        )

    def _get_expected_class_name(self, tool_name):
        """
        Convert tool name to expected class name.

        Args:
            tool_name: Tool name (e.g., "timeline", "force_load")

        Returns:
            str: Expected class name (e.g., "TimelineUI", "ForceLoadUI")

        Examples:
            >>> _get_expected_class_name("timeline")
            "TimelineUI"
            >>> _get_expected_class_name("force_load")
            "ForceLoadUI"
        """
        # Convert snake_case to TitleCase
        # "force_load" -> "ForceLoad"
        title_case = ''.join(word.capitalize() for word in tool_name.split('_'))

        # Append "UI"
        return f"{title_case}UI"
