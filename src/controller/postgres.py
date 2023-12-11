from flask import render_template, request, redirect, url_for, jsonify
from databases.postgres import PostgresDB

# Création des instances de bd
postgres_db = PostgresDB()

def get_all_pokemon():
    try:
        # Retrieving all data from MongoDB collection
        data = postgres_db.find_all()
        # Returning the data as a dictionary
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        # Handling errors and returning an error message
        return {'status': 'error', 'message': str(e)}

def update_pokemon_data():
    return postgres_db.update_pokemon_data()

def add_pokemon():
    data = request.get_json()
    postgres_db.add_data(data)
    return jsonify({'message': 'Pokemon added successfully'})

def update_pokemon(pokemon_id):
    try:
        data = request.get_json()
        postgres_db.update_data(pokemon_id, data)

        return jsonify({'status': 'success', 'Message': 200})
    except Exception as e:
        # Handling errors and returning an error message
        return {'status': 'error', 'message': str(e)}
    
def delete_pokemon(pokemon_id):
    postgres_db.delete(pokemon_id)
    return jsonify({'message': 'Pokemon deleted successfully'})