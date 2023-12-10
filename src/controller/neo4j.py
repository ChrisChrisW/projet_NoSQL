from flask import render_template, request, redirect, url_for
from databases.neo4j import Neo4jDB

# Création des instances de bd
neo4j_db = Neo4jDB()

def get_all_neo4j():
    return neo4j_db.get_items()

def insert_neo4j():
    neo4j_db.create_item('Product1', 'A great product with amazing features.')
    neo4j_db.create_item('Product2', 'An innovative solution for your needs.')
    neo4j_db.create_item('Product3', 'High-quality and reliable product for professionals.')

def submit_neo4j():
    field1 = request.form['field1']
    field2 = request.form['field2']

    neo4j_db.create_item(field1, field2)

    return redirect(url_for('index'))

def edit_neo4j(item_id):
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            new_field1 = request.form['field1']
            new_field2 = request.form['field2']
            neo4j_db.edit_item(item_id, new_field1, new_field2)
            return redirect(url_for('index'))

    item = neo4j_db.get_item_by_id(item_id)
    return render_template('neo4j/edit.html', item=item)

def delete_neo4j(item_id):
    if request.form.get('_method') == 'DELETE':
        if 'delete_neo4j' in request.form:
            neo4j_db.delete_item(item_id)

    return redirect(url_for('index'))

def delete_all_neo4j():
    neo4j_db.delete_items()
