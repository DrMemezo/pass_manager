from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from app.views.dashboard import DashboardView
from app.views.login import LoginView
from app.views.register import RegisterView

from app.models import DBManager, User

class AppController(QMainWindow):
    def __init__(self, db_manager:DBManager):
        super().__init__()

        self.db_manager = db_manager

        self.setWindowTitle("Password Manager")
        self.resize(420, 340)
        
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Define Views
        self.login_view = LoginView()
        self.register_view = RegisterView()
        self.dashboard_view = DashboardView()

        # Connect signals to slots
        self.register_view.register_required.connect(self.handle_register) 
        self.register_view.switch_to_login.connect(lambda : self.stack.setCurrentWidget(self.login_view))

        self.login_view.login_required.connect(self.handle_login) 
        self.login_view.switch_to_register.connect(lambda: self.stack.setCurrentWidget(self.register_view))

        # Add all views to the stack
        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.register_view)
        self.stack.addWidget(self.dashboard_view)

        self.stack.setCurrentWidget(self.login_view)

    def handle_login(self):

        def do_something_hash(x):
            raise NotImplementedError

        username = self.login_view.get_username()
        password = self.login_view.get_password()
        hashed = do_something_hash(password)
        with self.db_manager.get_session() as session: 
            user = session.query(User).filter_by(name=username, master_hash=password)

    

    def handle_register(self):
        """ Validate and handle registration"""
    
        username = self.register_view.get_username()
        password = self.register_view.get_password()
        rentry = self.register_view.get_rentry()

        # * RULE 1: All fields must be filled in
        if not (username and password and rentry):
            self.register_view.set_infoLabel("All fields must be filled!")
            return
        
        # * RULE 2: Password must match rentry:
        if not (password == rentry):
            self.register_view.set_infoLabel("Password does not match rentry")
            return
        

        # * RULE 3: Username must be unique:
        with self.db_manager.get_session() as session:
            if session.query(User).filter_by(name=username).first():
                self.register_view.set_infoLabel("Username must be unique!")
                return
        
        print("You are successfully registered! (not rlly)")



    def run(self):
        self.show()



if __name__ == "__main__":
    pass