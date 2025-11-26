"""
Content area component.

Displays tool UIs dynamically when selected from navigation.
"""
import ipywidgets as widgets
from ui.registry import get_tool_ui_class
from ui.components.error_display import ErrorDisplay


class ContentArea:
    """
    Main content display area.

    Shows welcome message initially, then loads tool UIs dynamically
    when user selects a tool from navigation.
    """

    def __init__(self):
        """Initialize content area with welcome message."""
        self.current_tool_ui = None  # Reference to currently loaded tool UI

        # Create main container (VBox = vertical stacking)
        self.widget = widgets.VBox([
            self._create_welcome_message()
        ])

    def _create_welcome_message(self):
        """
        Create welcome screen shown before any tool is selected.

        Returns:
            ipywidgets.HTML: Welcome message widget
        """
        return widgets.HTML("""
            <div style='padding: 40px; text-align: center;'>
                <h1>Welcome to NLRAD Dashboard</h1>
                <p style='font-size: 16px; color: #666; margin-top: 20px;'>
                    Select a tool from the navigation menu to get started.
                </p>
            </div>
        """)

    def _create_loading_message(self, tool_path):
        """
        Create loading indicator.

        Args:
            tool_path: Path of tool being loaded

        Returns:
            ipywidgets.HTML: Loading message widget
        """
        return widgets.HTML(f"""
            <div style='padding: 40px; text-align: center;'>
                <h2>Loading {tool_path}...</h2>
                <div style='margin-top: 20px; font-size: 24px;'>⏳</div>
            </div>
        """)

    def load_tool(self, tool_path, executor):
        """
        Load and display a tool UI.

        This is called when user clicks a tool in the navigation.

        Args:
            tool_path: Full path to tool (e.g., "RAD/ingestor/timeline")
            executor: Executor instance for running the tool
        """
        # Show loading indicator
        self.widget.children = [self._create_loading_message(tool_path)]

        try:
            # Get the tool UI class from registry
            tool_ui_class = get_tool_ui_class(tool_path)

            # Create instance of the tool UI
            # Pass executor so the UI can execute the tool when user clicks submit
            self.current_tool_ui = tool_ui_class(executor, tool_path)

            # Display the tool UI
            self.widget.children = [
                self._create_tool_header(tool_path),
                self.current_tool_ui.widget
            ]

        except Exception as e:
            # If loading fails, show error
            error_display = ErrorDisplay()
            self.widget.children = [
                error_display.create_error_widget(
                    title="Failed to Load Tool",
                    message=f"Could not load {tool_path}",
                    details=str(e)
                )
            ]

    def _create_tool_header(self, tool_path):
        """
        Create header showing which tool is loaded.

        Args:
            tool_path: Path of loaded tool

        Returns:
            ipywidgets.HTML: Header widget
        """
        # Extract tool name from path (e.g., "timeline" from "RAD/ingestor/timeline")
        tool_name = tool_path.split('/')[-1].replace('_', ' ').title()

        return widgets.HTML(f"""
            <div style='border-bottom: 2px solid #ddd; padding-bottom: 10px; margin-bottom: 20px;'>
                <h2>{tool_name}</h2>
                <p style='color: #666; font-size: 14px;'>{tool_path}</p>
            </div>
        """)
