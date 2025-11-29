# /workspace/application/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    spu_data = db.relationship('SpuData', backref='brand', lazy=True)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    spu_data = db.relationship('SpuData', backref='model', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    spu_data = db.relationship('SpuData', backref='category', lazy=True)

class Characteristic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    spu_data = db.relationship('SpuData', backref='characteristic', lazy=True)

class SpuData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spu_id = db.Column(db.String(50), nullable=False, unique=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    characteristic_id = db.Column(db.Integer, db.ForeignKey('characteristic.id'), nullable=False)