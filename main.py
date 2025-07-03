from PyQt6.QtWidgets import QApplication
import sys

from app.views.app_controller import AppController
from app.models import DBManager
from app.utils.crypto_manager import CryptographyManager

def main():   
    
    app = QApplication(sys.argv) 
    controller = AppController(
        DBManager("test.db"),
        CryptographyManager()
        )
    
    controller.run()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()