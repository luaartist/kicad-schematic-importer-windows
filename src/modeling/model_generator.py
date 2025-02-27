# Handle FreeCAD imports with try-except to avoid errors when FreeCAD is not installed
try:
    import FreeCAD
    import Part
    from FreeCAD import Base
    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False
    # Create dummy classes/modules for type checking
    class FreeCADDummy:
        def newDocument(self):
            pass
    
    class BaseDummy:
        pass
    
    class PartDummy:
        pass
    
    FreeCAD = FreeCADDummy()
    Part = PartDummy()
    Base = BaseDummy()

from src.viewproviders.view_base import ViewProviderComponent

class PCBModelGenerator:
    def __init__(self):
        self.doc = FreeCAD.newDocument()
        
    def create_board_model(self, components, board_dimensions):
        """Create complete PCB 3D model"""
        # Create base PCB
        board = self.create_pcb_base(board_dimensions)
        
        # Add components
        for component in components:
            self.add_component_model(component)
            
        # Add metadata for Flux.ai visualization
        self.add_visualization_metadata()
        
    def add_component_model(self, component):
        """Add individual component with metadata"""
        obj = self.doc.addObject("Part::FeaturePython", component.type)
        
        # Add visualization properties
        obj.addProperty("App::PropertyString", "ComponentType", "Metadata", "Type of component")
        obj.addProperty("App::PropertyString", "Footprint", "Metadata", "Component footprint")
        obj.addProperty("App::PropertyString", "FluxVisualization", "Metadata", "Flux.ai visualization data")
        
        # Set properties
        obj.ComponentType = component.type
        obj.Footprint = component.footprint
        
        # Add ViewProvider for custom visualization
        ViewProviderComponent(obj.ViewObject)
        
    def export_for_manufacturing(self, format_type):
        """Export model in various formats"""
        if format_type == "3d_print":
            return self.export_for_3d_printing()
        elif format_type == "flux":
            return self.export_for_flux()
        elif format_type == "step":
            return self.export_step()
