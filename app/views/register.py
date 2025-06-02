from PyQt6.QtWidgets import QMainWindow
from typing import Callable

from app.ui.compiled.register import Ui_MainWindow as RegisterUI

class RegisterView(QMainWindow):
    def __init__(self, switch_function:Callable):
        super().__init__()

        self.ui = RegisterUI()
        self.ui.setupUi(self)
        self.ui.registerButton.clicked.connect(self.handle_register)
        self.switch_to_login = switch_function

    def handle_register(self):
        self.switch_to_login()