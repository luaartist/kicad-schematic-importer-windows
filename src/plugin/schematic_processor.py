import os
from src.sync.flux_web_sync import FluxWebSync, FluxSyncConfig
from src.rules.stackup_manager import StackupManager
from src.routing.auto_router import AutoRouter

class SchematicProcessor:
    def __init__(self, private_mode=True):
        """
        Initialize the schematic processor
        
        Args:
            private_mode: Whether to run in private mode without external verification
        """
        self.flux_sync = FluxWebSync(FluxSyncConfig(
            api_endpoint=os.getenv('FLUX_API_ENDPOINT', 'https://app.flux.ai/api'),
            project_id=os.getenv('FLUX_PROJECT_ID', ''),
            auth_token=os.getenv('FLUX_AUTH_TOKEN', ''),
            auto_open_browser=True,
            private_mode=private_mode
        ))
        self.stackup_manager = StackupManager()
        self.auto_router = AutoRouter()
        self.private_mode = private_mode
        
    async def initialize(self):
        """Initialize real-time sync with Flux"""
        await self.flux_sync.start_sync()
        
    async def process_schematic_change(self, change):
        """Handle schematic changes with real-time sync"""
        # Automatically sync changes to PCB
        await self.flux_sync.push_schematic_update(change)
        
        # Auto-update ground planes
        await self.update_ground_planes()
        
        # Run real-time DRC
        violations = await self.check_design_rules()
        if violations:
            await self.display_violations(violations)
            
    async def update_ground_planes(self):
        """Automatically manage ground planes"""
        ground_portals = await self.find_ground_portals()
        for portal in ground_portals:
            await self.ground_plane_manager.create_or_update_plane(portal)
            
    async def start_interactive_routing(self, touch_point):
        """Start interactive routing session"""
        await self.auto_router.start_routing(touch_point)
