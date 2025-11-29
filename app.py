from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Инициализация приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tender-hack-kazan-secret'

# Настройка базы данных - используем PostgreSQL из переменных окружения
database_url = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                                          'ste_database.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Импорт моделей после инициализации db
from models import STE
from search_engine import SearchEngine

# Инициализация поискового движка
#search_engine = SearchEngine()
#search_engine.init_app(app, db)


@app.route('/')
def index():
    return render_template('index.html')

#
# @app.route('/search')
# def search():
#     query = request.args.get('q', '').strip()
#
#     # Получаем параметры фильтров
#     name_filter = request.args.get('name', '').strip()
#     model_filter = request.args.get('model', '').strip()
#     country_filter = request.args.get('country', '').strip()
#     manufacturer_filter = request.args.get('manufacturer', '').strip()
#     category_filter = request.args.get('category', '').strip()
#
#     # Подготавливаем словарь фильтров
#     filters = {}
#     if name_filter:
#         filters['name'] = name_filter
#     if model_filter:
#         filters['model'] = model_filter
#     if country_filter:
#         filters['country'] = country_filter
#     if manufacturer_filter:
#         filters['manufacturer'] = manufacturer_filter
#     if category_filter:
#         filters['category'] = category_filter
#
#     # Выполняем поиск с учетом фильтров
#     if query or filters:
#         results = search_engine.search(query, filters)
#     else:
#         results = []
#
#     return render_template('index.html', query=query, filters=filters, results=results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)