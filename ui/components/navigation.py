"""
Navigation sidebar component with polished styling.

Displays available tools in a hierarchical structure.
"""
import ipywidgets as widgets


# Color palette
SIDEBAR_BG = '#2c3e50'  # Dark blue-gray
BUTTON_COLOR = '#3498db'  # Blue
TEXT_COLOR = '#ffffff'  # White


class Navigation:
    """
    Sidebar navigation with tool selection.

    Shows tools from the registry in an organized structure.
    When a tool is clicked, emits an event that the app can handle.
    """

    def __init__(self, registry):
        """
        Initialize navigation.

        Args:
            registry: Tool registry instance
        """
        self.registry = registry
        self.callbacks = []  # List of callback functions
        self.widget = self._build_navigation()

    def _build_navigation(self):
        """
        Build the navigation widget from registry structure.

        Returns:
            ipywidgets.VBox: Navigation widget
        """
        # Get hierarchical structure from registry
        structure = self.registry.get_structure()

        # Create title with styling
        title = widgets.HTML(f"""
            <div style='
                padding: 15px;
                background-color: {SIDEBAR_BG};
                color: {TEXT_COLOR};
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                border-bottom: 2px solid #34495e;
            '>
                Tools
            </div>
        """)

        # Create tool buttons for each category
        tool_widgets = []

        for category, subcategories in structure.items():
            # Category header
            category_header = widgets.HTML(f"""
                <div style='
                    padding: 10px 15px 5px 15px;
                    color: {TEXT_COLOR};
                    font-size: 16px;
                    font-weight: bold;
                    background-color: {SIDEBAR_BG};
                '>
                    {category}
                </div>
            """)
            tool_widgets.append(category_header)

            # Process subcategories
            self._add_subcategory_widgets(
                subcategories,
                f"{category}",
                tool_widgets
            )

        # VBox = Vertical Box (stacked layout)
        return widgets.VBox(
            [title] + tool_widgets,
            layout=widgets.Layout(
                background_color=SIDEBAR_BG
            )
        )

    def _add_subcategory_widgets(self, subcategories, prefix, tool_widgets):
        """
        Recursively add subcategory and tool widgets.

        Args:
            subcategories: Dictionary of subcategories
            prefix: Path prefix (e.g., "RAD")
            tool_widgets: List to append widgets to
        """
        for key, value in subcategories.items():
            if key == '_tools':
                # This is the list of tool names
                for tool_name in value:
                    full_path = f"{prefix}/{tool_name}"
                    tool_button = self._create_tool_button(tool_name, full_path)
                    tool_widgets.append(tool_button)
            else:
                # This is a subcategory
                subcat_header = widgets.HTML(f"""
                    <div style='
                        padding: 8px 15px 5px 25px;
                        color: {TEXT_COLOR};
                        font-size: 14px;
                        font-weight: bold;
                        background-color: {SIDEBAR_BG};
                        opacity: 0.9;
                    '>
                        {key}
                    </div>
                """)
                tool_widgets.append(subcat_header)

                # Recursively process this subcategory
                self._add_subcategory_widgets(
                    value,
                    f"{prefix}/{key}",
                    tool_widgets
                )

    def _create_tool_button(self, tool_name, full_path):
        """
        Create a button for a tool.

        Args:
            tool_name: Display name of the tool
            full_path: Full path (e.g., "RAD/Ingestor/Timeline")

        Returns:
            ipywidgets.Button: Tool button
        """
        # Create a button with the tool name (already properly formatted)
        button = widgets.Button(
            description=tool_name,  # Tool name is already capitalized
            layout=widgets.Layout(
                width='90%',
                margin='2px 0 2px 25px'
            ),
            button_style='info',  # Blue button
            tooltip=f'Open {tool_name}'
        )

        # When clicked, emit the tool_selected event
        def on_click(b):
            self._emit_tool_selected(full_path)

        button.on_click(on_click)

        return button

    def on_tool_selected(self, callback):
        """
        Register a callback for when a tool is selected.

        Args:
            callback: Function to call with tool_path as argument

        Example:
            def handle_tool_click(tool_path):
                print(f"Selected: {tool_path}")

            navigation.on_tool_selected(handle_tool_click)
        """
        self.callbacks.append(callback)

    def _emit_tool_selected(self, tool_path):
        """
        Call all registered callbacks with the tool path.

        Args:
            tool_path: Path of selected tool
        """
        for callback in self.callbacks:
            callback(tool_path)
