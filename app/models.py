# app/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import TEXT

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(TEXT, primary_key=True)
    name = db.Column(db.Text, nullable=False)

class Model(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

class Manufacturer(db.Model):
    __tablename__ = 'manufacturers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

class CharacteristicKey(db.Model):
    __tablename__ = 'characteristic_keys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.Text, nullable=False, unique=True)

class CharacteristicValue(db.Model):
    __tablename__ = 'characteristic_values'
    id = db.Column(db.Integer, primary_key=True)
    key_id = db.Column(db.Integer, db.ForeignKey('characteristic_keys.id'), nullable=False)
    value_text = db.Column(db.Text, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))

    key = db.relationship("CharacteristicKey", backref="values")
    unit = db.relationship("Unit", backref="values")

class STE(db.Model):
    __tablename__ = 'stes'
    id = db.Column(db.Integer, primary_key=True)
    ste_external_id = db.Column(TEXT, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)
    category_id = db.Column(TEXT, db.ForeignKey('categories.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    normalized_name = db.Column(db.Text)
    normalized_category = db.Column(db.Text)

    category = db.relationship("Category")
    model = db.relationship("Model")
    manufacturer = db.relationship("Manufacturer")
    country = db.relationship("Country")

# Связь многие-ко-многим
ste_characteristics = db.Table(
    'ste_characteristics',
    db.Column('ste_id', db.Integer, db.ForeignKey('stes.id'), primary_key=True),
    db.Column('char_value_id', db.Integer, db.ForeignKey('characteristic_values.id'), primary_key=True)
)