from core import db
from core.base_model import BaseModel
from properties.model import Property, Image


class User(db.Model, BaseModel):
    __tablename__ = 'users'
    
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    
    properties = db.relationship(Property, back_populates='user', lazy=True, cascade="all, delete, delete-orphan")
    images = db.relationship(Image, back_populates='user', lazy=True, cascade="all, delete, delete-orphan")
    
    def to_dict(self):
        return self.__dict__