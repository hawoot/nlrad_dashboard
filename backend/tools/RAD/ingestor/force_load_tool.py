"""
Force load tool.

Allows users to force load configuration data to predefined tables.
"""
from typing import List, Dict, Any
from backend.core.base_tool import BaseTool, ExecutionContext
from backend.models.ingestor_force import IngestorForceModel, FORCE_LOAD_TABLES
from backend.lib.errors import ParameterValidationError


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
        action='save',
        config=None
    ):
        """
        Execute force load.

        Args:
            context: Execution context
            table_name: Table to load
            action: 'get_default' to get default config, 'save' to save config
            config: Configuration data (required for 'save' action)

        Returns:
            Dictionary with result details

        Raises:
            ParameterValidationError: If parameters are invalid
        """
        # Validate table name
        context.logger.info(f"Validating parameters: table={table_name}, action={action}")

        if table_name not in FORCE_LOAD_TABLES:
            available_tables = list(FORCE_LOAD_TABLES.keys())
            raise ParameterValidationError(
                f"Invalid table '{table_name}'. Must be one of: {available_tables}",
                user_message=f"Please select a valid table: {', '.join(available_tables)}"
            )

        # Create model
        model = IngestorForceModel()

        # Handle different actions
        if action == 'get_default':
            context.logger.info(f"Getting default config for {table_name}")
            default_config = model.get_default_config(table_name)
            schema = model.get_table_schema(table_name)
            return {
                'config': default_config,
                'schema': schema,
                'table_name': table_name
            }

        elif action == 'save':
            if config is None:
                raise ParameterValidationError(
                    "config parameter is required for 'save' action",
                    user_message="Configuration data is required"
                )

            # Validate configuration data
            context.logger.info(f"Validating {len(config)} configuration rows")
            model.validate_config(config)

            context.logger.info("Configuration validated successfully")

            # Execute force load
            context.logger.info(f"Executing force load to {table_name}")
            result = model.execute_force_load(table_name, config)

            context.logger.info(
                f"Force load complete: {result['rows_processed']} rows processed",
                extra={'result': result}
            )

            return result

        else:
            raise ParameterValidationError(
                f"Invalid action '{action}'. Must be 'get_default' or 'save'",
                user_message="Invalid action specified"
            )
