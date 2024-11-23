import os

from core.settings import BASE_DIR, DEBUG


class FileLoader:
    """
    A utility class to load files based on the application's environment (debug or production).
    """

    @staticmethod
    def load_file(filename: str) -> str:
        """
        Load a file based on the current environment.
        """
        if FileLoader.is_debug_enviroment():
            return FileLoader.get_filename_for_debug(filename)
        return FileLoader.get_filename_for_production(filename)

    @staticmethod
    def is_debug_enviroment() -> bool:
        """
        Check if the application is running in debug mode.
        """
        return DEBUG

    @staticmethod
    def get_filename_for_debug(filename: str) -> str:
        """
        Get the full path for a file in debug mode.
        """
        list_dirs_from_filename = filename.split('/')
        return os.path.join(os.path.dirname(BASE_DIR), 'backend', *list_dirs_from_filename)

    @staticmethod
    def get_filename_for_production(filename: str) -> str:
        """
        Get the full path for a file in production mode.
        """
        return filename
