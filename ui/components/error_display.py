"""
Error display component.

Provides consistent error rendering across the application.
"""
import ipywidgets as widgets


class ErrorDisplay:
    """
    Helper class for displaying errors in a user-friendly format.

    Creates styled error widgets with title, message, and optional details.
    """

    def create_error_widget(self, title, message, details=None):
        """
        Create an error display widget.

        Args:
            title: Error title (e.g., "Validation Error")
            message: User-friendly error message
            details: Optional technical details (stack trace, etc.)

        Returns:
            ipywidgets.VBox: Styled error widget
        """
        # Main error message with red styling
        error_html = f"""
            <div style='
                padding: 20px;
                border-left: 4px solid #d32f2f;
                background-color: #ffebee;
                margin: 20px 0;
            '>
                <h3 style='color: #d32f2f; margin: 0 0 10px 0;'>
                    ⚠️ {title}
                </h3>
                <p style='margin: 0; color: #333;'>
                    {message}
                </p>
            </div>
        """

        widgets_list = [widgets.HTML(error_html)]

        # Add collapsible details section if provided
        if details:
            details_html = widgets.HTML(f"""
                <div style='
                    padding: 10px;
                    background-color: #f5f5f5;
                    border: 1px solid #ddd;
                    font-family: monospace;
                    font-size: 12px;
                    white-space: pre-wrap;
                    max-height: 200px;
                    overflow-y: auto;
                '>
{details}
                </div>
            """)

            # Accordion widget makes details collapsible
            accordion = widgets.Accordion(children=[details_html])
            accordion.set_title(0, 'Technical Details')
            accordion.selected_index = None  # Start collapsed

            widgets_list.append(accordion)

        return widgets.VBox(widgets_list)

    def create_success_widget(self, message):
        """
        Create a success message widget.

        Args:
            message: Success message to display

        Returns:
            ipywidgets.HTML: Styled success widget
        """
        return widgets.HTML(f"""
            <div style='
                padding: 20px;
                border-left: 4px solid #388e3c;
                background-color: #e8f5e9;
                margin: 20px 0;
            '>
                <h3 style='color: #388e3c; margin: 0 0 10px 0;'>
                    ✓ Success
                </h3>
                <p style='margin: 0; color: #333;'>
                    {message}
                </p>
            </div>
        """)
