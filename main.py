from sqlalchemy.orm import Session
from sqlalchemy import create_engine, ForeignKey, Engine

# * Custom imports
from app.models import Base, User, VaultItem
from app.utils.logger import __configure_SQLA_logging, get_logger
from app.utils.paths import get_db_filepath

from app.ui.compiled.register import Ui_MainWindow as RegisterWindow
from app.ui.compiled.login import Ui_MainWindow as LoginWindow



def main():
    # Configure logging    
    __configure_SQLA_logging("app.log")
    app_logger = get_logger(__name__)

    app_logger.info("App starting...")
    # Configure database

    db_file = get_db_filepath("test.db")
    engine = create_engine(f"sqlite:///{db_file}", echo=False)
    # Create database (if not already)
    Base.metadata.create_all(engine)
    app_logger.info(f"Database created")

    # Actual session
    test_session(engine)

# TODO: Integrate with QT
def test_session(engine:Engine):

    with Session(engine) as session:
        pass


if __name__ == "__main__":
    main()