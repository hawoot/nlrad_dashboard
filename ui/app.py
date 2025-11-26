"""
Main application entry point.

This creates the dashboard UI using ipywidgets and Voila.
"""
import ipywidgets as widgets
from backend.server import initialize_backend
from backend.core.registry import get_registry
from backend.core.executor import get_executor
from ui.components.navigation import Navigation
from ui.components.content_area import ContentArea


def create_app():
    """
    Create and return the main application widget.

    This is the ONLY function called from the notebook.

    Returns:
        ipywidgets.Widget: Main application layout
    """
    # =========================================================================
    # STEP 1: Initialize Backend
    # =========================================================================
    # This sets up logging, discovers tools, and prepares the executor
    initialize_backend()

    # Get singleton instances
    registry = get_registry()
    executor = get_executor()

    # =========================================================================
    # STEP 2: Create UI Components
    # =========================================================================
    # Navigation sidebar (left) - shows available tools
    navigation = Navigation(registry)

    # Content area (right) - displays tool UIs
    content_area = ContentArea()

    # =========================================================================
    # STEP 3: Wire Navigation to Content
    # =========================================================================
    # When user clicks a tool in navigation, load its UI in the content area
    def on_tool_selected(tool_path):
        content_area.load_tool(tool_path, executor)

    navigation.on_tool_selected(on_tool_selected)

    # =========================================================================
    # STEP 4: Create Main Layout
    # =========================================================================
    # HBox = Horizontal Box (side-by-side layout)
    # Navigation on left (20% width), Content on right (80% width)
    main_layout = widgets.HBox([
        navigation.widget,
        content_area.widget
    ])

    # Style the layout
    main_layout.layout = widgets.Layout(
        width='100%',
        height='800px'
    )

    navigation.widget.layout = widgets.Layout(
        width='20%',
        height='800px',
        border='1px solid #ddd',
        padding='10px'
    )

    content_area.widget.layout = widgets.Layout(
        width='80%',
        height='800px',
        padding='20px'
    )

    return main_layout
