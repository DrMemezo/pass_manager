# * src/utils.py
import pathlib

WORKSPACE_FOLDER = pathlib.Path(__file__).parent.parent
LOGS_FOLDER = WORKSPACE_FOLDER.joinpath("logs")
DB_FOLDER = WORKSPACE_FOLDER.joinpath("database")
