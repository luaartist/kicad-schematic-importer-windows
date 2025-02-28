import pcbnew
import wx
import os
import sys
import re
import math
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

from src.utils.alternative_image_processor import AlternativeImageProcessor
from src.ui.import_dialog import ImportDialog

# [Rest of your action_plugin.py code here, starting from COMPONENT_PATTERNS]