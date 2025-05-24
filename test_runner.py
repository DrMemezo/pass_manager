import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from pyui.login_ui import Ui_MainWindow

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())

