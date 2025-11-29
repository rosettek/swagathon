from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tender-hack-kazan-secret'

# Пока без базы и поиска — только UI
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    # Позже здесь будет вызов search_engine.search(query)
    return render_template('index.html', query=query)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)