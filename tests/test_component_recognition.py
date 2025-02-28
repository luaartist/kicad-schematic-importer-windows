import pytest
from src.component_recognition import ComponentRecognizer, ConnectionTracer

def test_component_recognizer():
    recognizer = ComponentRecognizer()
    test_image = "tests/test_files/test_schematic.png"
    components = recognizer.recognize(test_image)
    assert len(components) > 0
    assert all(c.type for c in components)

def test_connection_tracer():
    tracer = ConnectionTracer()
    test_image = "tests/test_files/test_schematic.png"
    connections = tracer.trace(test_image)
    assert len(connections) > 0
    assert all(c.start and c.end for c in connections)
