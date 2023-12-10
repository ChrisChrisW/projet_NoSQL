from flask import render_template, request, redirect, url_for
from databases.redis import RedisDB

# Création des instances de bd
redis_db = RedisDB()

def get_all_redis():
    return redis_db.get_items_sorted()

def insert_redis():
    default_redis_data = {
        '0': '{"product_id": "P001", "name": "Laptop", "price": 1499.99}',
        '1': '{"product_id": "P002", "name": "Smartphone", "price": 799.99}',
        '2': '{"product_id": "P003", "name": "Headphones", "price": 129.99}',
        '3': '{"name": "Tablet", "price": 499.99, "brand": "Apple"}',
        '4': '{"name": "Desktop", "price": 1999.99, "brand": "HP"}',
        '5': '{"name": "Camera", "price": 599.99, "brand": "Canon"}',
        '6': '{"name": "Smartphone", "price": 399.99, "brand": "Samsung"}',
        '7': '{"name": "Laptop", "price": 899.99, "brand": "Dell"}',
        '8': '{"name": "Headphones", "price": 79.99, "brand": "Sony"}',
    }
    redis_db.create_items(default_redis_data)

def submit_redis():
    form = request.form
    redis_db.create_item(form)

    return redirect(url_for('index'))

def edit_redis(item_id):
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            new_field = request.form['field']
            redis_db.edit_item(item_id, new_field)
            return redirect(url_for('index'))

    item = redis_db.get_item_by_id(item_id)
    return render_template('redis/edit.html', field=item_id, item=item)

def delete_redis(item_id):
    if request.form.get('_method') == 'DELETE':
        if 'delete_redis' in request.form:
            redis_db.delete_item(item_id)

    return redirect(url_for('index'))

def delete_all_redis():
    redis_db.delete_items()