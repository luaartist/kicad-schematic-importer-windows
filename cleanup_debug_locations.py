import os
import shutil
import logging

def cleanup_debug_installations():
    """Remove debug plugin installations from test locations"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Cleanup")
    
    locations = [
        r"C:\Program Files\KiCad\9.0\share\kicad\plugins",
        os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', 'plugins'),
        os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', '3rdparty', 'plugins'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'KiCad', 'plugins'),
        os.path.join(os.getenv('APPDATA'), 'KiCad', 'plugins'),
        os.path.join(os.path.expanduser('~'), '.kicad', 'scripting', 'plugins')
    ]
    
    files_to_remove = [
        'debug_plugin.py',
        'test_debug.py',
        'debug_icon.png'
    ]
    
    for loc in locations:
        if os.path.exists(loc):
            logger.info(f"\nCleaning up {loc}")
            
            # Remove files
            for file in files_to_remove:
                file_path = os.path.join(loc, file)
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logger.info(f"Removed {file_path}")
                except Exception as e:
                    logger.error(f"Failed to remove {file_path}: {e}")
            
            # Remove debug directory
            debug_dir = os.path.join(loc, 'debug')
            if os.path.exists(debug_dir):
                try:
                    shutil.rmtree(debug_dir)
                    logger.info(f"Removed debug directory: {debug_dir}")
                except Exception as e:
                    logger.error(f"Failed to remove debug directory: {e}")

if __name__ == '__main__':
    cleanup_debug_installations()