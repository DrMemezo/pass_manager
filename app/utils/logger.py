import logging
from typing import Optional
from app.utils.paths import get_log_filepath

_configured_loggers = set()

def configure_logger(logger_name:Optional[str]=None, filename:Optional[str]=None, 
                     level:int=logging.DEBUG, 
                     format_str:str="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                     propogate:bool=True):
    """
    Configure a logger with a file handler
    Args:
        logger_name: Name of the logger. If None, configures root logger.
        filename: Log filename. If None, uses logger_name or 'app.log'
        level: Logging level
        format_string: Log message format
        propagate: Whether to propagate to parent loggers
    
    Returns:
        Configured logger instance    
    """

    logger = get_logger(logger_name)

    if logger_name in _configured_loggers:
        return logger
    
    logger.setLevel(level)
    logger.propagate = propogate 

    if filename is None:
        filename = f"{logger_name or 'app'}.log" 
    
    log_filepath = get_log_filepath(filename)
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(level)

    formatter = logging.Formatter(format_str)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    _configured_loggers.add(logger_name)

    return logger

def configure_SQLA_logging(filename:str="database.log"):
    """Configures logging for SQLAlchemy logs"""
    sqla_engine_logger = configure_logger( 
        logger_name='sqlalchemy.engine',
        filename=filename,
        level=logging.INFO,
        propogate=False 
    )

    sqla_orm_logger = configure_logger(
        logger_name='sqlalchemy.orm',
        filename=filename,
        level=logging.INFO,
        propogate=False
    )

    return sqla_engine_logger, sqla_orm_logger 

def get_logger(name:str|None=None) -> logging.Logger:
    """
    Get a logger instance. If the logger hasn't been configured yet,
    it will use the default Python logging configuration.
    """
    return logging.getLogger(name)
