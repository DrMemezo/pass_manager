from PyQt6.QtWidgets import QMainWindow, QHeaderView, QDialog, QTableWidgetItem, QComboBox
from PyQt6.QtCore import pyqtSignal
from typing import Optional


from app.ui.compiled.dashboard import Ui_MainWindow as DashboardUI
from app.ui.compiled.dialog import Ui_Dialog as DialogUI



class FormDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = DialogUI()
        self.ui.setupUi(self)
        self.remove_placeholders()

        self.ui.saveButton.clicked.connect(self.accept)
        # Reject is called if the user exits via the 'X".


    def get_form_data(self) -> dict[str, str]:
        """Returns the inputs from the modal form at the time of function being called"""
        return {
            "password": self.ui.passwordInput.text(),
            "username": self.ui.usernameInput.text(),
            "URL": self.ui.URLInput.text()
        }
    
    def clear_all(self):
        self.ui.passwordInput.clear()
        self.ui.usernameInput.clear()
        self.ui.URLInput.clear()


    def remove_placeholders(self):
        self.ui.passwordLabel.setText("Enter Password")
        self.ui.URLLabel.setText("Enter URL")
        self.ui.usernameLabel.setText("Enter username") 

class DashboardView(QMainWindow):
    logout_required = pyqtSignal()
    vi_added = pyqtSignal(dict)
    vi_editted = pyqtSignal()
    vi_deleted = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.ui = DashboardUI()
        self.ui.setupUi(self)

        # * CONFIGURING TABLES
        self.ui.VaultTable.setHorizontalHeaderLabels(["ID","Password","URL","Username","Edit"])
        self.ui.VaultTable.setColumnHidden(0, True)

        self.ui.VaultTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)        

        # table_width = self.ui.VaultTable.width()
        # self.ui.VaultTable.setColumnWidth(0, table_width//4)
        # self.ui.VaultTable.setColumnWidth(1, table_width//4)
        # self.ui.VaultTable.setColumnWidth(2, table_width//4)
        # self.ui.VaultTable.setColumnWidth(3, table_width//4)
        # * -------

        # * CONNECTING SIGNALS
        self.ui.logoutButton.clicked.connect(lambda: self.logout_required.emit())
        self.ui.addButton.clicked.connect(self.on_add) 
        self.ui.removeButton.clicked.connect(lambda: print("minus button clicked")) 
        self.ui.editButton.clicked.connect(lambda: print("edit button clicekd"))

        # * -----

        self.ui.UsernameLabel.setText("<h2>Placeholder</h2>")
    
    def set_UsernameLabel(self, text:str):
        self.ui.UsernameLabel.setText(f"<h2>{text}</h2>")

    def show_item(self, id:int, password:str, urls:list[str], username:Optional[str]): 
        """Shows the following information as a row in the vaultTable """
        row_position = self.ui.VaultTable.rowCount()
        self.ui.VaultTable.insertRow(row_position)

        # * Col 0 (hidden)
        id_item = QTableWidgetItem(str(id))
        self.ui.VaultTable.setItem(row_position, 0, id_item)

        # * Col 1 Passwords
        password_item = QTableWidgetItem(password)
        self.ui.VaultTable.setItem(row_position, 1, password_item)

        # * Col 2 URLs
        url_combo = QComboBox(self) # ? What would be the appropriate parent for this widget?
        for url in urls:
            url_combo.addItem(url)
        self.ui.VaultTable.setCellWidget(row_position, 2, url_combo)

    def on_add(self): 
        dialog = self.setupDialog()

        dialog.setWindowTitle("Add new entry")
        dialog.ui.optionLabel.setText("Add new password")


        if dialog.exec():
            data = dialog.get_form_data()
            self.vi_added.emit(data) 
        # else:
        #     print("User closed....")




    def setupDialog(self) -> FormDialog:
        """Creates and clears the dialog"""
        dialog = FormDialog(parent=self)
        dialog.clear_all()

        return dialog
