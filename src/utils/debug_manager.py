import sys
import os
import logging
import time
import traceback
from pathlib import Path
from functools import wraps

class DebugManager:
    """Manages debugging and performance tracking for image processing"""
    
    def __init__(self):
        self.logger = logging.getLogger('ImageProcessDebugger')
        self.setup_logging()
        self.processing_times = {}
        self.current_process = None
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path(__file__).parent.parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / 'image_processing_debug.log'
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)
    
    def track_processing(self, func):
        """Decorator to track processing time and flow"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            process_name = func.__name__
            
            self.logger.debug(f"Starting {process_name}")
            self.logger.debug(f"Args: {args}")
            self.logger.debug(f"Kwargs: {kwargs}")
            
            try:
                result = func(*args, **kwargs)
                
                end_time = time.time()
                duration = end_time - start_time
                
                if process_name not in self.processing_times:
                    self.processing_times[process_name] = []
                self.processing_times[process_name].append(duration)
                
                self.logger.debug(f"Completed {process_name} in {duration:.2f} seconds")
                self.logger.debug(f"Result type: {type(result)}")
                
                # Log memory usage
                import psutil
                process = psutil.Process(os.getpid())
                mem_usage = process.memory_info().rss / 1024 / 1024  # in MB
                self.logger.debug(f"Memory usage: {mem_usage:.2f} MB")
                
                return result
                
            except Exception as e:
                self.logger.error(f"Error in {process_name}: {str(e)}")
                self.logger.error(traceback.format_exc())
                raise
                
        return wrapper

debug_manager = DebugManager()