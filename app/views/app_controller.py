from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from app.views.dashboard import DashboardView
from app.views.login import LoginView
from app.views.register import RegisterView

from app.models import DBManager, User, VaultItem, VaultItemURL

from app.utils.logger import configure_logger, configure_SQLA_logging
from app.utils.crypto_manager import CryptographyManager

import os
from functools import partial
from typing import Optional

class AppController(QMainWindow):
    def __init__(self, db_manager:DBManager, crp_manager:CryptographyManager):
        super().__init__()

        self.db_manager = db_manager
        self.crypto_manager = crp_manager
        self.current_user:Optional[User] = None

        self.setWindowTitle("Password Manager")
        self.resize(420, 340)
        
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Set logger:
        self.logger = configure_logger("app")
        configure_SQLA_logging()        

        # Define Views
        self.login_view = LoginView()
        self.register_view = RegisterView()
        self.dashboard_view = DashboardView()

        # * Connect signals to slots
        self.register_view.register_required.connect(self.handle_register) 
        self.register_view.switch_to_login.connect(partial(self.switch_to, self.login_view))

        self.login_view.login_required.connect(self.handle_login) 
        self.login_view.switch_to_register.connect(partial(self.switch_to, self.register_view))

        self.dashboard_view.logout_required.connect(self.handle_logout)
        self.dashboard_view.vi_added.connect(self.handle_vi_entry)

        # * --------

        # Add all views to the stack
        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.register_view)
        self.stack.addWidget(self.dashboard_view)

        self.stack.setCurrentWidget(self.register_view)

    def handle_login(self):

        username = self.login_view.get_username()
        password = self.login_view.get_password()

        with self.db_manager.get_session() as session: 
            user = self.db_manager.get_user(username, session)
            
            if not user or not self.crypto_manager.verify(password, user.master_hash):
                self.set_info_label("Incorrect username or password")
                return
            
            self.current_user = user
            self.crypto_manager.set_fernet(password, user.salt)

            password = None
            del password
        
        self.switch_to(self.dashboard_view)
        self.dashboard_view.set_UsernameLabel(username)
        
        # TODO: SHOW ALL OF THE USER ITEMS ON LOGIN 
        for vi in user.vault_items:
            self.dashboard_view.show_item(id=vi.item_id, 
                                        password=self.crypto_manager.decrypt_password(vi.encrypted_item),
                                        urls=[url.url for url in vi.urls],  
                                        username=vi.username)

    def handle_logout(self):
        self.crypto_manager.clear()
        self.current_user = None
        self.switch_to(self.login_view)
        self.dashboard_view.clear_table()

    def set_info_label(self, msg:str):
        """Sets the infoLabel widget for the current view"""
        current_view = self.stack.currentWidget()

        if hasattr(current_view, 'set_infoLabel') and callable(getattr(current_view, 'set_infoLabel')):
            current_view.set_infoLabel(msg)
        else:
            raise NotImplementedError(f"set_infoLabel method not implemented for {type(current_view).__name__}")
    
    def switch_to(self, new_view:QMainWindow):
        self.stack.setCurrentWidget(new_view)

    def handle_register(self):
        """ Validate and handle registration"""
    
        username = self.register_view.get_username()
        password = self.register_view.get_password()
        rentry = self.register_view.get_rentry()

        # * RULE 1: All fields must be filled in
        if not (username and password and rentry):
            self.set_info_label("All fields must be filled!")
            return
        
        # * RULE 2: Password must match rentry:
        if not (password == rentry):
            self.set_info_label("Password does not match rentry")
            return
        

        # * RULE 3: Username must be unique:
        with self.db_manager.get_session() as session:
            if session.query(User).filter_by(name=username).first():
                self.set_info_label("Username must be unique!")
                return
        
        # Add to database
        with self.db_manager.get_session() as session:
            new_user = User(name=username, master_hash=self.crypto_manager.hash(password), salt=os.urandom(16))
            try:
                session.add(new_user)
                session.commit()
            except Exception as e:
                self.logger.critical(f"AN ERROR OCCURED: {str(e)}")
                self.set_info_label("An internal error occured!")
                return

        self.switch_to(self.login_view)

        self.set_info_label("You are sucessfully registered! Please login")
        password = None
        del password

    def handle_vi_entry(self, data:dict[str]):
        """ Validates user data, and adds them to the database if valid """
        
        # TODO: ADD FEEDBACK FOR FORM DIALOG
        password:str = data['password']
        username:str = data['username']
        urls:list[str] = data['URL']
        
        # Validate data
        if len(password) < 5:
            print("Password is too weak")
            return
        

        if not urls:
            print("a URL must be given")
            return
        
        if not username:
            print(" WARNING: Username field is empty")

        with self.db_manager.get_session() as session:
            ciphertext = self.crypto_manager.encrypt_password(password)

            new_vi = VaultItem(encrypted_item=ciphertext, 
                               username=username, 
                               user_id=self.current_user.user_id,
                               urls=[]
                            )
            
            for url in urls:
                vi_url = VaultItemURL(url=url, item_id=new_vi.item_id, vault_item=new_vi)
                new_vi.urls.append(vi_url)

            session.add(new_vi)
            session.commit()
            print("DEBUG: Vault_Item added!!!")


    def run(self):
        self.show()



if __name__ == "__main__":
    pass