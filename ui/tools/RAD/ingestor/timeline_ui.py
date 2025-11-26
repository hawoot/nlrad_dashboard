"""
Timeline tool UI.

User interface for querying timeline data by desk and date.
"""
import ipywidgets as widgets
from datetime import datetime, timedelta
import pandas as pd
from IPython.display import display
from ui.components.error_display import ErrorDisplay
from ui.components.dataframe_table import create_dataframe_table
from backend.models.ingestor_timeline import TIMELINE_DESKS


class TimelineUI:
    """
    Timeline tool user interface.

    Shows:
    - Dropdown for desk selection
    - Date picker for date selection
    - Submit button to query data
    - Results table showing timeline data
    """

    def __init__(self, executor, tool_path):
        """
        Initialize Timeline UI.

        Args:
            executor: Executor instance for running the tool
            tool_path: Path to this tool (e.g., "RAD/ingestor/timeline")
        """
        self.executor = executor
        self.tool_path = tool_path
        self.error_display = ErrorDisplay()

        # Create the UI widget
        self.widget = self._build_ui()

    def _build_ui(self):
        """
        Build the complete UI layout.

        Returns:
            ipywidgets.VBox: Main UI container
        """
        # ===== INPUT CONTROLS =====

        # Dropdown for desk selection
        # Options are the timeline desks from model config
        self.desk_dropdown = widgets.Dropdown(
            options=TIMELINE_DESKS,
            value=TIMELINE_DESKS[0],  # Default to first desk
            description='Desk:',
            style={'description_width': '80px'},
            layout=widgets.Layout(width='300px')
        )

        # Date picker widget
        # Defaults to today's date
        self.date_picker = widgets.DatePicker(
            description='Date:',
            value=datetime.now().date(),
            style={'description_width': '80px'},
            layout=widgets.Layout(width='300px')
        )

        # Submit button
        self.submit_button = widgets.Button(
            description='Query Timeline',
            button_style='primary',  # Blue button
            icon='search',
            layout=widgets.Layout(width='200px')
        )

        # Connect button click to handler
        # When user clicks button, _on_submit will be called
        self.submit_button.on_click(self._on_submit)

        # ===== OUTPUT AREA =====

        # Output widget displays dynamic content
        # We'll put results or errors here
        self.output_area = widgets.Output(
            layout=widgets.Layout(
                width='100%',
                border='1px solid #ddd',
                padding='10px',
                margin='10px 0'
            )
        )

        # ===== LAYOUT =====

        # Arrange controls horizontally (HBox)
        controls = widgets.HBox([
            self.desk_dropdown,
            self.date_picker,
            self.submit_button
        ], layout=widgets.Layout(
            padding='10px',
            gap='10px'
        ))

        # Arrange everything vertically (VBox)
        return widgets.VBox([
            self._create_instructions(),
            controls,
            self.output_area
        ])

    def _create_instructions(self):
        """
        Create instructions text.

        Returns:
            ipywidgets.HTML: Instructions widget
        """
        return widgets.HTML("""
            <div style='background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                <h3 style='margin-top: 0;'>Timeline Query</h3>
                <p style='margin-bottom: 0;'>
                    Select a desk and date to query timeline data.
                </p>
            </div>
        """)

    def _on_submit(self, button):
        """
        Handle submit button click.

        This method is called when user clicks the submit button.
        It executes the tool and displays results.

        Args:
            button: Button widget (automatically passed by ipywidgets)
        """
        # Clear previous output
        self.output_area.clear_output()

        # Show loading indicator
        with self.output_area:
            display(widgets.HTML("""
                <div style='text-align: center; padding: 20px;'>
                    <div style='font-size: 24px;'>⏳</div>
                    <div>Loading timeline data...</div>
                </div>
            """))

        # Get form values
        desk = self.desk_dropdown.value
        date = self.date_picker.value

        # Convert date to ISO format string
        date_str = date.isoformat()

        # Execute the tool
        # This calls backend through executor
        result = self.executor.execute(
            user='dashboard_user',  # In production, get from auth
            tool_path=self.tool_path,
            params={
                'desk': desk,
                'date': date_str
            }
        )

        # Clear loading indicator
        self.output_area.clear_output()

        # Display result
        with self.output_area:
            if result.success:
                self._display_success(result.data)
            else:
                self._display_error(result)

    def _display_success(self, data):
        """
        Display successful results.

        Args:
            data: Result data (dictionary with 'records' key)
        """
        # Extract records from result
        records = data.get('records', data)

        # Show success message
        display(self.error_display.create_success_widget(
            f"Found {len(records)} timeline records"
        ))

        # Convert data to DataFrame and display with reusable component
        df = pd.DataFrame(records)
        table_widget = create_dataframe_table(df, title="Timeline Results")
        display(table_widget)

    def _display_error(self, result):
        """
        Display error message.

        Args:
            result: Result object with error info
        """
        display(self.error_display.create_error_widget(
            title=result.error_type or "Error",
            message=result.user_message or result.error_message,
            details=result.traceback
        ))
