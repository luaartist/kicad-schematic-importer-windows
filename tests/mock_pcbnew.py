"""Mock module for pcbnew to allow testing without KiCad installation."""

class ActionPlugin:
    """Mock ActionPlugin base class"""
    def __init__(self):
        self.name = "Mock Plugin"
        self.category = "Mock Category"
        self.description = "Mock Description"
    
    def defaults(self):
        pass
    
    def Run(self):
        pass
        
    def register(self):
        """Mock register method"""
        pass

# Add other necessary mock classes and functions here
class VECTOR2I:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PCB_TEXT:
    def __init__(self, board=None):
        self._text = ""
        self.position = VECTOR2I(0, 0)
        self.size = VECTOR2I(0, 0)
    
    def SetText(self, text):
        self._text = text
    
    def GetText(self):
        return self._text
    
    @property
    def text(self):
        return self._text
    
    def SetPosition(self, position):
        self.position = position
    
    def SetTextSize(self, size):
        self.size = size

class FOOTPRINT:
    def __init__(self, board=None):
        self.reference = ""
        self.value = ""
        self.position = VECTOR2I(0, 0)
        self.pads = []
    
    def SetReference(self, reference):
        self.reference = reference
    
    def SetValue(self, value):
        self.value = value
    
    def SetPosition(self, position):
        self.position = position
    
    def Add(self, pad):
        self.pads.append(pad)

class PAD:
    def __init__(self, footprint=None):
        self.number = ""
        self.shape = 0
        self.attribute = 0
        self.size = VECTOR2I(0, 0)
        self.position = VECTOR2I(0, 0)
        self.drill_size = VECTOR2I(0, 0)
    
    def SetNumber(self, number):
        self.number = number
    
    def SetShape(self, shape):
        self.shape = shape
    
    def SetAttribute(self, attribute):
        self.attribute = attribute
    
    def SetSize(self, size):
        self.size = size
    
    def SetPosition(self, position):
        self.position = position
    
    def SetDrillSize(self, size):
        self.drill_size = size
    
    def SetLayerSet(self, layer_set):
        pass

class PCB_TRACK:
    def __init__(self, board=None):
        self.start = VECTOR2I(0, 0)
        self.end = VECTOR2I(0, 0)
        self.width = 0
    
    def SetStart(self, start):
        self.start = start
    
    def SetEnd(self, end):
        self.end = end
    
    def SetWidth(self, width):
        self.width = width

_current_board = None

class BOARD:
    def __init__(self):
        self.items = []
    
    def Add(self, item):
        self.items.append(item)

def GetBoard():
    global _current_board
    if _current_board is None:
        _current_board = BOARD()
    return _current_board

def FromMM(mm):
    return mm * 1000000

def Refresh():
    pass

# Constants
PAD_SHAPE_CIRCLE = 0
PAD_ATTRIB_PTH = 0

class LSET:
    @staticmethod
    def AllCuMask():
        return 0
