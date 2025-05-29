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
        return f"<Address id={self.address_id!r}, email={self.email_address!r}, user={self.user!r}>"


engine = create_engine("sqlite:///app/tests/test.db", echo=True)
Base.metadata.create_all(engine)


if __name__ == "__main__":
    with Session(engine) as session:
        while True:
            option = input("1.Create User\n2.See all users\n3. Update user\n4. Delete user\n5. See all address \n6.Exit\n").strip()
            match option:
                case '1':
                    username = input("Enter name: ")
                    address = input("Enter email address: ")
                    new_user = User(name=username, 
                            addresses=[Address(email_address=address)]
                        )
                    # ? How do I add a the new user to the db?
                    session.add(new_user)
                    session.commit()
                case '2':
                    users = session.query(User).all()
                    for user in users:
                        print(user)
                case '3':
                    pass
                case '4':
                    pass
                case '5':
                    addresses = session.query(Address).all()
                    for address in addresses:
                        print(address)
                case '6':
                    break
                case _:
                    print("Invalid option")
                    continue

            input("---- Continue --- ")