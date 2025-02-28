import pytest
import pcbnew

@pytest.fixture(autouse=True)
def reset_board():
    """Reset the board state before each test"""
    pcbnew._current_board = None
    yield
    pcbnew._current_board = None

@pytest.fixture
def board():
    """Create a fresh board for each test"""
    pcbnew._current_board = None
    return pcbnew.GetBoard()

class TestPlugin(pcbnew.ActionPlugin):
    """Test plugin class"""
    def __init__(self):
        super().__init__()
        self.name = "Test Plugin"
        self.category = "Test"
        self.description = "Test plugin for unit testing"
    
    def Run(self):
        """Test run method"""
        board = pcbnew.GetBoard()
        text = pcbnew.PCB_TEXT(board)
        text.SetText("Test")
        text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(10), pcbnew.FromMM(10)))
        board.Add(text)

def test_plugin_registration():
    """Test that plugin can be registered"""
    plugin = TestPlugin()
    plugin.register()  # Should not raise any exceptions

def test_plugin_attributes():
    """Test plugin attributes"""
    plugin = TestPlugin()
    assert plugin.name == "Test Plugin"
    assert plugin.category == "Test"
    assert plugin.description == "Test plugin for unit testing"

def test_plugin_run(board):
    """Test plugin run method"""
    plugin = TestPlugin()
    plugin.Run()  # Should not raise any exceptions
    
    # Verify text was added to the board
    assert len(board.items) == 1
    text = board.items[0]
    assert isinstance(text, pcbnew.PCB_TEXT)
    assert text.text == "Test"
    assert text.position.x == pcbnew.FromMM(10)
    assert text.position.y == pcbnew.FromMM(10)
