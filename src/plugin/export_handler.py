class ExportHandler:
    async def finalize_schematic(self):
        """Final processing and export to KiCad"""
        # Generate netlist
        netlist = self.generate_netlist()
        
        # Create KiCad project structure
        project = await self.create_kicad_project()
        
        # Export components and connections
        await self.export_to_kicad(project, netlist)
        
        # Final DRC check
        violations = await self.perform_final_drc()
        
        return {
            'project_path': project.path,
            'component_count': len(self.components),
            'connection_count': len(self.connections),
            'drc_violations': violations
        }