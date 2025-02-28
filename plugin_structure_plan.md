# KiCad Plugin Structure Plan

## Ideal Folder Structure

```
schematic_importer/
├── __init__.py                  # Package initialization
├── action_plugin.py             # Main plugin file
├── metadata.json                # Plugin metadata
├── README.md                    # Documentation
├── LICENSE                      # License file
├── resources/
│   ├── __init__.py              # Make resources a package
│   └── icon.png                 # Plugin icon
├── src/
│   ├── __init__.py              # Make src a package
│   ├── core/
│   │   ├── __init__.py          # Make core a package
│   │   └── schematic_importer.py # Core functionality
│   ├── ui/
│   │   ├── __init__.py          # Make ui a package
│   │   └── import_dialog.py     # UI components
│   └── utils/
│       ├── __init__.py          # Make utils a package
│       ├── image_processor.py   # Image processing utilities
│       └── path_validator.py    # Path validation utilities
└── tests/
    ├── __init__.py              # Make tests a package
    ├── test_image_processor.py  # Tests for image processor
    ├── test_path_validator.py   # Tests for path validator
    └── test_schematic_importer.py # Tests for schematic importer
```

## Commands to Create the Structure

```bash
# Create the main directory structure
mkdir -p schematic_importer/resources
mkdir -p schematic_importer/src/core
mkdir -p schematic_importer/src/ui
mkdir -p schematic_importer/src/utils
mkdir -p schematic_importer/tests

# Create __init__.py files
touch schematic_importer/__init__.py
touch schematic_importer/resources/__init__.py
touch schematic_importer/src/__init__.py
touch schematic_importer/src/core/__init__.py
touch schematic_importer/src/ui/__init__.py
touch schematic_importer/src/utils/__init__.py
touch schematic_importer/tests/__init__.py

# Create main plugin files
touch schematic_importer/action_plugin.py
touch schematic_importer/metadata.json
touch schematic_importer/README.md
touch schematic_importer/LICENSE
touch schematic_importer/resources/icon.png
```

## Files to Remove

The following directories and files can be removed as they are not necessary for the plugin:

```
community/
conda/
debug/
docs/
examples/
firmware/
github/
kicad_projects/
kicad_schematic_importer.egg-info/
models/
plugins/
schematics/
security/
sync/
viewproviders/
visualization/
```

## Files to Keep and Reorganize

The following files should be kept and reorganized into the new structure:

1. `src/utils/path_validator.py` → `schematic_importer/src/utils/path_validator.py`
2. `src/utils/image_processor.py` → `schematic_importer/src/utils/image_processor.py`
3. `src/utils/alternative_image_processor.py` → `schematic_importer/src/utils/image_processor.py` (merge functionality)
4. `src/core/schematic_importer.py` → `schematic_importer/src/core/schematic_importer.py`
5. `src/ui/import_dialog.py` → `schematic_importer/src/ui/import_dialog.py`
6. `tests/test_path_validator.py` → `schematic_importer/tests/test_path_validator.py`
7. `tests/test_image_processor.py` → `schematic_importer/tests/test_image_processor.py`
8. `tests/test_schematic_importer.py` → `schematic_importer/tests/test_schematic_importer.py`

## Commit Notes

When submitting to the KiCad repository, include the following information in your commit message:

```
Add Schematic Importer Plugin

This plugin allows users to import schematics from images using computer vision.
Features include:
- Import from various image formats (PNG, JPG, SVG)
- Automatic component detection
- Connection tracing
- Export to KiCad schematic format

The plugin is compatible with KiCad 7.0 and 9.0.

Tested on:
- Windows 10/11
- Python 3.12
```

## Generalizing the Code

To remove personal information and generalize the code:

1. Replace any hardcoded paths with relative paths or environment variables
2. Remove any references to personal usernames or directories
3. Use platform-agnostic path handling (use `os.path.join` instead of hardcoded separators)
4. Remove any API keys or credentials
5. Use generic email addresses and URLs in metadata
