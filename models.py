from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class STE(db.Model):
    __tablename__ = 'spu_data'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)  # id сте
    name = db.Column(db.String(500))  # название сте
    image_url = db.Column(db.String(500))  # ссылка на картинку сте
    model = db.Column(db.String(200))  # модель
    country = db.Column(db.String(100))  # страна происхождения
    manufacturer = db.Column(db.String(200))  # производитель
    category_id = db.Column(db.Integer)  # id категории
    category_name = db.Column(db.String(200))  # название категории
    characteristics = db.Column(db.Text)  # характеристики
    
    def __repr__(self):
        return f'<STE {self.id}: {self.name}>'