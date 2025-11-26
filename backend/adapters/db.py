"""
Database adapter - SWAP THIS AT WORK

Currently uses mock DB for local development.
To use work environment: Comment out LOCAL section, uncomment WORK section below.
"""

# ==============================================================================
# LOCAL IMPLEMENTATION (for development)
# ==============================================================================

class DBManager:
    """
    Mock database manager for local development.

    Provides same interface as work DBManager but returns mock data.
    """

    def __init__(self, env='dev'):
        """
        Initialize DB manager.

        Args:
            env: Environment (dev, uat, prod)
        """
        self.env = env
        print(f"[LOCAL] DBManager initialized for {env} environment")

    def query(self, sql, params=None):
        """
        Execute SQL query (mock).

        Args:
            sql: SQL query string
            params: Query parameters

        Returns:
            Mock result set
        """
        print(f"[LOCAL] Mock query: {sql}")
        return []

    def execute(self, sql, params=None):
        """
        Execute SQL statement (mock).

        Args:
            sql: SQL statement
            params: Statement parameters

        Returns:
            Number of rows affected (mock)
        """
        print(f"[LOCAL] Mock execute: {sql}")
        return 0

    def close(self):
        """Close connection (mock)."""
        print(f"[LOCAL] DBManager closed")


# Singleton instance
_db_manager = None


def get_db_manager(env='dev'):
    """
    Get singleton DBManager instance.

    Args:
        env: Environment (dev, uat, prod)

    Returns:
        DBManager singleton
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DBManager(env=env)
    return _db_manager


# ==============================================================================
# WORK IMPLEMENTATION (commented out - uncomment when deploying to work)
# ==============================================================================

# # Import your work DB manager class
# from your_work_package.db import DBManager
#
# # Singleton instance
# _db_manager = None
#
# def get_db_manager(env='prod'):
#     """
#     Get singleton DBManager instance.
#
#     Args:
#         env: Environment (dev, uat, prod)
#
#     Returns:
#         DBManager singleton
#     """
#     global _db_manager
#     if _db_manager is None:
#         _db_manager = DBManager(env=env)
#     return _db_manager
