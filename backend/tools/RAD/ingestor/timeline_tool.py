"""
Timeline query tool.

Allows users to query ingestor timeline data by desk and date.
"""
from datetime import datetime
from backend.core.base_tool import BaseTool, ExecutionContext
from backend.models.ingestor_timeline import IngestorTimelineModel
from backend.lib.errors import ParameterValidationError
from config.settings import RAD_TIMELINE_DESKS


class TimelineTool(BaseTool):
    """
    Query ingestor timeline data.

    Inputs:
        - desk: Desk name (Options, Exotics, Inflation, LDFX, FXG)
        - date: Query date (ISO format string)

    Returns:
        Dictionary with timeline data and analytics
    """

    category = "RAD/ingestor"
    name = "timeline"
    description = "Query ingestor timeline data by desk and date"

    def run(self, context, desk, date):
        """
        Execute timeline query.

        Args:
            context: Execution context
            desk: Desk name
            date: Date string (YYYY-MM-DD)

        Returns:
            Dictionary with records, summary, and dataframe

        Raises:
            ParameterValidationError: If parameters are invalid
        """
        # Validate desk
        context.logger.info(f"Validating parameters: desk={desk}, date={date}")

        if desk not in RAD_TIMELINE_DESKS:
            raise ParameterValidationError(
                f"Invalid desk '{desk}'. Must be one of: {RAD_TIMELINE_DESKS}",
                user_message=f"Please select a valid desk: {', '.join(RAD_TIMELINE_DESKS)}"
            )

        # Validate and parse date
        try:
            date_obj = datetime.fromisoformat(date)
        except ValueError as e:
            raise ParameterValidationError(
                f"Invalid date format: {e}",
                user_message="Please provide date in YYYY-MM-DD format"
            )

        # Log validated parameters
        context.logger.info(
            f"Parameters validated successfully",
            extra={'desk': desk, 'date': date}
        )

        # Create model and fetch data
        context.logger.info("Fetching timeline data")
        model = IngestorTimelineModel()
        df = model.get_timeline_data(desk, date_obj)

        context.logger.info(
            f"Retrieved {len(df)} timeline records",
            extra={'record_count': len(df)}
        )

        # Process data
        result = model.process_timeline_data(df)

        context.logger.info("Timeline processing complete")

        return result
