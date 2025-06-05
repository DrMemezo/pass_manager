import logging
from app.utils.paths import get_log_filepath


def _configure_SQLA_logging(filename:str):
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        [logger.removeHandler(handler) for handler in logger.handlers]

    # file handler
    log_filepath = get_log_filepath(filename)
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Configuring SQLA logger
    sqla_engine_logger = logging.getLogger('sqlalchemy.engine')
    sqla_engine_logger.setLevel(logging.INFO)
    sqla_orm_logger = logging.getLogger('sqlalchemy.orm')
    sqla_orm_logger.setLevel(logging.INFO)

def get_logger(name:str|None=None) -> logging.Logger:
    return logging.getLogger(name)
