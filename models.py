"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

class Restaurant(Base):
    __tablename__="restaurant"
    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    address = Column("address", TEXT, nullable=False)

    food = relationship("Food", back_populates="restaurant")


    def __init__(self, name, address):
        self.name = name
        self.address = address

class User(Base):
    __tablename__="user"
    id = Column("id", INTEGER, primary_key=True)
    username = Column("username", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)

    food = relationship("Food", back_populates="user")


    def __init__(self, username, password):
        self.username = username
        self.password = password


class Food(Base):
    __tablename__="food"
    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    rst_id = Column("rst_id", ForeignKey("restaurant.id"))
    user_id = Column("user_id", ForeignKey("user.id"))

    restaurant = relationship("Restaurant", back_populates="food")
    user = relationship("User", back_populates="food")

    def __init__(self, name, rst_id):
        self.name = name
        self.rst_id = rst_id

