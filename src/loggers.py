# src/loggers.py
import logging
from utils import LOGS_FOLDER


def __setup_loggers(filename:str):

    logging.basicConfig(
        filename= LOGS_FOLDER.joinpath(filename).absolute(),
        level = logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    

    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)