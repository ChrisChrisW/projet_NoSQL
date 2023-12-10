from flask import render_template, request, redirect, url_for
from databases.elasticsearch import ElasticsearchDB

# Création des instances de bd
es_db = ElasticsearchDB()

def get_all_elasticsearch():
    return es_db.get_items()

def insert_elasticsearch():
    default_elasticsearch_data = [
        {'field1': 'ProductA', 'field2': 'High-performance gadget for tech enthusiasts.'},
        {'field1': 'ProductB', 'field2': 'Fashionable accessory with cutting-edge design.'},
        {'field1': 'ProductC', 'field2': 'Innovative solution for everyday convenience.'},
    ]
    es_db.create_items(default_elasticsearch_data)

def submit_elasticsearch():
    field1 = request.form['field1']
    field2 = request.form['field2']

    es_db.create_item(field1, field2)

    return redirect(url_for('index'))

def edit_elasticsearch(item_id):
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            new_field1 = request.form['field1']
            new_field2 = request.form['field2']
            es_db.edit_item(item_id, new_field1, new_field2)
            return redirect(url_for('index'))

    es_data = es_db.get_item_by_id(item_id)
    return render_template('elasticsearch/edit.html', es_data=es_data)

def delete_elasticsearch(item_id):
    if request.form.get('_method') == 'DELETE':
        if 'delete_es' in request.form:
            es_db.delete_item(item_id)

    return redirect(url_for('index'))

def delete_all_elasticsearch():
    es_db.delete_items()
