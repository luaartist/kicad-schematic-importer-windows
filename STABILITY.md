# Stability Index & Version Compatibility

This document provides detailed information about the plugin's compatibility with different KiCad versions and known issues.

## Stability Index Methodology

Our stability index is based on:
1. **Automated Testing**: Percentage of tests passing
2. **User Reports**: Number and severity of reported issues
3. **Feature Completeness**: Percentage of features available
4. **Developer Testing**: Internal testing results

## KiCad 5.x Compatibility (🟡 Beta - 3/5)

### Supported Features
- Basic component detection
- Simple schematic import
- Local processing

### Known Limitations
- No support for complex component arrangements
- Limited footprint library integration
- Manual intervention often required for connections
- No support for hierarchical sheets

### Known Issues
- Issue #XX: Component placement offset in some cases
- Issue #XX: Resistor detection less accurate than in newer versions

## KiCad 6.x Compatibility (🟢 Stable - 4/5)

### Supported Features
- Full component detection
- Connection tracing
- FLUX.AI integration
- Debug visualization

### Known Limitations
- Some advanced footprints may not be properly mapped

### Known Issues
- Issue #XX: Occasional crashes with very large images

## KiCad 7.x Compatibility (🟢 Stable - 5/5)

### Supported Features
- All features fully supported
- Enhanced component recognition
- Advanced connection routing
- Full FLUX.AI integration

### Known Limitations
- None significant

### Known Issues
- None significant

## KiCad 9.x Compatibility (🔴 Alpha - 2/5)

### Supported Features
- Basic component detection
- Simple schematic import
- FLUX.AI integration (experimental)

### Known Limitations
- API changes in KiCad 9 may cause unexpected behavior
- Some features may not work as expected

### Known Issues
- Issue #XX: Plugin may not load correctly in some installations
- Issue #XX: Component placement issues with certain footprints

## Contributing to Stability Improvement

We welcome contributions to improve stability across all KiCad versions:

1. **Testing**: Test the plugin with your KiCad version and report results
2. **Bug Reports**: Submit detailed bug reports with steps to reproduce
3. **Code Contributions**: Help fix version-specific issues
4. **Documentation**: Help document workarounds for known issues