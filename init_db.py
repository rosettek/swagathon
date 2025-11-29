from app import app, db

# Создание таблиц в базе данных
with app.app_context():
    db.create_all()
    
print("Таблицы в базе данных созданы.")