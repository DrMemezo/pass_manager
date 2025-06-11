from PyQt6.QtWidgets import QApplication
import sys

from app.views.app_controller import AppController
from app.models import DBManager
from app.utils.crypto_manager import CryptographyManager

def main():
    DEBUG_MODE = "--debug" in sys.argv

    if DEBUG_MODE:
        print("SQL_ALCHEMY Logging is enabled")

    app = QApplication(sys.argv) 
    controller = AppController(
        DBManager("test.db", "app.log" if DEBUG_MODE else None),
        CryptographyManager()
        )
    
    controller.run()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()