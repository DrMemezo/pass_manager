from pathlib import Path

UTILS_FOLDER = Path(__file__).resolve().parent
APP_FOLDER = UTILS_FOLDER.parent
WORKSPACE_FOLDER = APP_FOLDER.parent

LOGS_FOLDER = WORKSPACE_FOLDER / "logs"
# TODO: After completing the business logic, change from storing locally to storing in the User-specific folder
DB_FOLDER = APP_FOLDER / "tests" 

def get_log_filepath(filename:str) -> Path:
    LOGS_FOLDER.mkdir(exist_ok=True)
    if filename[-4:] != ".log":
        raise ValueError("File must have the .log extension")
    return LOGS_FOLDER / filename

def get_db_filepath(filename:str) -> Path:
    DB_FOLDER.mkdir(exist_ok=True)
    if filename[-3:] != ".db":
        raise ValueError("File must have the .db extension")
    
    return DB_FOLDER / filename
