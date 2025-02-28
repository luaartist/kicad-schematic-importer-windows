
from setuptools import setup, find_packages
import platform

# Base requirements
install_requires = [
    "opencv-python>=4.5.0",
    "numpy>=1.20.0",
    "pillow>=8.0.0",
    "svgpathtools>=1.5.0",
    "watchdog>=2.1.0",  # Added for file monitoring
]

# Add skidl only on Windows
if platform.system() == "Windows":
    install_requires.append("skidl>=1.0.0")

setup(
    name="kicad-schematic-importer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">=3.9",
    platforms=["win32", "win-amd64"],  # Windows only
)
