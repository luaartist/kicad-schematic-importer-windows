import os
import yaml
import ast
from typing import Dict, List, Set
from collections import defaultdict

def format_section(title: str, items: Set[str]) -> str:
    """Format a section of the report with sorted items"""
    section = f"\n{title}\n{'-' * len(title)}\n"
    
    if not items:
        section += "None found\n"
    else:
        for item in sorted(items):
            section += f"- {item}\n"
    
    return section

def preprocess_yaml_content(content: str) -> str:
    """
    Preprocess YAML content by replacing placeholders with default values
    """
    # Common KiBot placeholders and their default values
    placeholders = {
        '@_KIBOT_IMPORT_DIR@': './import',
        '@_KIBOT_MANF_DIR@': './manufacturing',
        '@_KIBOT_CHKZONE_THRESHOLD@': '0.5',
        '@LAYERS@': 'F.Cu,B.Cu',
        '@ID@': 'default',
        '@UNITS@': 'millimeters'
    }
    
    # Replace all placeholders
    for placeholder, default_value in placeholders.items():
        content = content.replace(placeholder, default_value)
    
    return content

def analyze_yaml_files(directory: str) -> Dict[str, List[str]]:
    """
    Analyze YAML files in the directory for common issues
    Returns a dictionary of issues categorized by type
    """
    issues = {
        'version_issues': [],
        'filter_issues': [],
        'output_issues': [],
        'structure_issues': [],
        'placeholder_warnings': []  # New category for placeholder warnings
    }
    
    if not os.path.exists(directory):
        return issues
        
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.kibot.yaml'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for placeholders and record warnings
                    if '@' in content:
                        issues['placeholder_warnings'].append(
                            f"Found placeholders in {filepath} - using default values")
                    
                    # Preprocess content before parsing
                    processed_content = preprocess_yaml_content(content)
                    data = yaml.safe_load(processed_content)
                    
                    if not data:
                        continue
                        
                    # Check version
                    if 'kibot' in data and 'version' in data['kibot']:
                        if data['kibot']['version'] != 1:
                            issues['version_issues'].append(
                                f"Invalid version in {filepath}: {data['kibot']['version']}")
                    
                    # Check filters
                    if 'filters' in data:
                        for filter_item in data['filters']:
                            if isinstance(filter_item, dict) and 'type' not in filter_item:
                                issues['filter_issues'].append(
                                    f"Filter missing type in {filepath}: {filter_item.get('name', 'unnamed')}")
                    
                    # Check outputs
                    if 'outputs' in data:
                        for output in data['outputs']:
                            if isinstance(output, dict) and 'type' not in output:
                                issues['output_issues'].append(
                                    f"Output missing type in {filepath}: {output.get('name', 'unnamed')}")

                    # Check for Python scripts in outputs
                    if 'outputs' in data:
                        for output in data['outputs']:
                            if isinstance(output, dict) and output.get('type') == 'python':
                                script_path = output.get('script')
                                if script_path and os.path.exists(script_path):
                                    script_issues = analyze_python_file(script_path)
                                    if script_issues['plugin_patterns']:
                                        issues['structure_issues'].append(
                                            f"Python script {script_path} contains plugin patterns")
                                    if not script_issues['kicad_imports']:
                                        issues['structure_issues'].append(
                                            f"Python script {script_path} lacks KiCad imports")
                                
                except yaml.YAMLError as e:
                    issues['structure_issues'].append(f"YAML parsing error in {filepath}: {str(e)}")
                except Exception as e:
                    issues['structure_issues'].append(f"Error processing {filepath}: {str(e)}")
    
    return issues

