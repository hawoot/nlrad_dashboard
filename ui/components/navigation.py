"""
Navigation sidebar component.

Displays available tools in a hierarchical structure.
"""
import ipywidgets as widgets


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
        # Structure format:
        # {
        #     'RAD': {
        #         'ingestor': {
        #             '_tools': ['timeline', 'force_load']
        #         }
        #     }
        # }
        structure = self.registry.get_structure()

        # Create title
        title = widgets.HTML("<h2>Tools</h2>")

        # Create tool buttons for each category
        tool_widgets = []

        for category, subcategories in structure.items():
            # Category header
            category_header = widgets.HTML(f"<h3 style='margin: 10px 0 5px 0;'>{category}</h3>")
            tool_widgets.append(category_header)

            # Process subcategories
            self._add_subcategory_widgets(
                subcategories,
                f"{category}",
                tool_widgets
            )

        # VBox = Vertical Box (stacked layout)
        return widgets.VBox([title] + tool_widgets)

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
                subcat_header = widgets.HTML(
                    f"<div style='margin-left: 10px; font-weight: bold;'>{key}</div>"
                )
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
            full_path: Full path (e.g., "RAD/ingestor/timeline")

        Returns:
            ipywidgets.Button: Tool button
        """
        # Create a button with the tool name
        button = widgets.Button(
            description=tool_name.replace('_', ' ').title(),
            layout=widgets.Layout(
                width='90%',
                margin='2px 0 2px 15px'
            ),
            button_style='',  # '', 'success', 'info', 'warning', 'danger'
            tooltip=f'Click to open {tool_name}'
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
