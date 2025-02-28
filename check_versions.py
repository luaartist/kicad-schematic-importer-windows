import sys
print(f"Python version: {sys.version}")
try:
    import numpy
    print(f"NumPy version: {numpy.__version__}")
except ImportError as e:
    print(f"NumPy import error: {e}")