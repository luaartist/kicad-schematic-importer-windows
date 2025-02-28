import os
import sys
import shutil
import logging
from pathlib import Path

def check_dependencies():
    """Check and install required dependencies"""
    try:
        import wx
    except ImportError:
        print("\nError: wxPython (wx) is not installed.")
        print("\nPlease install wxPython using one of these methods:")
        print("\n1. Using pip:")
        print("   pip install wxPython")
        print("\n2. Or download from: https://wxpython.org/pages/downloads/")
        print("\nAfter installing wxPython, run this script again.")
        sys.exit(1)

def test_debug_locations():
    """Test installing debug plugin in multiple locations"""
    
    # Setup logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("DebugTest")
    
    # List of potential installation directories
    locations = [
        # Program Files
        {
            'path': r"C:\Program Files\KiCad\9.0\share\kicad\plugins",
            'type': 'system',
            'requires_admin': True
        },
        # User Documents
        {
            'path': os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', 'plugins'),
            'type': 'user',
            'requires_admin': False
        },
        # 3rdparty plugins
        {
            'path': os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', '3rdparty', 'plugins'),
            'type': 'user',
            'requires_admin': False
        },
        # AppData Local
        {
            'path': os.path.join(os.getenv('LOCALAPPDATA'), 'KiCad', 'plugins'),
            'type': 'user',
            'requires_admin': False
        },
        # AppData Roaming
        {
            'path': os.path.join(os.getenv('APPDATA'), 'KiCad', 'plugins'),
            'type': 'user',
            'requires_admin': False
        },
        # KiCad scripting plugins
        {
            'path': os.path.join(os.path.expanduser('~'), '.kicad', 'scripting', 'plugins'),
            'type': 'user',
            'requires_admin': False
        }
    ]
    
    # Files to copy
    files_to_copy = [
        'debug_plugin.py',
        'test_debug.py'
    ]
    
    results = []
    
    for loc in locations:
        try:
            logger.info(f"\nTesting location: {loc['path']}")
            
            # Skip system directories if not running as admin
            if loc['requires_admin'] and not os.access(os.path.dirname(loc['path']), os.W_OK):
                logger.warning(f"Skipping {loc['path']} - requires admin privileges")
                continue
            
            # Create directory if it doesn't exist
            os.makedirs(loc['path'], exist_ok=True)
            
            # Copy files
            for file in files_to_copy:
                src = os.path.join(os.path.dirname(__file__), file)
                dst = os.path.join(loc['path'], file)
                try:
                    shutil.copy2(src, dst)
                    logger.info(f"Copied {file} to {dst}")
                except Exception as e:
                    logger.error(f"Failed to copy {file}: {e}")
                    continue
            
            # Create debug directories
            debug_dir = os.path.join(loc['path'], 'debug')
            images_dir = os.path.join(debug_dir, 'images')
            os.makedirs(debug_dir, exist_ok=True)
            os.makedirs(images_dir, exist_ok=True)
            
            # Try importing the plugin
            sys.path.append(loc['path'])
            try:
                import debug_plugin
                debug_plugin.register_debug_plugin()
                logger.info("Successfully imported and registered plugin")
                results.append({
                    'location': loc['path'],
                    'status': 'SUCCESS',
                    'message': 'Plugin installed successfully'
                })
            except Exception as e:
                logger.error(f"Failed to import plugin: {e}")
                results.append({
                    'location': loc['path'],
                    'status': 'FAILED',
                    'message': f'Import failed: {str(e)}'
                })
            
            # Remove from sys.path to avoid conflicts
            sys.path.remove(loc['path'])
            
        except Exception as e:
            logger.error(f"Failed to test location {loc['path']}: {e}")
            results.append({
                'location': loc['path'],
                'status': 'ERROR',
                'message': str(e)
            })
    
    # Print summary
    print("\nTest Results Summary:")
    print("=====================")
    for result in results:
        print(f"\nLocation: {result['location']}")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
    
    # Return successful locations
    return [r['location'] for r in results if r['status'] == 'SUCCESS']

if __name__ == '__main__':
    # Check dependencies first
    check_dependencies()
    
    # Run tests
    successful_locations = test_debug_locations()
    
    if successful_locations:
        print("\nSuccessful installations:")
        for loc in successful_locations:
            print(f"- {loc}")
        print("\nTo use the debug plugin in KiCad:")
        print("1. Open KiCad PCB Editor")
        print("2. View → Python Console")
        print("3. Run these commands (choose one successful path):")
        for loc in successful_locations:
            print(f"\nFor {loc}:")
            print(f"   >>> import sys")
            print(f"   >>> sys.path.append(r'{loc}')")
            print(f"   >>> import debug_plugin")
            print(f"   >>> debug_plugin.register_debug_plugin()")
    else:
        print("\nNo successful installations found.")
        print("Please check the error messages above for details.")
