"""
Force load tool.

Allows users to force load configuration data to predefined tables.
"""
from typing import List, Dict, Any
from backend.core.base_tool import BaseTool, ExecutionContext
from backend.models.ingestor_force import IngestorForceModel
from backend.lib.errors import ParameterValidationError
from config.settings import RAD_FORCE_LOAD_TABLES


class ForceLoadTool(BaseTool):
    """
    Force load configuration data.

    Inputs:
        - table_name: Predefined table name
        - config_data: List of configuration dictionaries
                      Each dict has keys defined in table schema

    Returns:
        Dictionary with success status and details
    """

    category = "RAD/ingestor"
    name = "force_load"
    description = "Force load configuration data to predefined tables"

    def run(
        self,
        context,
        table_name,
        config_data
    ):
        """
        Execute force load.

        Args:
            context: Execution context
            table_name: Table to load
            config_data: Configuration data

        Returns:
            Dictionary with result details

        Raises:
            ParameterValidationError: If parameters are invalid
        """
        # Validate table name
        context.logger.info(f"Validating parameters: table={table_name}")

        if table_name not in RAD_FORCE_LOAD_TABLES:
            available_tables = list(RAD_FORCE_LOAD_TABLES.keys())
            raise ParameterValidationError(
                f"Invalid table '{table_name}'. Must be one of: {available_tables}",
                user_message=f"Please select a valid table: {', '.join(available_tables)}"
            )

        # Create model
        model = IngestorForceModel()

        # Validate configuration data
        context.logger.info(f"Validating {len(config_data)} configuration rows")
        model.validate_config(config_data)

        context.logger.info("Configuration validated successfully")

        # Execute force load
        context.logger.info(f"Executing force load to {table_name}")
        result = model.execute_force_load(table_name, config_data)

        context.logger.info(
            f"Force load complete: {result['rows_processed']} rows processed",
            extra={'result': result}
        )

        return result
