from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSignal

from app.ui.compiled.login import Ui_MainWindow as LoginUI

class LoginView(QMainWindow):
    login_required = pyqtSignal()
    switch_to_register = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ui = LoginUI()
        self.ui.setupUi(self)
        self.ui.infoLabel.hide()

        self.ui.loginButton.clicked.connect(lambda : self.login_required.emit())
        self.ui.switchToRegisterButton.clicked.connect(lambda : self.switch_to_register.emit())


    def set_infoLabel(self, msg:str):
        self.ui.infoLabel.setText(msg)
        self.ui.infoLabel.adjustSize()
        self.ui.infoLabel.show()

    def get_username(self) -> str:
        return self.ui.usernameInput.text()

    def get_password(self) -> str:
        return self.ui.passwordInput.text()

    
