"""
Force Load tool UI.

User interface for managing force load configurations with editable tables.
"""
import ipywidgets as widgets
from IPython.display import display
import pandas as pd
from ui.components.error_display import ErrorDisplay
from ui.components.dataframe_table import create_dataframe_table
from backend.models.ingestor_force import FORCE_LOAD_TABLES


# Color palette
BUTTON_PRIMARY = '#3498db'
BUTTON_SUCCESS = '#27ae60'
BUTTON_WARNING = '#e67e22'
BUTTON_DANGER = '#e74c3c'
BG_LIGHT = '#f5f5f5'
BORDER_COLOR = '#ddd'


class ForceLoadUI:
    """
    Force Load tool user interface.

    Shows:
    - Dropdown for table selection
    - Editable table for configuration
    - Add row button and per-row delete buttons
    - Dry Run checkbox (default checked)
    - Submit button with dynamic text
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
        self.table_container = widgets.VBox([
            widgets.HTML(f"""
                <div style='padding: 40px; text-align: center; color: #666;'>
                    Select a table and click "Load Table" to begin editing.
                </div>
            """)
        ])

        # ===== ACTION BUTTONS =====

        # Dry Run checkbox (default checked)
        self.dry_run_checkbox = widgets.Checkbox(
            value=True,
            description='Dry Run',
            indent=False,
            layout=widgets.Layout(width='120px'),
            disabled=True  # Disabled until table loaded
        )
        self.dry_run_checkbox.observe(self._on_dry_run_changed, names='value')

        self.add_row_button = widgets.Button(
            description='Add Row',
            button_style='success',
            icon='plus',
            layout=widgets.Layout(width='120px'),
            disabled=True  # Disabled until table loaded
        )
        self.add_row_button.on_click(self._on_add_row)

        self.submit_button = widgets.Button(
            description='Dry Run',  # Default text
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
                border=f'1px solid {BORDER_COLOR}',
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
            self.dry_run_checkbox,
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
        return widgets.HTML(f"""
            <div style='background-color: {BG_LIGHT}; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                <h3 style='margin-top: 0;'>Force Load Configuration</h3>
                <p style='margin-bottom: 0;'>
                    Select a table, load the default configuration, edit values as needed,
                    add or remove rows, then submit. Use "Dry Run" to preview results without saving.
                </p>
            </div>
        """)

    def _on_dry_run_changed(self, change):
        """Update button text when dry run checkbox changes."""
        if change['new']:
            self.submit_button.description = 'Dry Run'
        else:
            self.submit_button.description = 'Force Load Run'

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
        columns = ['configName', 'key', 'group']

        # Create input widgets for each row
        table_widgets = []

        # Header row
        header_widgets = [
            widgets.HTML(
                "<b>configName</b>",
                layout=widgets.Layout(width='200px', padding='5px')
            ),
            widgets.HTML(
                "<b>key</b>",
                layout=widgets.Layout(width='200px', padding='5px')
            ),
            widgets.HTML(
                "<b>group</b>",
                layout=widgets.Layout(width='200px', padding='5px')
            ),
            widgets.HTML(
                "<b>Actions</b>",
                layout=widgets.Layout(width='80px', padding='5px')
            )
        ]
        table_widgets.append(widgets.HBox(header_widgets))

        # Data rows with per-row delete buttons
        for row_idx, row_data in enumerate(self.current_data):
            row_widgets = []

            # Input fields for each column
            for col_name in columns:
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

            # Delete button for this row
            delete_button = widgets.Button(
                description='✗',
                button_style='danger',
                layout=widgets.Layout(width='60px'),
                tooltip=f'Delete row {row_idx + 1}'
            )
            delete_button.row_idx = row_idx
            delete_button.on_click(self._on_delete_row)

            row_widgets.append(delete_button)

            table_widgets.append(widgets.HBox(row_widgets, layout=widgets.Layout(margin='2px 0')))

        # Show table info
        info_html = widgets.HTML(f"""
            <div style='padding: 10px; background-color: #e3f2fd; margin-bottom: 10px; border-radius: 5px;'>
                <b>Table:</b> {self.current_table_name}<br>
                <b>Description:</b> {schema['description']}<br>
                <b>Rows:</b> {len(self.current_data)}
            </div>
        """)

        self.table_container.children = [
            info_html,
            widgets.VBox(table_widgets, layout=widgets.Layout(
                border=f'1px solid {BORDER_COLOR}',
                padding='10px',
                background_color='white'
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

    def _on_delete_row(self, button):
        """Delete a specific row."""
        row_idx = button.row_idx

        if 0 <= row_idx < len(self.current_data):
            self.current_data.pop(row_idx)
            self._render_table()

    def _on_submit(self, button):
        """Submit the changes (either dry run or actual force load)."""
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
            is_dry_run = self.dry_run_checkbox.value
            action_text = "Running dry run" if is_dry_run else "Executing force load"
            display(widgets.HTML(f"""
                <div style='text-align: center; padding: 20px;'>
                    <div style='font-size: 24px;'>⏳</div>
                    <div>{action_text}...</div>
                </div>
            """))

        # Execute tool
        result = self.executor.execute(
            user='dashboard_user',
            tool_path=self.tool_path,
            params={
                'table_name': self.current_table_name,
                'action': 'force_load',
                'config': self.current_data,
                'dry_run': self.dry_run_checkbox.value
            }
        )

        self.output_area.clear_output()

        with self.output_area:
            if result.success:
                self._display_success(result.data, is_dry_run=self.dry_run_checkbox.value)
            else:
                display(self.error_display.create_error_widget(
                    title=result.error_type or "Error",
                    message=result.user_message or result.error_message,
                    details=result.traceback
                ))

    def _display_success(self, data, is_dry_run=True):
        """
        Display successful results.

        Args:
            data: Result data containing DataFrame records
            is_dry_run: Whether this was a dry run
        """
        # Extract records from result
        records = data.get('records', data)

        # Success message
        mode_text = "Dry run" if is_dry_run else "Force load"
        display(self.error_display.create_success_widget(
            f"{mode_text} completed successfully - {len(records)} records"
        ))

        # Convert to DataFrame and display with reusable component
        df = pd.DataFrame(records)
        title = f"{'Dry Run' if is_dry_run else 'Force Load'} Results"
        table_widget = create_dataframe_table(df, title=title)
        display(table_widget)

    def _enable_buttons(self):
        """Enable action buttons."""
        self.add_row_button.disabled = False
        self.dry_run_checkbox.disabled = False
        self.submit_button.disabled = False

    def _disable_buttons(self):
        """Disable action buttons."""
        self.add_row_button.disabled = True
        self.dry_run_checkbox.disabled = True
        self.submit_button.disabled = True
