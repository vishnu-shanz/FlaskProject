import uuid
from datetime import datetime
from app import db

class Product(db.Model):
    __tablename__ = 'product'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    
    movements = db.relationship('ProductMovement', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Location(db.Model):
    __tablename__ = 'location'
    
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    
    movements_from = db.relationship('ProductMovement', foreign_keys='ProductMovement.from_location', backref='from_loc', lazy=True)
    movements_to = db.relationship('ProductMovement', foreign_keys='ProductMovement.to_location', backref='to_loc', lazy=True)
    
    def __repr__(self):
        return f'<Location {self.name}>'

class ProductMovement(db.Model):
    __tablename__ = 'product_movement'
    
    movement_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<ProductMovement {self.movement_id}>'
    
    def get_movement_type(self):
        if self.from_location is None and self.to_location is not None:
            return 'IN'
        elif self.from_location is not None and self.to_location is None:
            return 'OUT'
        elif self.from_location is not None and self.to_location is not None:
            return 'TRANSFER'
        else:
            return 'UNKNOWN'
