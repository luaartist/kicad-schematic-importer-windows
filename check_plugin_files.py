import os

def check_plugin_files():
    base_dir = r"C:\Users\walla\Documents\KiCad\9.0\3rdparty\plugins\enhanced_importer_v2"
    
    # Print all files in the directory and subdirectories
    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == '.':
            print(f"\nFiles in root directory:")
        else:
            print(f"\nFiles in {rel_path}:")
            
        for file in files:
            print(f"  - {file}")
            
        # Print empty directories
        empty_dirs = [d for d in dirs if not os.listdir(os.path.join(root, d))]
        if empty_dirs:
            print("  Empty directories:")
            for d in empty_dirs:
                print(f"  - {d}/")

if __name__ == "__main__":
    check_plugin_files()