import logging
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CodeChangeMonitor(FileSystemEventHandler):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            self.logger.addHandler(handler)

    def on_modified(self, event):
        if not event.is_directory:
            self.logger.info(f"File modified: {event.src_path}")
            self._analyze_changes(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.logger.info(f"File created: {event.src_path}")
            self._analyze_changes(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.logger.warning(f"File deleted: {event.src_path}")

    def _analyze_changes(self, file_path):
        """Analyze file changes for potential issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for common issues
            self._check_syntax(file_path, content)
            self._check_dependencies(file_path, content)
            self._check_resource_usage(file_path, content)
            
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {str(e)}")

    def _check_syntax(self, file_path, content):
        """Check for syntax errors"""
        if file_path.endswith('.py'):
            try:
                compile(content, file_path, 'exec')
            except SyntaxError as e:
                self.logger.error(f"Syntax error in {file_path}: {str(e)}")

    def _check_dependencies(self, file_path, content):
        """Check for dependency issues"""
        import_keywords = ['import ', 'from ']
        for line in content.split('\n'):
            line = line.strip()
            if any(keyword in line for keyword in import_keywords):
                self.logger.info(f"Found dependency in {file_path}: {line}")

    def _check_resource_usage(self, file_path, content):
        """Check for potential resource issues"""
        resource_keywords = [
            'open(', 
            'with open',
            'subprocess.', 
            'threading.',
            'multiprocessing'
        ]
        
        for line_num, line in enumerate(content.split('\n'), 1):
            for keyword in resource_keywords:
                if keyword in line:
                    self.logger.info(
                        f"Resource usage found in {file_path}:{line_num} - {line.strip()}"
                    )

def start_monitoring(path="."):
    """Start monitoring code changes"""
    event_handler = CodeChangeMonitor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()