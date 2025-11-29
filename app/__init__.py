# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Настройки из переменных окружения или по умолчанию
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:postgres@db:5432/tenderhack'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Инициализация расширений с приложением
    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрация маршрутов (если будут)
    from routes import main_bp
    app.register_blueprint(main_bp)

    return app