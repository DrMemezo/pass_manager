from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import create_engine, ForeignKey
from typing import List


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User id={self.user_id!r}, name={self.name!r}>"

class Address(Base):
    __tablename__ = "address"
    address_id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"<Address id={self.address_id!r}, email={self.email_address!r}"


engine = create_engine("sqlite:///app/tests/test.db", echo=True)
Base.metadata.create_all(engine)


with Session(engine) as session:
    spongebob = User(name="spongebob", 
                     addresses=[Address(email_address="sponge@bob.com")])
    sandy = User(name="sandy",
                 addresses=[
                    Address(email_address="sandy@sqlalchemy.org"),
                    Address(email_address="sandy@squirrel.org")
                    ]
                )
    session.add_all([sandy, spongebob])
    session.commit()