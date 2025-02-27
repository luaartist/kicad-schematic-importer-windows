
from setuptools import setup, find_packages

setup(
    name="kicad-schematic-importer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.20.0",
        "pillow>=8.0.0",
        "skidl>=1.0.0",
        # python-potrace is optional
    ],
)
