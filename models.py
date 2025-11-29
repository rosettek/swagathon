from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SPUData(db.Model):
    __tablename__ = 'spu_data'

    id = db.Column(db.Integer, primary_key=True)
    spu_external_id = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    normalized_name = db.Column(db.Text)
    normalized_category = db.Column(db.Text)

    # Relationships
    category = db.relationship('Category', backref='spus')
    model = db.relationship('Model', backref='spus')
    manufacturer = db.relationship('Manufacturer', backref='spus')
    country = db.relationship('Country', backref='spus')
    characteristics = db.relationship('CharacteristicValue', secondary='spu_characteristics', backref='spus')

    def __repr__(self):
        return f'<SPUData {self.id}: {self.name}>'


# Для обратной совместимости с вашим кодом
STE = SPUData