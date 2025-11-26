"""
Force Load tool UI.

User interface for managing force load configurations with editable tables.
"""
import ipywidgets as widgets
from IPython.display import display
import pandas as pd
from ui.components.error_display import ErrorDisplay
from backend.models.ingestor_force import FORCE_LOAD_TABLES


class ForceLoadUI:
    """
    Force Load tool user interface.

    Shows:
    - Dropdown for table selection
    - Editable table for configuration
    - Add/Remove row buttons
    - Submit button to save changes
    """

    def __init__(self, executor, tool_path):
        """
        Initialize Force Load UI.

        Args:
            executor: Executor instance for running the tool
            tool_path: Path to this tool
        """
        self.executor = executor
        self.tool_path = tool_path
        self.error_display = ErrorDisplay()

        # Current table data (list of dicts)
        self.current_data = []
        self.current_table_name = None

        # Create the UI widget
        self.widget = self._build_ui()

    def _build_ui(self):
        """
        Build the complete UI layout.

        Returns:
            ipywidgets.VBox: Main UI container
        """
        # ===== TABLE SELECTION =====

        # Dropdown for table selection
        table_names = list(FORCE_LOAD_TABLES.keys())
        self.table_dropdown = widgets.Dropdown(
            options=table_names,
            value=table_names[0],
            description='Table:',
            style={'description_width': '80px'},
            layout=widgets.Layout(width='400px')
        )

        # When user changes table, reload data
        self.table_dropdown.observe(self._on_table_changed, names='value')

        # Load table button
        self.load_button = widgets.Button(
            description='Load Table',
            button_style='info',
            icon='download',
            layout=widgets.Layout(width='150px')
        )
        self.load_button.on_click(self._on_load_table)

        # ===== TABLE EDITOR =====

        # Container for the editable table
        # This will be populated when user loads a table
        self.table_container = widgets.VBox([
            widgets.HTML("""
                <div style='padding: 40px; text-align: center; color: #666;'>
                    Select a table and click "Load Table" to begin editing.
                </div>
            """)
        ])

        # ===== ACTION BUTTONS =====

        self.add_row_button = widgets.Button(
            description='Add Row',
            button_style='success',
            icon='plus',
            layout=widgets.Layout(width='120px'),
            disabled=True  # Disabled until table loaded
        )
        self.add_row_button.on_click(self._on_add_row)

        self.remove_row_button = widgets.Button(
            description='Remove Last Row',
            button_style='warning',
            icon='minus',
            layout=widgets.Layout(width='160px'),
            disabled=True
        )
        self.remove_row_button.on_click(self._on_remove_row)

        self.submit_button = widgets.Button(
            description='Submit Changes',
            button_style='primary',
            icon='check',
            layout=widgets.Layout(width='160px'),
            disabled=True
        )
        self.submit_button.on_click(self._on_submit)

        # ===== OUTPUT AREA =====

        self.output_area = widgets.Output(
            layout=widgets.Layout(
                width='100%',
                border='1px solid #ddd',
                padding='10px',
                margin='10px 0'
            )
        )

        # ===== LAYOUT =====

        header = widgets.HBox([
            self.table_dropdown,
            self.load_button
        ], layout=widgets.Layout(gap='10px', padding='10px'))

        action_buttons = widgets.HBox([
            self.add_row_button,
            self.remove_row_button,
            self.submit_button
        ], layout=widgets.Layout(gap='10px', padding='10px'))

        return widgets.VBox([
            self._create_instructions(),
            header,
            self.table_container,
            action_buttons,
            self.output_area
        ])

    def _create_instructions(self):
        """Create instructions text."""
        return widgets.HTML("""
            <div style='background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                <h3 style='margin-top: 0;'>Force Load Configuration</h3>
                <p style='margin-bottom: 0;'>
                    Select a table, load the default configuration, edit values as needed,
                    add or remove rows, then submit your changes.
                </p>
            </div>
        """)

    def _on_table_changed(self, change):
        """Handle table dropdown change."""
        # Reset table container when selection changes
        self.table_container.children = [widgets.HTML("""
            <div style='padding: 40px; text-align: center; color: #666;'>
                Click "Load Table" to load this configuration.
            </div>
        """)]
        self.current_data = []
        self.current_table_name = None
        self._disable_buttons()

    def _on_load_table(self, button):
        """Load the selected table's default configuration."""
        self.output_area.clear_output()

        table_name = self.table_dropdown.value

        # Execute tool to get default config
        result = self.executor.execute(
            user='dashboard_user',
            tool_path=self.tool_path,
            params={
                'table_name': table_name,
                'action': 'get_default'
            }
        )

        if result.success:
            self.current_data = result.data['config']
            self.current_table_name = table_name
            self._render_table()
            self._enable_buttons()
        else:
            with self.output_area:
                display(self.error_display.create_error_widget(
                    title="Failed to Load Table",
                    message=result.user_message or result.error_message,
                    details=result.traceback
                ))

    def _render_table(self):
        """Render the editable table from current_data."""
        if not self.current_data:
            return

        # Get table schema
        schema = FORCE_LOAD_TABLES[self.current_table_name]
        # Extract columns from the data keys (since we removed explicit column definitions)
        columns = [{'name': key} for key in ['configName', 'key', 'group']]

        # Create input widgets for each cell
        # We'll use a grid layout
        table_widgets = []

        # Header row
        header_widgets = []
        for col in columns:
            required_badge = " *" if col.get('required') else ""
            header_widgets.append(widgets.HTML(
                f"<b>{col['name']}{required_badge}</b>",
                layout=widgets.Layout(width='200px', padding='5px')
            ))
        table_widgets.append(widgets.HBox(header_widgets))

        # Data rows
        for row_idx, row_data in enumerate(self.current_data):
            row_widgets = []
            for col in columns:
                col_name = col['name']
                value = row_data.get(col_name, '')

                # Create text input for each cell
                text_input = widgets.Text(
                    value=str(value),
                    layout=widgets.Layout(width='200px'),
                    continuous_update=False  # Only update on blur/enter
                )

                # Store reference to update data when changed
                text_input.row_idx = row_idx
                text_input.col_name = col_name
                text_input.observe(self._on_cell_changed, names='value')

                row_widgets.append(text_input)

            table_widgets.append(widgets.HBox(row_widgets))

        # Show table info
        info_html = widgets.HTML(f"""
            <div style='padding: 10px; background-color: #e3f2fd; margin-bottom: 10px;'>
                <b>Table:</b> {self.current_table_name}<br>
                <b>Description:</b> {schema['description']}<br>
                <b>Rows:</b> {len(self.current_data)}
            </div>
        """)

        self.table_container.children = [
            info_html,
            widgets.VBox(table_widgets, layout=widgets.Layout(
                border='1px solid #ddd',
                padding='10px'
            ))
        ]

    def _on_cell_changed(self, change):
        """Handle cell value change."""
        widget = change['owner']
        row_idx = widget.row_idx
        col_name = widget.col_name
        new_value = change['new']

        # Update data
        self.current_data[row_idx][col_name] = new_value

    def _on_add_row(self, button):
        """Add a new empty row."""
        if not self.current_table_name:
            return

        # Create empty row with standard columns
        new_row = {'configName': '', 'key': '', 'group': ''}
        self.current_data.append(new_row)

        # Re-render table
        self._render_table()

    def _on_remove_row(self, button):
        """Remove the last row."""
        if self.current_data:
            self.current_data.pop()
            self._render_table()

    def _on_submit(self, button):
        """Submit the changes."""
        self.output_area.clear_output()

        if not self.current_data:
            with self.output_area:
                display(self.error_display.create_error_widget(
                    title="No Data",
                    message="Please load a table first."
                ))
            return

        # Show loading
        with self.output_area:
            display(widgets.HTML("""
                <div style='text-align: center; padding: 20px;'>
                    <div style='font-size: 24px;'>⏳</div>
                    <div>Submitting changes...</div>
                </div>
            """))

        # Execute tool to save config
        result = self.executor.execute(
            user='dashboard_user',
            tool_path=self.tool_path,
            params={
                'table_name': self.current_table_name,
                'action': 'save',
                'config': self.current_data
            }
        )

        self.output_area.clear_output()

        with self.output_area:
            if result.success:
                display(self.error_display.create_success_widget(
                    f"Successfully saved {len(self.current_data)} rows for {self.current_table_name}"
                ))
            else:
                display(self.error_display.create_error_widget(
                    title=result.error_type or "Error",
                    message=result.user_message or result.error_message,
                    details=result.traceback
                ))

    def _enable_buttons(self):
        """Enable action buttons."""
        self.add_row_button.disabled = False
        self.remove_row_button.disabled = False
        self.submit_button.disabled = False

    def _disable_buttons(self):
        """Disable action buttons."""
        self.add_row_button.disabled = True
        self.remove_row_button.disabled = True
        self.submit_button.disabled = True
