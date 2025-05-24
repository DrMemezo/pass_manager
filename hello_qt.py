import sys
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, 
    QMainWindow
    )
from PyQt6.QtCore import Qt

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.label = QLabel("<h1>Welcome to your password manager!</h1>", central_widget)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0,0, self.width(), self.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyMainWindow()
    window.show()

    sys.exit(app.exec())