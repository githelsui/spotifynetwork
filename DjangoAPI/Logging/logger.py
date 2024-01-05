import logging 
from .models import Log
from datetime import datetime
import hashlib

class Logger:
    def __init__(self):
        # self.publisher = Publisher()
        self.logger = logging.getLogger('system')
        self.console_handler = logging.StreamHandler()
        self.console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.log_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
        }
        self.categories = ['view','controller','manager','service','data access layer', 'cross-cutting concerns'] 
    
    # Saves log to database
    # Prints error & debug logs to console
    def log(self, message, log_level, category, operation, success=None, session_id=None, user_id=None):
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
        
        hashed_user = None
        if user_id !=None:
            hashed_user = hashlib.sha256(user_id.encode()).hexdigest()
        hashed_session = None
        if session_id != None:
            hashed_session = hashlib.sha256(session_id.encode()).hexdigest()
            
        # Get timestamp
        current_dt = datetime.now()
        formatted_dt = current_dt.strftime("%m-%d-%Y %H:%M:%S")
        
        # Log under any log_level saved to sqlite db
        log = Log(Message=message,LogLevel=log_level,Category=category,Timestamp=formatted_dt,Operation=operation,Success=success,UserId=hashed_user,SessionId=hashed_session)
        log.save()
        
        # Log under debug and error level saved saved to debug.log & printed to console
        if level == self.log_levels['debug'] or level == self.log_levels['error']:
            self.logger.log(level,message)
        
        status = True
        return status