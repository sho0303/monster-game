"""
Resource path utilities for PyInstaller bundled execution.

This module provides functions to locate resources (images, sounds, YAML files)
whether running in development mode or as a bundled PyInstaller executable.
"""
import os
import sys
from pathlib import Path


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller.
    
    When running as a PyInstaller bundle, resources are extracted to a
    temporary folder (sys._MEIPASS). This function transparently handles
    both development and bundled execution modes.
    
    Args:
        relative_path (str): Relative path to resource from project root
                           Examples: 'art/ninja.png', 'monsters/Dragon.yaml'
    
    Returns:
        str: Absolute path to the resource
    
    Example:
        >>> image_path = get_resource_path('art/ninja.png')
        >>> with open(get_resource_path('store.yaml')) as f:
        >>>     data = yaml.safe_load(f)
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in development mode - use current directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Normalize the relative path to use OS-specific separators
    # This fixes issues on Windows where paths might have forward slashes
    relative_path = relative_path.replace('/', os.sep).replace('\\', os.sep)
    
    # Join the base path with the relative path
    full_path = os.path.join(base_path, relative_path)
    
    return full_path


def get_resource_dir(relative_dir):
    """Get absolute path to a resource directory.
    
    Args:
        relative_dir (str): Relative path to directory from project root
                          Examples: 'art', 'monsters', 'sounds'
    
    Returns:
        str: Absolute path to the directory
    """
    return get_resource_path(relative_dir)


def list_resource_files(relative_dir, extension=None):
    """List files in a resource directory.
    
    Args:
        relative_dir (str): Relative path to directory from project root
        extension (str, optional): Filter by file extension (e.g., '.yaml', '.png')
    
    Returns:
        list: List of filenames (not full paths) in the directory
    
    Example:
        >>> yaml_files = list_resource_files('monsters', '.yaml')
        >>> # Returns: ['Dragon.yaml', 'Goblin.yaml', ...]
    """
    dir_path = get_resource_path(relative_dir)
    
    try:
        if not os.path.isdir(dir_path):
            return []
        
        files = os.listdir(dir_path)
        
        if extension:
            # Filter by extension
            if not extension.startswith('.'):
                extension = '.' + extension
            files = [f for f in files if f.endswith(extension)]
        
        return files
    except OSError:
        return []


def resource_exists(relative_path):
    """Check if a resource exists.
    
    Args:
        relative_path (str): Relative path to resource from project root
    
    Returns:
        bool: True if resource exists, False otherwise
    """
    full_path = get_resource_path(relative_path)
    return os.path.exists(full_path)


def ensure_writable_dir(dir_name):
    """Ensure a writable directory exists outside the bundle.
    
    For directories that need to be writable (saves, logs), we create them
    in the user's app data directory or alongside the executable, NOT in
    the temporary _MEIPASS folder.
    
    Args:
        dir_name (str): Directory name (e.g., 'saves', 'logs')
    
    Returns:
        str: Absolute path to the writable directory
    """
    try:
        # Check if running as PyInstaller bundle
        if hasattr(sys, '_MEIPASS'):
            # Get the directory where the executable is located
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                exe_dir = os.path.dirname(sys.executable)
            else:
                exe_dir = os.path.dirname(os.path.abspath(__file__))
            
            writable_dir = os.path.join(exe_dir, dir_name)
        else:
            # Development mode - use current directory
            writable_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                dir_name
            )
        
        # Create directory if it doesn't exist
        os.makedirs(writable_dir, exist_ok=True)
        
        return writable_dir
    except Exception as e:
        # Fallback to current directory if something goes wrong
        fallback_dir = os.path.join(os.getcwd(), dir_name)
        os.makedirs(fallback_dir, exist_ok=True)
        return fallback_dir


def is_bundled():
    """Check if running as a PyInstaller bundle.
    
    Returns:
        bool: True if running as bundled executable, False if development mode
    """
    return hasattr(sys, '_MEIPASS')
