from core import db
from core.base_model import BaseModel

class Property(BaseModel, db.Model):
    __tablename__ = 'properties'
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', lazy=True, back_populates='properties')
    images = db.relationship('Image', lazy=True, back_populates='property', cascade="all, delete, delete-orphan")
    
    
class Image(BaseModel, db.Model):
    __tablename__ = 'images'
    
    path = db.Column(db.String(500), unique=True, nullable=False)
    mime_type = db.Column(db.String(25), unique=True, nullable=False)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.ForeignKey('properties.id'), nullable=False)

    user = db.relationship('User', lazy=True, back_populates='images')
    property = db.relationship('Property', lazy=True, back_populates='images')
    