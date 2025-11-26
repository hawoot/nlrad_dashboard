"""
Backend initialization and bootstrap.

Called once during application startup.
"""
from backend.lib.logger import configure_root_logger
from backend.core.registry import get_registry
from backend.core.executor import get_executor
from backend.core.model_loader import get_model_loader


def initialize_backend():
    """
    Initialize backend infrastructure.

    Process:
    1. Configure logging
    2. Warm up registry (discover tools)
    3. Initialize executor
    4. Prepare shared resources
    """
    # Configure logging
    configure_root_logger()

    # Warm up registry (triggers tool discovery)
    registry = get_registry()
    print(f"Discovered {len(registry.list_all_tools())} tools")

    # Initialize executor
    executor = get_executor()

    # Initialize model loader (empty for now)
    loader = get_model_loader()

    print("Backend initialization complete")
