import os
import json
import sys
import importlib.util

class HomeAutomationIntegration:
    """Integration with HomeAutomationProjectManager"""
    
    def __init__(self, project_manager_path=None):
        self.project_manager = None
        self.project_manager_path = project_manager_path
        self._load_project_manager()
    
    def _load_project_manager(self):
        """Load HomeAutomationProjectManager module"""
        if self.project_manager_path and os.path.exists(self.project_manager_path):
            try:
                # Add directory to path
                sys.path.append(os.path.dirname(self.project_manager_path))
                
                # Load module
                spec = importlib.util.spec_from_file_location(
                    "project_manager", 
                    self.project_manager_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Create instance
                self.project_manager = module.HomeAutomationProjectManager()
                return True
            except Exception as e:
                print(f"Error loading project manager: {e}")
        return False
    
    def import_to_project(self, kicad_project_path, module_name=None):
        """Import KiCad project to HomeAutomationProjectManager"""
        if not self.project_manager:
            print("Project manager not loaded")
            return False
        
        try:
            result = self.project_manager.import_kicad_project(kicad_project_path, module_name)
            return result
        except Exception as e:
            print(f"Error importing to project: {e}")
            return False
    
    def create_module_for_schematic(self, schematic_name, module_type='generic'):
        """Create a new module for the schematic"""
        if not self.project_manager:
            print("Project manager not loaded")
            return None
        
        try:
            module_info = self.project_manager.create_module(schematic_name, module_type)
            return module_info
        except Exception as e:
            print(f"Error creating module: {e}")
            return None
    
    def add_reminder_for_schematic(self, schematic_name, description=None, due_date=None):
        """Add a reminder for the schematic"""
        if not self.project_manager:
            print("Project manager not loaded")
            return None
        
        title = f"Review schematic: {schematic_name}"
        if description is None:
            description = f"Review and finalize the schematic for {schematic_name}"
        
        try:
            reminder = self.project_manager.add_reminder(title, description, due_date)
            return reminder
        except Exception as e:
            print(f"Error adding reminder: {e}")
            return None