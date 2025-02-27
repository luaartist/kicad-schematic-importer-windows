"""Base view provider for KiCad schematic components."""

# Handle FreeCAD imports with try-except to avoid errors when FreeCAD is not installed
try:
    import FreeCAD
    import FreeCADGui
    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False
    # Create dummy classes/modules for type checking
    class FreeCADDummy:
        pass
    
    class FreeCADGuiDummy:
        pass
    
    FreeCAD = FreeCADDummy()
    FreeCADGui = FreeCADGuiDummy()

class ViewProviderComponent:
    """Base view provider for KiCad schematic components."""

    def __init__(self, vobj):
        """
        Set this object to the proxy object of the actual view provider.
        
        Parameters
        ----------
        vobj: ViewObject
            The view object to attach to
        """
        vobj.Proxy = self

    def attach(self, vobj):
        """
        Setup the scene sub-graph of the view provider.
        
        Parameters
        ----------
        vobj: ViewObject
            The view object to attach to
        """
        self.ViewObject = vobj
        self.Object = vobj.Object

    def getIcon(self):
        """Return the icon which will appear in the tree view."""
        return ":/icons/schematic_component.svg"

    def __getstate__(self):
        """Return the state of the object for storing."""
        return None

    def __setstate__(self, state):
        """Set the state of the object after restoring."""
        return None
