import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from pyui.login import Ui_MainWindow as LoginPage
from pyui.register import Ui_MainWindow as RegisterPage

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LoginPage()
        self.ui.setupUi(self)

        self.setWindowTitle("Login")

        # connect signals
        self.connect_signals()

    def connect_signals(self):
        """Connect widgets to custom slots"""

        self.ui.loginButton.clicked.connect(
            lambda : print(self.ui.usernameInput.text(), self.ui.passwordInput.text())
        )

class RegisterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = RegisterPage()
        self.ui.setupUi(self)

        self.setWindowTitle("Register")

        self.connect_signals()

    def connect_signals(self):
        self.ui.registerButton.clicked.connect(self.validate_inputs)

    def validate_inputs(self):
        username = self.ui.usernameInput.text()
        password = self.ui.passwordInput.text()
        double_entry = self.ui.renterPasswordInput.text()

        if not username:
            QMessageBox.information(self, "Error", "Username is required")
            return
        
        if not password:
            QMessageBox.information(self, "Error", "Password is required")
            return

        # TODO: Turn this back on in prod
        # if len(password) < 8:
        #     QMessageBox.information(self, "Error", "Password must be at least 8 characters long")
        #     return

        if password != double_entry:
            QMessageBox.information(self, "Error", "Passwords do not match")
            return
        
        QMessageBox.information(self, "Confirm", "Are you sure you want to go through with this?")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterApp()
    window.show()
    sys.exit(app.exec())

