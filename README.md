# KiCad Schematic Importer Plugin

A powerful KiCad plugin that uses computer vision to convert images of schematics into editable KiCad projects. Perfect for digitizing hand-drawn circuits, photographed schematics, or legacy documentation.

## Features

- Import schematics from various image formats (PNG, JPG, SVG)
- Automatic component detection
- Connection tracing
- Export to KiCad schematic format

## Installation

### Automatic Installation

Run the installation script:

```bash
python install.py --kicad-version 9.0
```

### Manual Installation

1. Copy the plugin files to the KiCad plugins directory:
   - Windows (KiCad 9.0): `%USERPROFILE%\Documents\KiCad\9.0\3rdparty\plugins\schematic_importer`
   - Windows (KiCad 7.0): `%APPDATA%\kicad\7.0\scripting\plugins\schematic_importer`
   - Linux: `~/.local/share/kicad/[version]/scripting/plugins/schematic_importer`
   - macOS: `~/Library/Application Support/kicad/[version]/scripting/plugins/schematic_importer`

2. Restart KiCad

## Usage

1. Open KiCad PCB Editor
2. Click on the "Schematic Importer" plugin in the External Plugins menu
3. Select an image file containing a schematic
4. The plugin will vectorize the image and import it into the board

## Requirements

- KiCad 7.0 or later
- Python 3.6 or later
- OpenCV (for image processing)
- wxPython (for UI)

## Development

### Project Structure

```
schematic_importer/
├── __init__.py                  # Package initialization
├── action_plugin.py             # Main plugin file
├── metadata.json                # Plugin metadata
├── resources/
│   ├── icons/
│   │   └── icon.png             # Plugin icon
│   └── templates/
├── src/
│   ├── core/
│   │   └── schematic_importer.py # Core functionality
│   ├── ui/
│   │   └── import_dialog.py     # UI components
│   └── utils/
│       ├── image_processor.py   # Image processing utilities
│       └── path_validator.py    # Path validation utilities
└── tests/
    ├── test_image_processor.py
    ├── test_path_validator.py
    └── test_schematic_importer.py
```

### Running Tests

```bash
python -m pytest
```

## License

MIT License

## Author

Wallace Lebrun - Lead Developer and Architect

## Acknowledgments

This plugin was developed using a hybrid AI-assisted development methodology, utilizing various AI platforms including:
- OpenAI ChatGPT Pro
- Anthropic Claude
- NinjaTech AI

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.
