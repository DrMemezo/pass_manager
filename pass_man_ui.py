import sys 
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QMessageBox
)
from PyQt6.QtCore import Qt

class PasswordManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Manager 2")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        # * -- Form --
        form_layout = QGridLayout()

        # * row 0
        self.website_label = QLabel("Website: ")
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("e.g., google.com")
        form_layout.addWidget(self.website_label, 0, 0)
        form_layout.addWidget(self.website_input, 0, 1)

        # * row 1
        self.username_label = QLabel("Username: ")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("john@john.com")
        form_layout.addWidget(self.username_label, 1, 0)
        form_layout.addWidget(self.username_input, 1, 1)

        # * row 2
        self.password_label = QLabel("Password: ")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password:")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.password_label, 2, 0)
        form_layout.addWidget(self.password_input, 2, 1)

        form_layout.setRowStretch(3, 0)
        form_layout.setColumnStretch(2, 1)


        # * --- Buttons ----
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Entry")
        self.retrieve_button = QPushButton("Retreive Entry")
        self.edit_button = QPushButton("Edit Entry")
        self.delete_button = QPushButton("Delete Entry")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.retrieve_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        button_layout.addStretch(1)

        # * -- Connect signals ---
        self.add_button.clicked.connect(self.add_entry)
        self.retrieve_button.clicked.connect(self.retrieve_entry)
        self.edit_button.clicked.connect(self.edit_entry)
        self.delete_button.clicked.connect(self.delete_entry)

        # * --- Combine into main layout --
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)

    def add_entry(self):
        QMessageBox.information(self, "Success", "Entry added")

    def retrieve_entry(self):
        QMessageBox.information(self, "Success", "Entry retrieved")

    def edit_entry(self):
        QMessageBox.information(self, "Success", "Entry editted")

    def delete_entry(self):
        QMessageBox.information(self, "Success", "Entry deleted")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManagerUI()
    window.show()
    sys.exit(app.exec())