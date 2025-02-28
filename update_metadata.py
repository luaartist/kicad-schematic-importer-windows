#!/usr/bin/env python3
import os
import platform
import json

def find_kicad_plugin_dir(kicad_version="9.0"):
    """Find KiCad plugin directory"""
    if platform.system() == "Windows":
        if kicad_version == "9.0":
            # KiCad 9.0 uses a different location on Windows
            return os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "plugins")
        else:
            # Windows: %APPDATA%\kicad\7.0\scripting\plugins
            return os.path.join(os.getenv("APPDATA"), "kicad", kicad_version, "scripting", "plugins")
    elif platform.system() == "Darwin":  # macOS
        # macOS: ~/Library/Application Support/kicad/scripting/plugins
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "kicad", kicad_version, "scripting", "plugins")
    else:  # Linux
        # Linux: ~/.local/share/kicad/scripting/plugins
        return os.path.join(os.path.expanduser("~"), ".local", "share", "kicad", kicad_version, "scripting", "plugins")

def update_metadata():
    """Update the metadata.json file with developer credits"""
    # Get the KiCad plugin directory
    kicad_plugin_dir = find_kicad_plugin_dir("9.0")
    
    # Define the plugin directories
    plugin_dirs = [
        os.path.join(kicad_plugin_dir, "schematic_importer"),
        os.path.join(kicad_plugin_dir, "schematic_importer_simple")
    ]
    
    # Updated metadata with developer credits
    metadata = {
        "identifier": "com.augmentcode.kicad.schematicimporter",
        "name": "Schematic Importer",
        "description": "Import schematics from images using computer vision",
        "description_full": "A powerful KiCad plugin that uses computer vision to convert images of schematics into editable KiCad projects. Perfect for digitizing hand-drawn circuits, photographed schematics, or legacy documentation.",
        "category": "Importers",
        "author": {
            "name": "Wallace Lebrun",
            "contact": {
                "web": "https://github.com/augmentcode/kicad-schematic-importer"
            },
            "credentials": {
                "role": "Lead Developer",
                "expertise": [
                    "KiCad Plugin Development",
                    "Computer Vision Integration",
                    "Cross-platform Development"
                ]
            }
        },
        "development": {
            "methodology": "Hybrid AI-Assisted Development",
            "platforms_used": [
                "OpenAI ChatGPT Pro",
                "Anthropic Claude",
                "NinjaTech AI"
            ],
            "development_period": "2024",
            "development_hours": "100+"
        },
        "license": "MIT",
        "copyright": "© 2024 Wallace Lebrun",
        "resources": {
            "homepage": "https://github.com/augmentcode/kicad-schematic-importer"
        },
        "versions": [
            {
                "version": "0.3.2",
                "status": "testing",
                "kicad_version": "9.0",
                "platforms": ["linux", "windows", "macos"]
            }
        ],
        "tags": ["import", "computer vision", "automation"]
    }
    
    # Update metadata.json in each plugin directory
    for plugin_dir in plugin_dirs:
        metadata_path = os.path.join(plugin_dir, "metadata.json")
        if os.path.exists(plugin_dir):
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=4)
            print(f"Updated metadata.json in {plugin_dir}")
        else:
            print(f"Plugin directory not found: {plugin_dir}")
    
    print("\nMetadata updated with developer credits.")
    print("Please restart KiCad to see the updated metadata.")

if __name__ == "__main__":
    update_metadata()
