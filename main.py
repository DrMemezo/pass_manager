from PyQt6.QtWidgets import QApplication
import sys

# * Custom imports
from app.models import Base, User, VaultItem, DBManager
from app.utils.paths import get_db_filepath

from app.tests.testqt import AppController

def main():
    
    db_man = DBManager(get_db_filepath("test.db"))

    db_man.logger.info("App starting...")
    db_man.logger.info(f"Database created")

    app = QApplication(sys.argv)
    controller = AppController()
    controller.run()

    # Actual session
    test_session(db_man) 

    sys.exit(app.exec())

# TODO: Integrate with QT
def test_session(db_man:DBManager):

    session = db_man.get_session()
    result = session.query(User).all()

    print(result)

if __name__ == "__main__":
    main()