def fix_yaml_files(directory: str, issues: Dict[str, List[str]]) -> None:
    """
    Apply fixes to YAML files based on identified issues
    Creates backup files before making changes
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.kibot.yaml'):
                filepath = os.path.join(root, file)
                try:
                    # Read original content
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for placeholders and preprocess
                    if '@' in content:
                        processed_content = preprocess_yaml_content(content)
                        data = yaml.safe_load(processed_content)
                    else:
                        data = yaml.safe_load(content)
                    
                    if not data:
                        continue
                    
                    modified = False
                    
                    # Fix version issues
                    if 'kibot' in data and 'version' in data['kibot']:
                        if data['kibot']['version'] != 1:
                            data['kibot']['version'] = 1
                            modified = True
                    
                    # Fix filter issues
                    if 'filters' in data:
                        for filter_item in data['filters']:
                            if isinstance(filter_item, dict) and 'type' not in filter_item:
                                filter_item['type'] = 'basic'  # Default type
                                modified = True
                    
                    if modified:
                        # Create backup
                        backup_path = filepath + '.bak'
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        # Write fixed content
                        with open(filepath, 'w', encoding='utf-8') as f:
                            yaml.dump(data, f, sort_keys=False)
                        
                except Exception as e:
                    print(f"Error fixing {filepath}: {str(e)}")

def analyze_python_file(filepath: str) -> Dict[str, Set[str]]:
    """Analyze a Python file for classes, functions, imports and plugin patterns"""
    results = {
        'classes': set(),
        'functions': set(),
        'imports': set(),
        'plugin_patterns': set(),
        'kicad_imports': set()
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
            
        for node in ast.walk(tree):
            # Find classes
            if isinstance(node, ast.ClassDef):
                results['classes'].add(node.name)
                # Check for plugin patterns
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        if 'Plugin' in base.id or 'Action' in base.id:
                            results['plugin_patterns'].add(f"{node.name} ({base.id})")
            
            # Find functions
            elif isinstance(node, ast.FunctionDef):
                results['functions'].add(node.name)
                # Check for special plugin methods
                if node.name in ['Run', 'register', 'defaults']:
                    results['plugin_patterns'].add(f"method: {node.name}")
            
            # Find imports
            elif isinstance(node, ast.Import):
                for name in node.names:
                    results['imports'].add(name.name)
                    if 'kicad' in name.name.lower() or 'pcbnew' in name.name.lower():
                        results['kicad_imports'].add(name.name)
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ''
                for name in node.names:
                    results['imports'].add(f"{module}.{name.name}")
                    if 'kicad' in module.lower() or 'pcbnew' in module.lower():
                        results['kicad_imports'].add(f"{module}.{name.name}")
                
    except Exception as e:
        print(f"Error analyzing {filepath}: {str(e)}")
        
    return results

def print_section(title: str, items: Set[str]) -> None:
    """Print a formatted section of results"""
    print(f"\n{title}")
    print("-" * len(title))
    if items:
        for item in sorted(items):
            print(f"- {item}")
    else:
        print("None found")

def analyze_examples():
    """Analyze all Python files in the kicad_examples directory"""
    total_stats = defaultdict(set)
    plugin_files = []
    
    print("Analyzing KiCad examples...")
    print("=" * 50)
    
    for root, _, files in os.walk('kicad_examples'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                results = analyze_python_file(filepath)
                
                # Check if this looks like a plugin file
                if results['plugin_patterns']:
                    plugin_files.append(filepath)
                    print(f"\nPotential Plugin Found: {filepath}")
                    print_section("Plugin Patterns", results['plugin_patterns'])
                    print_section("KiCad Imports", results['kicad_imports'])
                
                # Aggregate total stats
                for key, values in results.items():
                    total_stats[key].update(values)
    
    print("\nOverall Analysis")
    print("=" * 50)
    print(f"Total files analyzed: {len(plugin_files)}")
    print("\nPlugin Files Found:")
    for filepath in plugin_files:
        print(f"- {filepath}")
    
    print("\nCommon Patterns:")
    print_section("Common KiCad Imports", total_stats['kicad_imports'])
    print_section("Common Plugin Patterns", total_stats['plugin_patterns'])

if __name__ == '__main__':
    analyze_examples()
