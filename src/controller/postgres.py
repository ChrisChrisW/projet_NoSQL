from flask import render_template, request, redirect, url_for
from databases.postgres import PostgresDB

# Création des instances de bd
postgres_db = PostgresDB()

def get_all_postgres():
    return postgres_db.get_items()

def insert_postgres():
    complex_postgres_data = [
        {'field1': 'Computer', 'field2': 'Intel Core i7'},
        {'field1': 'Monitor', 'field2': '27-inch 4K'},
        {'field1': 'Keyboard', 'field2': 'Mechanical'},
        {'field1': 'Monitor', 'field2': '32-inch 4K'},
        {'field1': 'Mouse', 'field2': 'Wireless'},
        {'field1': 'Printer', 'field2': 'Color LaserJet'},
    ]
    postgres_db.create_items(complex_postgres_data)

def submit_postgres():
    field1 = request.form['field1']
    field2 = request.form['field2']

    postgres_db.create_item(field1, field2)

    return redirect(url_for('index'))

def edit_postgres(item_id):
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            new_field1 = request.form['field1']
            new_field2= request.form['field2']
            postgres_db.edit_item(item_id, new_field1, new_field2)

            return redirect(url_for('index'))

    item = postgres_db.get_item_by_id(item_id)
    return render_template('postgres/edit.html', item=item)

def delete_postgres(item_id):
    if request.form.get('_method') == 'DELETE':
        if 'delete_postgres' in request.form:
            postgres_db.delete_item(item_id)

    return redirect(url_for('index'))

def delete_all_postgres():
    postgres_db.delete_items()