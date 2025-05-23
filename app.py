from flask import Flask, render_template, request, abort
import json

app = Flask(__name__)


def load_menu():
    with open('restaurante_alberto.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        items = []
        for category in data[0]['restaurante']['menu']:
            for item in category['items']:
                item['categoria'] = category['categoria']
                items.append(item)
        return items, data[0]['restaurante']['menu']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buscador', methods=['GET'])
def buscador():
    _, categories = load_menu()
    category_names = [cat['categoria'] for cat in categories]
    return render_template('buscador.html', categories=category_names)

@app.route('/resultados', methods=['POST'])
def resultados():
    items, categories = load_menu()
    search_query = request.form.get('search', '').lower()
    selected_category = request.form.get('category', '')
    

    filtered_items = items
    if search_query:
        filtered_items = [item for item in filtered_items if item['nombre'].lower().startswith(search_query)]
    if selected_category:
        filtered_items = [item for item in filtered_items if item['categoria'] == selected_category]
    
    category_names = [cat['categoria'] for cat in categories]
    
    return render_template('resultados.html', 
                         items=filtered_items,
                         search_query=search_query,
                         selected_category=selected_category,
                         categories=category_names)


@app.route('/item/<id_item>')
def detail_item(id_item):
    items, _ = load_menu()
    item = next((item for item in items if item['id_item'] == id_item), None)
    
    if item is None:
        abort(404)
    
    return render_template('detail_item.html', item=item)

