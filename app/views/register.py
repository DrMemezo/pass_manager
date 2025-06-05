from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSignal
from typing import Callable, Optional

from app.ui.compiled.register import Ui_MainWindow as RegisterUI

class RegisterView(QMainWindow):
    register_required = pyqtSignal()
    switch_to_login = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ui = RegisterUI()
        self.ui.setupUi(self)
        self.ui.registerButton.clicked.connect(lambda : self.register_required.emit())
        self.ui.switchToLoginButton.clicked.connect(lambda : self.switch_to_login.emit())

        self.ui.infoLabel.hide()

    def get_username(self) -> str:
        return self.ui.usernameInput.text()

    def get_password(self) -> str:
        return self.ui.passwordInput.text()
    
    def get_rentry(self) -> str:
        return self.ui.renterPasswordInput.text()
    
    def set_infoLabel(self, msg:str):
        self.ui.infoLabel.setText(msg)
        self.ui.infoLabel.adjustSize()
        self.ui.infoLabel.show()
