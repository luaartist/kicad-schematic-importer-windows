# Contributing to KiCad Schematic Importer

Thank you for your interest in contributing to this Windows-only KiCad plugin!

## Development Requirements
- Windows 10 or later
- Python 3.9 or later
- KiCad 5.x, 6.x, 7.x, or 9.x (Windows versions)
- Git for Windows
- Visual Studio Code (recommended)

## How to Contribute

### Setting Up Development Environment
1. Install Python for Windows
2. Install KiCad for Windows
3. Clone the repository
4. Run `pip install -r requirements-dev.txt`
5. Install Windows-specific dependencies:
   ```
   pip install winshell pywin32
   ```

### Testing
1. Run the Windows test suite:
   ```
   .\run_windows_tests.ps1
   ```

### Reporting Bugs
When reporting bugs, please include:
- Windows version
- KiCad version
- Python version
- Steps to reproduce
- Expected vs. actual behavior
- Screenshots if applicable

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Ensure all Windows tests pass
6. Submit a pull request

### Documentation Contributions
Help improve our documentation, especially:
- Version-specific instructions
- Troubleshooting guides
- Usage examples

## Version-Specific Development Guidelines

### KiCad 5.x
- Use only the legacy API methods
- Test thoroughly with KiCad 5.1.x
- Document any workarounds needed

### KiCad 6.x and 7.x
- Use standard API methods
- Ensure backward compatibility where possible

### KiCad 9.x
- Document any API changes
- Use conditional imports for version-specific code
- Clearly mark experimental features

## Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Comment complex sections of code
- Write docstrings for all functions and classes

## Review Process
All contributions will be reviewed for:
- Code quality
- Cross-version compatibility
- Documentation completeness
- Test coverage

Thank you for helping improve the KiCad Schematic Importer!
