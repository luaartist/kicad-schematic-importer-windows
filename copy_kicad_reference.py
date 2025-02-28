"""
Script to copy KiCad reference files to a local directory for analysis.

This script creates a local copy of the KiCad installation directory for closer
examination of the DLLs and other files. This allows for easier analysis without
having to access the Program Files directory directly.

The copied files are for reference only and should not be used for actual execution.
"""

import os
import sys
import shutil
import logging
import platform
import argparse
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_kicad_installation():
    """Find KiCad installation directory."""
    if platform.system() == "Windows":
        # Check common installation paths on Windows
        program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
        program_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
        
        # Check for KiCad in Program Files
        kicad_versions = ['9.0', '8.0', '7.0', '6.0']
        for version in kicad_versions:
            # Check 64-bit installation
            path = os.path.join(program_files, 'KiCad', version)
            if os.path.exists(path):
                return path, version
            
            # Check 32-bit installation
            path = os.path.join(program_files_x86, 'KiCad', version)
            if os.path.exists(path):
                return path, version
    
    elif platform.system() == "Darwin":  # macOS
        # Check common installation paths on macOS
        paths = [
            '/Applications/KiCad/KiCad.app',
            '/Applications/KiCad.app'
        ]
        
        for path in paths:
            if os.path.exists(path):
                return path, None
    
    else:  # Linux and others
        # Check common installation paths on Linux
        paths = [
            '/usr/share/kicad',
            '/usr/local/share/kicad'
        ]
        
        for path in paths:
            if os.path.exists(path):
                return path, None
    
    return None, None

def copy_kicad_reference(source_dir, target_dir, include_patterns=None, exclude_patterns=None, max_size_mb=100):
    """
    Copy KiCad reference files to a local directory.
    
    Args:
        source_dir: Source directory (KiCad installation)
        target_dir: Target directory for the copy
        include_patterns: List of file patterns to include (e.g., ['*.dll', '*.exe'])
        exclude_patterns: List of file patterns to exclude (e.g., ['*.pdb', '*.lib'])
        max_size_mb: Maximum size of files to copy in MB
    """
    if not os.path.exists(source_dir):
        logger.error(f"Source directory not found: {source_dir}")
        return False
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Default patterns if not provided
    if include_patterns is None:
        include_patterns = ['*.dll', '*.exe', '*.py', '*.json', '*.txt', '*.md', '*.h', '*.cpp']
    
    if exclude_patterns is None:
        exclude_patterns = ['*.pdb', '*.lib', '*.a', '*.o', '*.obj', '*.log']
    
    # Maximum file size in bytes
    max_size = max_size_mb * 1024 * 1024
    
    # Track statistics
    stats = {
        'copied_files': 0,
        'skipped_files': 0,
        'total_size': 0
    }
    
    # Copy files
    for root, dirs, files in os.walk(source_dir):
        # Create relative path
        rel_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, rel_path)
        
        # Create target directory
        os.makedirs(target_path, exist_ok=True)
        
        # Copy files
        for file in files:
            # Check if file matches include patterns
            include_file = False
            for pattern in include_patterns:
                if Path(file).match(pattern):
                    include_file = True
                    break
            
            # Check if file matches exclude patterns
            for pattern in exclude_patterns:
                if Path(file).match(pattern):
                    include_file = False
                    break
            
            if include_file:
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_path, file)
                
                # Check file size
                file_size = os.path.getsize(source_file)
                if file_size > max_size:
                    logger.info(f"Skipping large file: {source_file} ({file_size / 1024 / 1024:.2f} MB)")
                    stats['skipped_files'] += 1
                    continue
                
                # Copy file
                try:
                    shutil.copy2(source_file, target_file)
                    stats['copied_files'] += 1
                    stats['total_size'] += file_size
                    logger.debug(f"Copied: {source_file} -> {target_file}")
                except Exception as e:
                    logger.error(f"Error copying {source_file}: {e}")
                    stats['skipped_files'] += 1
    
    # Log statistics
    logger.info(f"Copied {stats['copied_files']} files ({stats['total_size'] / 1024 / 1024:.2f} MB)")
    logger.info(f"Skipped {stats['skipped_files']} files")
    
    return True

def create_readme(target_dir, kicad_path, kicad_version):
    """Create a README file in the target directory."""
    readme_path = os.path.join(target_dir, 'README.md')
    
    content = f"""# KiCad Reference Files

This directory contains reference files from the KiCad installation for analysis purposes.

## Source Information

- KiCad Path: {kicad_path}
- KiCad Version: {kicad_version or 'Unknown'}
- Copy Date: {os.path.ctime(os.path.getmtime(target_dir))}

## Purpose

These files are for reference only and should not be used for actual execution.
They are provided to allow for easier analysis of KiCad's structure and functionality
without having to access the Program Files directory directly.

## Important Notes

- These files are not meant to be executed directly.
- The directory structure has been preserved to match the original KiCad installation.
- Some large files may have been excluded to save space.
"""
    
    with open(readme_path, 'w') as f:
        f.write(content)
    
    logger.info(f"Created README file: {readme_path}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Copy KiCad reference files to a local directory.')
    parser.add_argument('--target', default='kicad_reference', help='Target directory for the copy')
    parser.add_argument('--source', help='Source directory (KiCad installation)')
    parser.add_argument('--include', nargs='+', help='File patterns to include')
    parser.add_argument('--exclude', nargs='+', help='File patterns to exclude')
    parser.add_argument('--max-size', type=int, default=100, help='Maximum file size in MB')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Find KiCad installation if not provided
    source_dir = args.source
    kicad_version = None
    if not source_dir:
        source_dir, kicad_version = find_kicad_installation()
        if not source_dir:
            logger.error("KiCad installation not found. Please specify the source directory.")
            return 1
    
    # Create absolute paths
    source_dir = os.path.abspath(source_dir)
    target_dir = os.path.abspath(args.target)
    
    logger.info(f"Source directory: {source_dir}")
    logger.info(f"Target directory: {target_dir}")
    
    # Copy files
    if copy_kicad_reference(source_dir, target_dir, args.include, args.exclude, args.max_size):
        # Create README
        create_readme(target_dir, source_dir, kicad_version)
        logger.info("KiCad reference files copied successfully.")
        return 0
    else:
        logger.error("Failed to copy KiCad reference files.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
