import logging
from django.db.backends import BaseDatabaseWrapper
from .models import Log
from datetime import datetime

class CustomDatabaseHandler(logging.Handler, BaseDatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.log_levels = {
        # 'debug': logging.DEBUG,
        # 'info': logging.INFO,
        # 'warning': logging.WARNING,
        # 'error': logging.ERROR,
        # 'critical': logging.CRITICAL,
        # }
        # self.categories = ['view','controller','manager','service','data access layer'] #Logger names in Django 
    

    def emit(self, record):
        if record.name != 'django.db.backends':
            # Only log database-related messages
            return
        
        # Get log data
        message = self.format(record)
        log_level = record.levelname
        operation = getattr(record, 'operation', '')
        category = getattr(record, 'category', '')
        user = getattr(record, 'user', '')
        current_dt = datetime.now()
        formatted_dt = current_dt.strftime("%Y-%m-%d %H:%M:%S")
        
        # Validate message parameter
        if len(message) > 200:
            raise ValueError(f"Invalid message: {message}. Exceeds 200 char limit.")

        # # Validate the log level parameter
        # if log_level.lower() not in self.log_levels:
        #     raise ValueError(f"Invalid log level: {log_level}. Supported levels: {', '.join(self.log_levels.keys())}")
        # level = self.log_levels[log_level.lower()]
        
        # # Validate category parameter
        # if category.lower() not in self.categories:
        #     raise ValueError(f"Invalid category: {category}. Supported categories: {', '.join(self.categories)}")
        
        # Validate operation parameter
        if len(operation) > 50:
            raise ValueError(f"Invalid operation: {operation}. Exceeds 50 char limit.")

        log_entry = Log(
            Message=message,
            LogLevel=log_level,
            Operation=operation,
            Category=category,
            Timestamp=formatted_dt,
            UserEmail=user
        )
        log_entry.save()