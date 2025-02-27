"""View provider for KiCad schematic components."""

from .view_base import ViewProviderComponent

class ViewProviderSchematicComponent(ViewProviderComponent):
    """View provider for KiCad schematic components."""
    
    def __init__(self, vobj):
        super().__init__(vobj)