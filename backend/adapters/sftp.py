"""
SFTP adapter - SWAP THIS AT WORK

Currently uses mock SFTP for local development.
To use work environment: Comment out LOCAL section, uncomment WORK section below.
"""

# ==============================================================================
# LOCAL IMPLEMENTATION (for development)
# ==============================================================================

class SFTPManager:
    """
    Mock SFTP manager for local development.

    Provides same interface as work SFTPManager but returns mock data.
    """

    def __init__(self, host=None, username=None, key_file=None):
        """
        Initialize SFTP manager.

        Args:
            host: SFTP host
            username: Username
            key_file: SSH key file path
        """
        self.host = host
        self.username = username
        print(f"[LOCAL] SFTPManager initialized for {host}")

    def upload(self, local_path, remote_path):
        """
        Upload file (mock).

        Args:
            local_path: Local file path
            remote_path: Remote file path

        Returns:
            Success status (mock)
        """
        print(f"[LOCAL] Mock upload: {local_path} -> {remote_path}")
        return True

    def download(self, remote_path, local_path):
        """
        Download file (mock).

        Args:
            remote_path: Remote file path
            local_path: Local file path

        Returns:
            Success status (mock)
        """
        print(f"[LOCAL] Mock download: {remote_path} -> {local_path}")
        return True

    def list_files(self, remote_dir):
        """
        List files in directory (mock).

        Args:
            remote_dir: Remote directory path

        Returns:
            List of file names (mock)
        """
        print(f"[LOCAL] Mock list files: {remote_dir}")
        return []

    def close(self):
        """Close SFTP connection (mock)."""
        print(f"[LOCAL] SFTPManager closed")


# Singleton instance
_sftp_manager = None


def get_sftp_manager(host=None, username=None, key_file=None):
    """
    Get singleton SFTPManager instance.

    Args:
        host: SFTP host
        username: Username
        key_file: SSH key file path

    Returns:
        SFTPManager singleton
    """
    global _sftp_manager
    if _sftp_manager is None:
        _sftp_manager = SFTPManager(host=host, username=username, key_file=key_file)
    return _sftp_manager


# ==============================================================================
# WORK IMPLEMENTATION (commented out - uncomment when deploying to work)
# ==============================================================================

# # Import your work SFTP manager class
# from your_work_package.sftp import SFTPManager
#
# # Singleton instance
# _sftp_manager = None
#
# def get_sftp_manager(host=None, username=None, key_file=None):
#     """
#     Get singleton SFTPManager instance.
#
#     Args:
#         host: SFTP host
#         username: Username
#         key_file: SSH key file path
#
#     Returns:
#         SFTPManager singleton
#     """
#     global _sftp_manager
#     if _sftp_manager is None:
#         _sftp_manager = SFTPManager(host=host, username=username, key_file=key_file)
#     return _sftp_manager
