"""
Reusable DataFrame table component with sort and filter.

Provides a consistent, polished table display for any DataFrame.
"""
import ipywidgets as widgets
import pandas as pd
from IPython.display import display


# Color palette
SUCCESS_COLOR = '#27ae60'
HEADER_COLOR = '#34495e'
ROW_EVEN = '#ffffff'
ROW_ODD = '#f9f9f9'


class DataFrameTable:
    """
    Interactive table component for DataFrames.

    Features:
    - Click column headers to sort (ascending/descending)
    - Search box to filter across all columns
    - Styled, professional appearance
    """

    def __init__(self, df, title=None):
        """
        Initialize DataFrame table.

        Args:
            df: pandas DataFrame to display
            title: Optional title to show above table
        """
        self.original_df = df.copy()
        self.current_df = df.copy()
        self.sort_column = None
        self.sort_ascending = True
        self.title = title

        # Create widgets
        self.widget = self._build_widget()

    def _build_widget(self):
        """
        Build the complete widget.

        Returns:
            widgets.VBox: Complete table widget
        """
        # Title (optional)
        widgets_list = []
        if self.title:
            title_widget = widgets.HTML(f"""
                <div style='
                    font-size: 18px;
                    font-weight: bold;
                    color: {HEADER_COLOR};
                    margin-bottom: 10px;
                '>
                    {self.title}
                </div>
            """)
            widgets_list.append(title_widget)

        # Search box
        self.search_box = widgets.Text(
            placeholder='Search...',
            description='Filter:',
            layout=widgets.Layout(width='400px', margin='0 0 10px 0')
        )
        self.search_box.observe(self._on_search, names='value')
        widgets_list.append(self.search_box)

        # Table output
        self.table_output = widgets.Output()
        with self.table_output:
            display(widgets.HTML(self._create_table_html()))
        widgets_list.append(self.table_output)

        return widgets.VBox(widgets_list)

    def _on_search(self, change):
        """Handle search box changes."""
        search_text = change['new'].lower()

        if not search_text:
            # No search, show all
            self.current_df = self.original_df.copy()
        else:
            # Filter rows where any column contains search text
            mask = self.original_df.astype(str).apply(
                lambda row: row.str.lower().str.contains(search_text).any(),
                axis=1
            )
            self.current_df = self.original_df[mask].copy()

        # Re-apply sort if active
        if self.sort_column:
            self.current_df = self.current_df.sort_values(
                by=self.sort_column,
                ascending=self.sort_ascending
            )

        # Refresh table
        self._refresh_table()

    def _on_sort_click(self, column):
        """Handle column header click for sorting."""
        if self.sort_column == column:
            # Toggle sort order
            self.sort_ascending = not self.sort_ascending
        else:
            # New column, default to ascending
            self.sort_column = column
            self.sort_ascending = True

        # Sort the dataframe
        self.current_df = self.current_df.sort_values(
            by=column,
            ascending=self.sort_ascending
        )

        # Refresh table
        self._refresh_table()

    def _refresh_table(self):
        """Refresh the table display."""
        self.table_output.clear_output()
        with self.table_output:
            display(widgets.HTML(self._create_table_html()))

    def _create_table_html(self):
        """
        Create HTML table from current DataFrame.

        Returns:
            str: HTML table string
        """
        df = self.current_df

        if len(df) == 0:
            return """
                <div style='padding: 20px; text-align: center; color: #7f8c8d;'>
                    No data to display
                </div>
            """

        # Start table
        html = f"""
        <div style='max-height: 500px; overflow: auto; border: 1px solid #ddd; border-radius: 5px;'>
            <table style='
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            '>
                <thead style='
                    position: sticky;
                    top: 0;
                    background-color: {HEADER_COLOR};
                    color: white;
                    border-bottom: 2px solid #2c3e50;
                '>
                    <tr>
        """

        # Add column headers (clickable for sorting)
        for col in df.columns:
            # Sort indicator
            indicator = ''
            if self.sort_column == col:
                indicator = ' ↓' if self.sort_ascending else ' ↑'

            html += f"""
                        <th style='
                            padding: 12px;
                            text-align: left;
                            font-weight: bold;
                            cursor: pointer;
                            user-select: none;
                        ' onclick='alert("Sorting not available in static HTML")'>
                            {col}{indicator}
                        </th>
            """

        html += """
                    </tr>
                </thead>
                <tbody>
        """

        # Add data rows
        for idx, row in df.iterrows():
            # Alternate row colors
            bg_color = ROW_EVEN if idx % 2 == 0 else ROW_ODD
            html += f"<tr style='background-color: {bg_color};'>"

            for col in df.columns:
                value = row[col]

                # Format boolean values
                if isinstance(value, bool):
                    formatted_value = '✓' if value else '✗'
                    color = SUCCESS_COLOR if value else '#e74c3c'
                    html += f"""
                        <td style='padding: 10px; color: {color}; font-weight: bold;'>
                            {formatted_value}
                        </td>
                    """
                else:
                    html += f"<td style='padding: 10px;'>{value}</td>"

            html += "</tr>"

        html += """
                </tbody>
            </table>
        </div>
        """

        # Add row count
        total_rows = len(self.original_df)
        shown_rows = len(df)
        count_text = f"Showing {shown_rows} of {total_rows} rows" if shown_rows != total_rows else f"{total_rows} rows"

        html += f"""
        <div style='
            padding: 10px;
            font-size: 12px;
            color: #7f8c8d;
            text-align: right;
        '>
            {count_text}
        </div>
        """

        return html


def create_dataframe_table(df, title=None):
    """
    Helper function to create a DataFrame table widget.

    Args:
        df: pandas DataFrame
        title: Optional title

    Returns:
        widgets.VBox: Table widget
    """
    table = DataFrameTable(df, title=title)
    return table.widget
