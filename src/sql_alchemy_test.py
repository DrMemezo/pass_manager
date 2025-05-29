# src/sql_alchemy_test.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from src.utils import DB_FOLDER
from src.loggers import __setup_loggers

__setup_loggers("sqlalchemy.log")

engine = create_engine(f"sqlite:///{str(DB_FOLDER.joinpath("test.db").absolute())}")
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    
    addresses = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    street = Column(String)
    city = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="addresses")

Base.metadata.create_all(engine)


def insert_user(name:str, email:str) -> bool:
    if not name:
        raise ValueError("Name is empty!")
    
    if not email:
        raise ValueError("Email is empty!")

    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()

    return True

if __name__ == "__main__":
    username = input("Enter a username: ")
    email = input("Enter email: ")

    try:
        insert_user(username, email)
    except ValueError as e:
        print(str(e))
    except Exception as e:
        print("CRITICAL: " + str(e))    

