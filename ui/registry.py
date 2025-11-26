"""
UI Tool Registry.

Maps tool paths to UI classes. This keeps UI and backend separate
while providing explicit control over tool-to-UI mapping.
"""
from typing import Dict, Type

# Import UI classes
from ui.tools.RAD.ingestor.timeline_ui import TimelineUI
from ui.tools.RAD.ingestor.force_load_ui import ForceLoadUI


# Map tool paths to UI classes
TOOL_UI_MAP: Dict[str, Type] = {
    'RAD/Ingestor/Timeline': TimelineUI,
    'RAD/Ingestor/Force Load': ForceLoadUI,
}


def get_tool_ui_class(tool_path: str):
    """
    Get the UI class for a tool path.

    Args:
        tool_path: Tool path (e.g., "RAD/Ingestor/Timeline")

    Returns:
        UI class for the tool

    Raises:
        KeyError: If tool path not found
    """
    if tool_path not in TOOL_UI_MAP:
        raise KeyError(
            f"No UI class registered for tool '{tool_path}'. "
            f"Available tools: {list(TOOL_UI_MAP.keys())}"
        )
    return TOOL_UI_MAP[tool_path]


def get_available_tools():
    """
    Get list of all tools with UI registered.

    Returns:
        List of tool paths
    """
    return list(TOOL_UI_MAP.keys())
