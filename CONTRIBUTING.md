# Contributing to KiCad Schematic Importer

Thank you for your interest in contributing to this project! We especially value contributions that help improve multi-version compatibility.

## How to Contribute

### Reporting Bugs
When reporting bugs, please include:
- KiCad version
- Plugin version
- Operating system
- Steps to reproduce
- Expected vs. actual behavior
- Screenshots if applicable

### Testing Version Compatibility
One of the most valuable contributions is testing with different KiCad versions:
1. Install the plugin on your KiCad version
2. Run through the [test procedure](docs/testing.md)
3. Report your results, even if everything works correctly!

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Ensure your code works across supported KiCad versions
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