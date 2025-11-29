# /workspace/application/app.py
from flask import Flask, jsonify, render_template
from models import db, Brand, Model, Category, Characteristic, SpuData
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spu_data.db'
db.init_app(app)
with app.app_context():
    db.create_all()
@app.route('/api/brands')
def get_brands():
    return jsonify([{'id': b.id, 'name': b.name} for b in Brand.query.all()])

@app.route('/api/models')
def get_models():
    return jsonify([{'id': m.id, 'name': m.name} for m in Model.query.all()])

@app.route('/api/categories')
def get_categories():
    return jsonify([{'id': c.id, 'name': c.name} for c in Category.query.all()])

@app.route('/api/characteristics')
def get_characteristics():
    return jsonify([{'id': ch.id, 'name': ch.name} for ch in Characteristic.query.all()])

@app.route('/api/spu_ids')
def get_spu_ids():
    brand_id = request.args.get('brand_id')
    model_id = request.args.get('model_id')
    category_id = request.args.get('category_id')
    characteristic_id = request.args.get('spu_characteristics_id')

    query = SpuData.query

    if brand_id:
        query = query.filter_by(brand_id=brand_id)
    if model_id:
        query = query.filter_by(model_id=model_id)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if characteristic_id:
        query = query.filter_by(characteristic_id=characteristic_id)

    spu_ids = [spu.spu_id for spu in query.all()]
    return jsonify(spu_ids)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)