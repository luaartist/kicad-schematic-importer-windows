import os
import pytest
from src.plugin.import_workflow import SchematicImportWorkflow

def test_windows_performance():
    """Test performance metrics on Windows platform"""
    workflow = SchematicImportWorkflow()
    test_images = [
        "test_data/simple_circuit.png",
        "test_data/complex_circuit.png"
    ]
    
    performance_data = {}
    for img in test_images:
        result = workflow.process_image(img)
        
        # Collect metrics
        performance_data[img] = {
            'preprocessing_time': result.preprocess_time,
            'detection_time': result.detect_time,
            'memory_usage': result.memory_used,
            'total_time': result.total_time
        }
        
        # Assert performance thresholds
        assert result.preprocess_time < 2.0, f"Preprocessing too slow: {result.preprocess_time}s"
        assert result.memory_used < 500_000_000, f"Excessive memory use: {result.memory_used} bytes"

    return performance_data