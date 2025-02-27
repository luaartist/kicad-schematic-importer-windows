import sys
from unittest.mock import MagicMock

# Create mock modules for KiCad dependencies
MOCK_MODULES = ['pcbnew', 'wx']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = MagicMock()

# Mock specific classes and functions used in the code
sys.modules['pcbnew'].ActionPlugin = MagicMock
sys.modules['pcbnew'].GetBoard = MagicMock
sys.modules['wx'].Dialog = MagicMock
