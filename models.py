"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base
from flask_login import UserMixin

# Restaurant Class
class Restaurant(Base):
    __tablename__="restaurant"
    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    address = Column("address", TEXT, nullable=False)

    # relationship between Food and Restaurant 
    food = relationship("Food", back_populates="restaurant")


    def __init__(self, name, address):
        self.name = name
        self.address = address

#User class
class User(UserMixin,Base):
    __tablename__="user"
    id = Column("id", INTEGER, primary_key=True)
    username = Column("username", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)
    role = Column("role", TEXT, nullable=False)
    # relationship between User and Food
    food = relationship("Food", back_populates="user")

    def __init__(self, username, password, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def is_admin(self):
        return self.role == 'a'
    
    def is_client(self):
        return self.role == 'c'

# Food class
class Food(Base):
    __tablename__="food"
    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    rst_id = Column("rst_id", ForeignKey("restaurant.id"))
    user_id = Column("user_id", ForeignKey("user.id"))

    # relationships between Food and User, and Restaurant and Food
    restaurant = relationship("Restaurant", back_populates="food")
    user = relationship("User", back_populates="food")

    def __init__(self, name, rst_id):
        self.name = name
        self.rst_id = rst_id

