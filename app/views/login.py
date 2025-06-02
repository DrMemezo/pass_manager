from PyQt6.QtWidgets import QMainWindow
from typing import Callable

from app.ui.compiled.login import Ui_MainWindow as LoginUI

class LoginView(QMainWindow):
    def __init__(self, switch_function:Callable):
        super().__init__()

        self.ui = LoginUI()
        self.ui.setupUi(self)
        self.ui.loginButton.clicked.connect(self.handle_login)
        self.switch_to_register = switch_function

    def handle_login(self):
        self.switch_to_register()