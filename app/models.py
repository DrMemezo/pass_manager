from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker
from sqlalchemy import ForeignKey, create_engine
from typing import List, Optional
from pathlib import Path

from app.utils.logger import _configure_SQLA_logging, get_logger

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    master_hash: Mapped[str] # * Hashed 

    vault_items: Mapped[List["VaultItem"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User: {self.user_id!r}, Name: {self.name!r}>"
    
class VaultItem(Base):
    __tablename__ = "vaultitems"

    item_id: Mapped[int] = mapped_column(primary_key=True)
    encrypted_item: Mapped[str]
    username: Mapped[Optional[str]] # * Username may not be entered
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))

    owner: Mapped["User"] = relationship(back_populates="vault_items")
    urls: Mapped[List["VaultItemURL"]] = relationship( # * There can be multiple urls for a single password
        back_populates="vault_item", cascade="all, delete-orphan"
    ) 

class VaultItemURL(Base):
    __tablename__ = "urls"

    url_id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    item_id: Mapped[int] = mapped_column(ForeignKey("vaultitems.item_id"))

    vault_item: Mapped[VaultItem] = relationship(back_populates="urls")

class DBManager:
    def __init__(self, uri:Path, log_file:Optional[str]=None):

        # Configure logging
        _configure_SQLA_logging(log_file if log_file else "app.log")
        self.logger = get_logger(__name__)

        # Configure engine
        self.engine = create_engine(f"sqlite:///{uri}", echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine) 

    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)