import os
import re
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

def is_html_content(content: str) -> bool:
    """Check if content is HTML instead of Python code"""
    html_indicators = [
        '<!DOCTYPE html>',
        '<html',
        '<div class="Box-body">',
        'class="blob-code',
        '<table class="highlight">'
    ]
    return any(indicator in content for indicator in html_indicators)

def extract_python_from_html(content: str) -> str:
    """Extract Python code from HTML content using BeautifulSoup"""
    try:
        soup = BeautifulSoup(content, 'html.parser')
        # Try different common GitHub code containers
        code_elements = (
            soup.select('table.highlight td.blob-code') or
            soup.select('div.highlight pre') or
            soup.select('pre.code')
        )
        
        if code_elements:
            return '\n'.join(element.get_text() for element in code_elements)
    except Exception:
        pass
    return None

def download_raw_python_file(github_url: str) -> str:
    """Download raw Python content from GitHub URL"""
    # Convert regular GitHub URL to raw content URL
    raw_url = github_url.replace('github.com', 'raw.githubusercontent.com')
    raw_url = raw_url.replace('/blob/', '/')
    
    response = requests.get(raw_url)
    return response.text

def fix_examples_directory(directory: str = 'kicad_examples') -> Dict[str, List[str]]:
    """
    Scan directory for Python files containing HTML and fix them
    Returns dict of files processed and any errors
    """
    results = {
        'fixed': [],
        'errors': [],
        'skipped': []
    }
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.txt')):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if is_html_content(content):
                        # First try to extract GitHub URL
                        url_match = re.search(r'initial-path="([^"]+)"', content)
                        if url_match:
                            github_path = url_match.group(1)
                            github_url = f"https://github.com{github_path}"
                            python_content = download_raw_python_file(github_url)
                        else:
                            # Try to extract Python code directly from HTML
                            python_content = extract_python_from_html(content)
                        
                        if python_content:
                            # Save with .py extension
                            new_filepath = filepath.replace('.txt', '.py')
                            with open(new_filepath, 'w', encoding='utf-8') as f:
                                f.write(python_content)
                            results['fixed'].append(filepath)
                        else:
                            results['errors'].append(f"Could not extract Python code from {filepath}")
                    else:
                        results['skipped'].append(filepath)
                        
                except Exception as e:
                    results['errors'].append(f"Error processing {filepath}: {str(e)}")
    
    return results

if __name__ == '__main__':
    print("Installing required package...")
    os.system('pip install beautifulsoup4')
    
    print("\nFixing example files...")
    results = fix_examples_directory()
    
    print("\nFixed files:")
    for file in results['fixed']:
        print(f"- {file}")
        
    print("\nSkipped files (already Python):")
    for file in results['skipped']:
        print(f"- {file}")
        
    print("\nErrors:")
    for error in results['errors']:
        print(f"- {error}")
