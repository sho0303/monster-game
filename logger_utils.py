"""
Centralized logging utility for PyQuest Monster Game.

This module provides a standardized logging configuration that all other modules
should use instead of print() statements. Ensures consistent formatting and
proper log routing to both file and console.

Usage:
    from logger_utils import get_logger
    
    logger = get_logger(__name__)
    logger.info("Information message")
    logger.error("Error message")
    logger.debug("Debug message")
"""

import logging
import os
from datetime import datetime
from typing import Optional
from resource_utils import ensure_writable_dir


# Track if logging is already configured to avoid duplicate handlers
_logging_configured = False
_log_file_path: Optional[str] = None


def setup_logging(log_dir: str = "logs", log_level: int = logging.INFO) -> str:
    """
    Configure the root logger with file and console handlers.
    
    This should be called once at application startup (in monster-game-gui.py).
    Subsequent calls to get_logger() will use this configuration.
    
    Args:
        log_dir: Directory to store log files (default: "logs")
        log_level: Logging level (default: logging.INFO)
        
    Returns:
        Path to the created log file
        
    Example:
        log_file = setup_logging(log_dir="logs", log_level=logging.DEBUG)
        print(f"Logging to: {log_file}")
    """
    global _logging_configured, _log_file_path
    
    if _logging_configured:
        return _log_file_path
    
    # Ensure writable logs directory (handles PyInstaller bundle)
    log_dir_path = ensure_writable_dir(log_dir)
    
    # Create timestamped log file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir_path, f'game_{timestamp}.log')
    _log_file_path = log_file
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove any existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler - logs everything
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler - logs WARNING and above to avoid cluttering terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    _logging_configured = True
    
    root_logger.info("=" * 80)
    root_logger.info("PyQuest Monster Game - Logging System Initialized")
    root_logger.info(f"Log file: {log_file}")
    root_logger.info(f"Log level: {logging.getLevelName(log_level)}")
    root_logger.info("=" * 80)
    
    return log_file


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    This is the primary function that all modules should use to get their logger.
    Each module should call this once at the module level:
    
        logger = get_logger(__name__)
    
    Args:
        name: Name of the logger (typically __name__ for the calling module)
        
    Returns:
        Configured logger instance
        
    Example:
        # At the top of your module
        from logger_utils import get_logger
        logger = get_logger(__name__)
        
        # Later in your code
        logger.info("Starting combat round")
        logger.error(f"Failed to load monster: {monster_name}")
        logger.debug(f"Damage calculation: {damage}")
    """
    global _logging_configured
    
    # If logging hasn't been configured yet, do basic configuration
    # This ensures modules work even if setup_logging() wasn't called
    if not _logging_configured:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        _logging_configured = True
    
    return logging.getLogger(name)


def get_log_file_path() -> Optional[str]:
    """
    Get the path to the current log file.
    
    Returns:
        Path to the log file, or None if logging hasn't been set up yet
    """
    return _log_file_path
