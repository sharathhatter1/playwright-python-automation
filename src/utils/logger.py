import  os
import logging
from datetime import datetime

class Logger:
    @staticmethod
    def get_logger(name):
        # Create logs directory if it doesn't exist
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        # Configure logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        # Check if logger already has handlers to avoid duplicates
        if not logger.handlers:
            # File handler
            log_file = f"logs/{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Create formatter and add to handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger
 