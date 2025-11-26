"""
Hydra adapter - SWAP THIS AT WORK

Currently uses mock Hydra for local development.
To use work environment: Comment out LOCAL section, uncomment WORK section below.
"""

# ==============================================================================
# LOCAL IMPLEMENTATION (for development)
# ==============================================================================

class HydraManager:
    """
    Mock Hydra operations manager for local development.

    Provides same interface as work HydraManager but returns mock data.
    """

    def __init__(self, env='dev'):
        """
        Initialize Hydra manager.

        Args:
            env: Environment (dev, uat, prod)
        """
        self.env = env
        print(f"[LOCAL] HydraManager initialized for {env} environment")

    def get_config(self, config_name):
        """
        Get configuration (mock).

        Args:
            config_name: Configuration name

        Returns:
            Mock configuration dict
        """
        print(f"[LOCAL] Mock get_config: {config_name}")
        return {}

    def set_config(self, config_name, config_data):
        """
        Set configuration (mock).

        Args:
            config_name: Configuration name
            config_data: Configuration data

        Returns:
            Success status (mock)
        """
        print(f"[LOCAL] Mock set_config: {config_name}")
        return True

    def run_operation(self, operation_name, params=None):
        """
        Run Hydra operation (mock).

        Args:
            operation_name: Operation name
            params: Operation parameters

        Returns:
            Mock operation result
        """
        print(f"[LOCAL] Mock run_operation: {operation_name}")
        return {"status": "success", "data": {}}


# Singleton instance
_hydra_manager = None


def get_hydra_manager(env='dev'):
    """
    Get singleton HydraManager instance.

    Args:
        env: Environment (dev, uat, prod)

    Returns:
        HydraManager singleton
    """
    global _hydra_manager
    if _hydra_manager is None:
        _hydra_manager = HydraManager(env=env)
    return _hydra_manager


# ==============================================================================
# WORK IMPLEMENTATION (commented out - uncomment when deploying to work)
# ==============================================================================

# # Import your work Hydra manager class
# from your_work_package.hydra import HydraManager
#
# # Singleton instance
# _hydra_manager = None
#
# def get_hydra_manager(env='prod'):
#     """
#     Get singleton HydraManager instance.
#
#     Args:
#         env: Environment (dev, uat, prod)
#
#     Returns:
#         HydraManager singleton
#     """
#     global _hydra_manager
#     if _hydra_manager is None:
#         _hydra_manager = HydraManager(env=env)
#     return _hydra_manager
