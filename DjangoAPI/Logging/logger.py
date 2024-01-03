import logging 
from .models import Log
from datetime import datetime

class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.console_handler = logging.StreamHandler()
        self.console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.log_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
        }
        self.categories = ['view','controller','manager','service','data access layer'] #Logger names in Django 
    
        
    def log(self, message, log_level, category, operation, user_email):
        status = None 
        
        # Validate message parameter
        if len(message) > 200:
            raise ValueError(f"Invalid message: {message}. Exceeds 200 char limit.")

        # Validate the log level parameter
        if log_level.lower() not in self.log_levels:
            raise ValueError(f"Invalid log level: {log_level}. Supported levels: {', '.join(self.log_levels.keys())}")
        level = self.log_levels[log_level.lower()]
        
        # Validate category parameter
        if category.lower() not in self.categories:
            raise ValueError(f"Invalid category: {category}. Supported categories: {', '.join(self.categories)}")
        
        # Validate operation parameter
        if len(operation) > 50:
            raise ValueError(f"Invalid operation: {operation}. Exceeds 50 char limit.")
        
        # Get timestamp
        current_dt = datetime.now()
        formatted_dt = current_dt.strftime("%Y-%m-%d %H:%M:%S")
        
        # Create handler and formatter specific to log_level parameter
        self.console_handler.setLevel(level)
        self.console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(self.console_handler)
        self.logger.log(level, message)
        # Log being saved to sqlite db
        log = Log(Message=message,LogLevel=log_level,Category=category,Timestamp=formatted_dt,Operation=operation,UserEmail=user_email)
        log.save()
        status = True

        return status