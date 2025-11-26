"""
Application configuration settings.
"""
import os
from pathlib import Path

# ==============================================================================
# PROJECT CONFIGURATION
# ==============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
APP_NAME = "NLRAD Dashboard"
APP_VERSION = "0.1.0"


# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FORMAT = os.environ.get("LOG_FORMAT", "json")  # json or text
LOG_FILE = PROJECT_ROOT / "logs" / "dashboard.log"


# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================

# Placeholder - user hasn't specified DB yet
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING", None)
DB_TIMEOUT = int(os.environ.get("DB_TIMEOUT", "30"))


# ==============================================================================
# RAD SETTINGS
# ==============================================================================

# Timeline Tool
RAD_TIMELINE_DESKS = ["Options", "Exotics", "Inflation", "LDFX", "FXG"]

# Force Load Tool
# Dictionary of table configurations with their schemas
RAD_FORCE_LOAD_TABLES = {
    "Inflation Env": {
        "description": "Inflation environment configuration",
        "columns": [
            {"name": "configName", "type": "string", "required": True},
            {"name": "key", "type": "string", "required": True},
            {"name": "group", "type": "string", "required": True},
        ],
        "default_rows": [
            {'configName': 'Config1', 'key': 'inflation.rate', 'group': 'ENV'},
            {'configName': 'Config2', 'key': 'inflation.curve', 'group': 'ENV'},
            {'configName': 'Config3', 'key': 'inflation.spread', 'group': 'ENV'},
        ]
    },
    "Options ScenarioGamma": {
        "description": "Options scenario gamma configuration",
        "columns": [
            {"name": "configName", "type": "string", "required": True},
            {"name": "key", "type": "string", "required": True},
            {"name": "group", "type": "string", "required": True},
        ],
        "default_rows": [
            {'configName': 'Gamma1', 'key': 'gamma.scenario.base', 'group': 'OPTS'},
            {'configName': 'Gamma2', 'key': 'gamma.scenario.stress', 'group': 'OPTS'},
        ]
    },
}


# ==============================================================================
# DD SETTINGS (placeholder for future DD tools)
# ==============================================================================

# Add DD-specific settings here when DD tools are implemented


# ==============================================================================
# BACKWARD COMPATIBILITY (deprecated - use RAD_* versions)
# ==============================================================================

TIMELINE_DESKS = RAD_TIMELINE_DESKS  # Deprecated: use RAD_TIMELINE_DESKS
FORCE_LOAD_TABLES = list(RAD_FORCE_LOAD_TABLES.keys())  # Deprecated: use RAD_FORCE_LOAD_TABLES
