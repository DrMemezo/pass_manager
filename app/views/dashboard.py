from PyQt6.QtWidgets import QMainWindow

from app.ui.compiled.dashboard import Ui_MainWindow as DashboardUI


class DashboardView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.ui = DashboardUI()
        self.ui.setupUi(self)
        self.ui.UsernameLabel.setText("<h2>lalalala</h2>")
    
    def setUsernameLabel(self, text:str):
        self.ui.UsernameLabel.setText(f"<h2>{text}</h2>")
