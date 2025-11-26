"""
Application configuration settings.

Only shared project-level settings. Tool-specific configs are in their models.
"""
from pathlib import Path

# ==============================================================================
# PROJECT CONFIGURATION
# ==============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
APP_NAME = "NLRAD Dashboard"
APP_VERSION = "0.1.0"
