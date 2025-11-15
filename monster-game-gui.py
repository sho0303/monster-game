"""
Monster Game - GUI Launcher
Main entry point for the graphical user interface version with enhanced error handling
"""
import sys
import os
import warnings
from pathlib import Path
from datetime import datetime
from logger_utils import setup_logging, get_logger

# Suppress pygame's pkg_resources deprecation warning
# This is a pygame internal issue that will be fixed in future pygame versions
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

# Initialize logging first
log_file = setup_logging()
logger = get_logger(__name__)

def check_python_version():
    """Ensure Python version is compatible"""
    min_version = (3, 7)
    current_version = sys.version_info[:2]
    
    if current_version < min_version:
        error_msg = (
            f"Python {min_version[0]}.{min_version[1]} or higher is required.\n"
            f"Current version: {current_version[0]}.{current_version[1]}\n"
            f"Please upgrade Python and try again."
        )
        show_error("Python Version Error", error_msg)
        return False
    
    logger.info(f"Python version check passed: {current_version[0]}.{current_version[1]}")
    return True

def check_dependencies():
    """Check if all required modules are available with detailed feedback"""
    required_modules = {
        'tkinter': 'tkinter (usually included with Python)',
        'PIL': 'Pillow (pip install Pillow)',
        'pygame': 'pygame (pip install pygame)', 
        'yaml': 'PyYAML (pip install PyYAML)'
    }
    
    missing_modules = []
    
    for module, install_info in required_modules.items():
        try:
            __import__(module)
            logger.info(f"Module '{module}' found")
        except ImportError as e:
            missing_modules.append(install_info)
            logger.error(f"Missing module: {module} - {e}")
    
    if missing_modules:
        error_msg = (
            "Missing required dependencies:\n\n" +
            "\n".join(f"• {module}" for module in missing_modules) +
            "\n\nPlease install missing dependencies:\n"
            "pip install -r requirements.txt\n\n"
            "Or install individually:\n" +
            "\n".join(f"pip install {module.split('(')[1].split(')')[0]}" for module in missing_modules if '(' in module)
        )
        show_error("Missing Dependencies", error_msg)
        return False
    
    logger.info("All dependencies found")
    return True

def check_working_directory():
    """Verify we're running from the correct directory"""
    current_dir = Path.cwd()
    required_files = ['gui_main.py', 'game_state.py', 'store.yaml']
    required_dirs = ['heros', 'monsters', 'sounds', 'art']
    
    missing_items = []
    
    # Check files
    for file_name in required_files:
        if not (current_dir / file_name).exists():
            missing_items.append(f"File: {file_name}")
    
    # Check directories
    for dir_name in required_dirs:
        dir_path = current_dir / dir_name
        if not dir_path.exists():
            missing_items.append(f"Directory: {dir_name}")
        elif not any(dir_path.iterdir()):
            missing_items.append(f"Directory: {dir_name} (empty)")
    
    if missing_items:
        error_msg = (
            f"Game files not found in current directory:\n{current_dir}\n\n"
            "Missing items:\n" +
            "\n".join(f"• {item}" for item in missing_items) +
            "\n\nPlease ensure you're running the game from the correct directory.\n"
            "The game directory should contain gui_main.py and the game folders."
        )
        show_error("Missing Game Files", error_msg)
        return False
    
    logger.info(f"Working directory check passed: {current_dir}")
    return True

def check_gui_main_module():
    """Check if gui_main module can be imported"""
    try:
        from gui_main import GameGUI
        logger.info("gui_main module imported successfully")
        return True
    except ImportError as e:
        error_msg = (
            f"Could not import gui_main module:\n{e}\n\n"
            "This usually means:\n"
            "• gui_main.py is missing or corrupted\n"
            "• Missing dependencies in gui_main.py\n"
            "• Python path issues\n\n"
            "Please check that gui_main.py exists and all dependencies are installed."
        )
        show_error("Module Import Error", error_msg)
        return False
    except Exception as e:
        error_msg = (
            f"Unexpected error importing gui_main:\n{e}\n\n"
            "Please check the game files and try again."
        )
        show_error("Unexpected Import Error", error_msg)
        return False

def show_error(title, message):
    """Show error message with fallback for when tkinter might not be available"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:
        # Fallback to console output if tkinter fails
        print(f"\n{'='*50}")
        print(f"ERROR: {title}")
        print(f"{'='*50}")
        print(message)
        print(f"{'='*50}\n")

def initialize_game():
    """Initialize and start the game with comprehensive error handling"""
    try:
        import tkinter as tk
        from gui_main import GameGUI
        
        logger.info("Creating main window...")
        root = tk.Tk()
        
        # Bring window to foreground on Windows
        try:
            # Force window to appear on top initially
            root.wm_attributes("-topmost", 1)
            root.focus_force()
            root.lift()
            
            # Remove topmost after window is shown (so it doesn't stay always on top)
            root.after(100, lambda: root.wm_attributes("-topmost", 0))
            
            logger.info("Window configured to appear in foreground")
        except Exception as e:
            logger.warning(f"Could not configure window foreground behavior: {e}")
        
        logger.info("Initializing game GUI...")
        game = GameGUI(root)
        
        logger.info("Starting main loop...")
        root.mainloop()
        
    except Exception as e:
        error_msg = (
            f"Failed to start the game:\n{e}\n\n"
            "This could be due to:\n"
            "• Corrupted game files\n"
            "• Graphics driver issues\n"
            "• Insufficient system resources\n\n"
            "Check the log file in the 'logs' folder for detailed information."
        )
        logger.error(f"Game initialization failed: {e}", exc_info=True)
        show_error("Game Startup Error", error_msg)
        return False
    
    return True

def main():
    """Main entry point with comprehensive startup checks"""
    print("Monster Game - Starting up...")
    
    try:
        logger.info("=== Monster Game Startup ===")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Working directory: {Path.cwd()}")
        
        # Run all startup checks
        startup_checks = [
            ("Python version compatibility", check_python_version),
            ("Required dependencies", check_dependencies),
            ("Game files and directories", check_working_directory),
            ("GUI module import", check_gui_main_module),
        ]
        
        for check_name, check_func in startup_checks:
            logger.info(f"Checking: {check_name}")
            if not check_func():
                logger.error(f"Startup check failed: {check_name}")
                return False
        
        logger.info("All startup checks passed - initializing game")
        
        # Initialize and run the game
        success = initialize_game()
        
        if success:
            logger.info("Game session completed normally")
        else:
            logger.error("Game session ended with errors")
            
        return success
        
    except KeyboardInterrupt:
        logger.info("Game interrupted by user (Ctrl+C)")
        print("\nGame interrupted by user")
        return True
        
    except Exception as e:
        error_msg = f"Critical error during startup: {e}"
        logger.critical(error_msg, exc_info=True)
        show_error("Critical Startup Error", error_msg)
        return False
    
    finally:
        logger.info("=== Monster Game Shutdown ===")

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
