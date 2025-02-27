#!/usr/bin/env python3
import os
import json
import datetime
import argparse
import shutil
from pathlib import Path

class HomeAutomationProjectManager:
    def __init__(self, base_dir=None):
        """Initialize the project manager"""
        if base_dir is None:
            # Use current directory if none specified
            self.base_dir = os.path.abspath(os.path.curdir)
        else:
            self.base_dir = os.path.abspath(base_dir)
        
        # Config file path
        self.config_path = os.path.join(self.base_dir, 'project_config.json')
        
        # Load or create config
        self.config = self.load_config()
        
        # Ensure base directories exist
        self.ensure_base_structure()
    
    def load_config(self):
        """Load project configuration or create default"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.create_default_config()
        else:
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default project configuration"""
        config = {
            'project_name': 'Home Automation Project',
            'created_date': datetime.datetime.now().isoformat(),
            'last_modified': datetime.datetime.now().isoformat(),
            'components': [],
            'modules': [],
            'reminders': [],
            'structure': {
                'kicad_projects': 'kicad_projects',
                'schematics': 'schematics',
                'firmware': 'firmware',
                'documentation': 'docs',
                'models': 'models',
                'plugins': 'plugins',
                'tests': 'tests',
                'data': 'data'
            }
        }
        
        # Save config
        self.save_config(config)
        return config
    
    def save_config(self, config=None):
        """Save project configuration"""
        if config is None:
            config = self.config
        
        # Update last modified date
        config['last_modified'] = datetime.datetime.now().isoformat()
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def ensure_base_structure(self):
        """Ensure base directory structure exists"""
        for dir_name in self.config['structure'].values():
            dir_path = os.path.join(self.base_dir, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"Created directory: {dir_path}")
    
    def create_module(self, module_name, module_type='generic'):
        """Create a new module in the project"""
        # Validate module name
        if not module_name.isalnum() and not '_' in module_name:
            raise ValueError("Module name must be alphanumeric (with underscores)")
        
        # Check if module already exists
        for module in self.config['modules']:
            if module['name'] == module_name:
                print(f"Module {module_name} already exists")
                return module
        
        # Create module structure based on type
        if module_type == 'sensor':
            module_structure = {
                'firmware': True,
                'schematic': True,
                'pcb': True,
                'docs': True,
                'tests': True
            }
        elif module_type == 'controller':
            module_structure = {
                'firmware': True,
                'schematic': True,
                'pcb': True,
                'docs': True,
                'tests': True,
                'api': True
            }
        elif module_type == 'interface':
            module_structure = {
                'frontend': True,
                'docs': True,
                'tests': True
            }
        else:  # generic
            module_structure = {
                'docs': True
            }
        
        # Create module directories
        module_dirs = []
        
        if module_structure.get('firmware', False):
            firmware_dir = os.path.join(self.base_dir, self.config['structure']['firmware'], module_name)
            os.makedirs(firmware_dir, exist_ok=True)
            module_dirs.append(firmware_dir)
            
            # Create basic firmware files
            with open(os.path.join(firmware_dir, f"{module_name}.ino"), 'w') as f:
                firmware_content = """/*
 * {0} - Firmware
 * Created: {1}
 */

void setup() {{
  // Initialize
  Serial.begin(115200);
  Serial.println("Initializing {0}...");
}}

void loop() {{
  // Main loop
  delay(1000);
}}
"""
                f.write(firmware_content.format(
                    module_name, 
                    datetime.datetime.now().strftime('%Y-%m-%d')
                ))
        
        if module_structure.get('schematic', False):
            schematic_dir = os.path.join(self.base_dir, self.config['structure']['kicad_projects'], module_name)
            os.makedirs(schematic_dir, exist_ok=True)
            module_dirs.append(schematic_dir)
        
        if module_structure.get('docs', False):
            docs_dir = os.path.join(self.base_dir, self.config['structure']['documentation'], module_name)
            os.makedirs(docs_dir, exist_ok=True)
            module_dirs.append(docs_dir)
            
            # Create basic README
            with open(os.path.join(docs_dir, "README.md"), 'w') as f:
                f.write(f"""# {module_name}

## Overview
Description of the {module_name} module.

## Components
- List components here

## Connections
- List connections here

## Usage
Instructions for using this module.
""")
        
        if module_structure.get('tests', False):
            tests_dir = os.path.join(self.base_dir, self.config['structure']['tests'], module_name)
            os.makedirs(tests_dir, exist_ok=True)
            module_dirs.append(tests_dir)
        
        if module_structure.get('api', False):
            api_dir = os.path.join(self.base_dir, self.config['structure']['firmware'], module_name, 'api')
            os.makedirs(api_dir, exist_ok=True)
            module_dirs.append(api_dir)
        
        # Add module to config
        module_info = {
            'name': module_name,
            'type': module_type,
            'created_date': datetime.datetime.now().isoformat(),
            'directories': [os.path.relpath(d, self.base_dir) for d in module_dirs],
            'components': []
        }
        
        self.config['modules'].append(module_info)
        self.save_config()
        
        print(f"Created module: {module_name} ({module_type})")
        return module_info
    
    def add_reminder(self, title, description, due_date=None):
        """Add a reminder for future work"""
        if due_date is None:
            # Default to 7 days from now
            due_date = (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
        elif isinstance(due_date, str):
            # Parse date string
            try:
                due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").isoformat()
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD")
                return None
        
        reminder = {
            'id': len(self.config['reminders']) + 1,
            'title': title,
            'description': description,
            'created_date': datetime.datetime.now().isoformat(),
            'due_date': due_date,
            'completed': False
        }
        
        self.config['reminders'].append(reminder)
        self.save_config()
        
        print(f"Added reminder: {title} (due: {due_date})")
        return reminder
    
    def list_reminders(self, show_completed=False):
        """List all reminders"""
        reminders = self.config['reminders']
        
        if not show_completed:
            reminders = [r for r in reminders if not r['completed']]
        
        if not reminders:
            print("No reminders found.")
            return []
        
        print("\nReminders:")
        print("-" * 60)
        for r in reminders:
            status = "[DONE]" if r['completed'] else "[TODO]"
            due_date = datetime.datetime.fromisoformat(r['due_date']).strftime("%Y-%m-%d")
            print(f"{r['id']:3d} {status} {r['title']} (Due: {due_date})")
            if r['description']:
                print(f"     {r['description']}")
        print("-" * 60)
        
        return reminders
    
    def complete_reminder(self, reminder_id):
        """Mark a reminder as completed"""
        for reminder in self.config['reminders']:
            if reminder['id'] == reminder_id:
                reminder['completed'] = True
                reminder['completed_date'] = datetime.datetime.now().isoformat()
                self.save_config()
                print(f"Marked reminder {reminder_id} as completed")
                return True
        
        print(f"Reminder {reminder_id} not found")
        return False
    
    def import_kicad_project(self, kicad_project_path, module_name=None):
        """Import an existing KiCad project"""
        if not os.path.exists(kicad_project_path):
            print(f"KiCad project not found: {kicad_project_path}")
            return False
        
        # Extract module name from path if not provided
        if module_name is None:
            module_name = os.path.basename(os.path.dirname(kicad_project_path))
        
        # Create module if it doesn't exist
        module_exists = False
        for module in self.config['modules']:
            if module['name'] == module_name:
                module_exists = True
                break
        
        if not module_exists:
            self.create_module(module_name, 'generic')
        
        # Copy KiCad project files
        dest_dir = os.path.join(self.base_dir, self.config['structure']['kicad_projects'], module_name)
        os.makedirs(dest_dir, exist_ok=True)
        
        # If path is a file, copy just that file
        if os.path.isfile(kicad_project_path):
            shutil.copy2(kicad_project_path, dest_dir)
            print(f"Imported KiCad file: {os.path.basename(kicad_project_path)}")
        else:
            # Copy all files in the directory
            for item in os.listdir(kicad_project_path):
                s = os.path.join(kicad_project_path, item)
                d = os.path.join(dest_dir, item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)
            print(f"Imported KiCad project to: {dest_dir}")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Home Automation Project Manager')
    parser.add_argument('--dir', type=str, help='Base project directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize project structure')
    
    # Create module command
    module_parser = subparsers.add_parser('create-module', help='Create a new module')
    module_parser.add_argument('name', type=str, help='Module name')
    module_parser.add_argument('--type', type=str, default='generic', 
                              choices=['generic', 'sensor', 'controller', 'interface'],
                              help='Module type')
    
    # Add reminder command
    reminder_parser = subparsers.add_parser('add-reminder', help='Add a reminder')
    reminder_parser.add_argument('title', type=str, help='Reminder title')
    reminder_parser.add_argument('--desc', type=str, default='', help='Reminder description')
    reminder_parser.add_argument('--due', type=str, help='Due date (YYYY-MM-DD)')
    
    # List reminders command
    list_parser = subparsers.add_parser('list-reminders', help='List reminders')
    list_parser.add_argument('--all', action='store_true', help='Show completed reminders')
    
    # Complete reminder command
    complete_parser = subparsers.add_parser('complete', help='Mark reminder as completed')
    complete_parser.add_argument('id', type=int, help='Reminder ID')
    
    # Import KiCad project command
    import_parser = subparsers.add_parser('import-kicad', help='Import KiCad project')
    import_parser.add_argument('path', type=str, help='Path to KiCad project file or directory')
    import_parser.add_argument('--module', type=str, help='Module name (default: derived from path)')
    
    args = parser.parse_args()
    
    # Create project manager
    pm = HomeAutomationProjectManager(args.dir)
    
    if args.command == 'init':
        pm.ensure_base_structure()
        print(f"Project initialized at: {pm.base_dir}")
    
    elif args.command == 'create-module':
        pm.create_module(args.name, args.type)
    
    elif args.command == 'add-reminder':
        pm.add_reminder(args.title, args.desc, args.due)
    
    elif args.command == 'list-reminders':
        pm.list_reminders(args.all)
    
    elif args.command == 'complete':
        pm.complete_reminder(args.id)
    
    elif args.command == 'import-kicad':
        pm.import_kicad_project(args.path, args.module)
    
    else:
        # If no command specified, show reminders
        print(f"Home Automation Project: {pm.config['project_name']}")
        pm.list_reminders()

if __name__ == "__main__":
    main()
