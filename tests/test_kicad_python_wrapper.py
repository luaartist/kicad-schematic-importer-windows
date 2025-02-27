def test_kicad_initialization(self, windows_only):
    """Test KiCad wrapper initialization"""
    wrapper = KicadPythonWrapper()
    assert wrapper.initialized == False
    assert wrapper.kicad_version is not None

def test_path_handling(self, windows_only):
    """Test Windows-specific path handling"""
    wrapper = KicadPythonWrapper()
    test_path = wrapper._normalize_path("C:\\Program Files\\KiCad\\")
    assert '\\' in test_path