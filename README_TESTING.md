# KiCad Schematic Importer Testing Guide

This document provides guidance on testing the KiCad Schematic Importer plugin, including how to set up the testing environment and run the tests.

## Testing Environment Setup

### Mock pcbnew Module

Since the KiCad Schematic Importer plugin depends on the `pcbnew` module, which is part of KiCad's Python API and not available through pip, we've created a mock module for testing purposes.

The mock module is located at `tests/mock_pcbnew.py` and provides mock implementations of the KiCad classes and functions used by the plugin.

### conftest.py

The `tests/conftest.py` file sets up the testing environment by:

1. Adding the mock `pcbnew` module to `sys.modules`
2. Providing fixtures for platform-specific tests
3. Providing fixtures for test file paths

## Running Tests

To run all tests:

```bash
python -m pytest
```

To run a specific test file:

```bash
python -m pytest tests/test_install_advanced_plugin_simple.py
```

To run tests with verbose output:

```bash
python -m pytest -v
```

## Test Files

### test_install_advanced_plugin_simple.py

This file contains tests for the `install_advanced_plugin_simple.py` script, which is a simplified version of the plugin installer. It tests:

1. Finding the KiCad plugin directory on different platforms
2. Installing dependencies

### Other Test Files

- `test_alternative_image_processor.py`: Tests for the alternative image processor
- `test_image_processor.py`: Tests for the image processor
- `test_path_validator.py`: Tests for the path validator
- `test_project_manager.py`: Tests for the project manager
- `test_schematic_importer.py`: Tests for the schematic importer

## Mocking Strategies

When testing the plugin, we use several mocking strategies:

1. **Mock Modules**: We mock the `pcbnew` module to avoid requiring a KiCad installation.
2. **Monkeypatching**: We use pytest's `monkeypatch` fixture to replace functions and methods with mock implementations.
3. **Temporary Files**: We use pytest's `tmp_path` fixture to create temporary files and directories for testing.

## Continuous Integration

The plugin is tested in a CI environment using GitHub Actions. The workflow is defined in `.github/workflows/ci.yml`.

## Adding New Tests

When adding new tests:

1. Use the existing mocking infrastructure where possible
2. Add new mock classes and functions to `tests/mock_pcbnew.py` as needed
3. Use pytest fixtures to set up test environments
4. Use parametrized tests to test multiple scenarios with a single test function

## Troubleshooting

If you encounter issues with the tests:

1. Check that the mock `pcbnew` module provides all the necessary classes and functions
2. Ensure that the test environment is properly set up in `conftest.py`
3. Check that the tests are using the correct mocking strategies
4. Verify that the tests are compatible with the current version of the plugin
