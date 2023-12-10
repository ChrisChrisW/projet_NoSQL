from flask import render_template, request, redirect, url_for
from databases.mongo import MongoDB

# Création des instances de bd
mongo_db = MongoDB()

def get_all_mongo_data():
    try:
        # Retrieving all data from MongoDB collection
        data = mongo_db.find_all()

        # Returning the data as a dictionary
        return {'status': 'success', 'data': data}

    except Exception as e:
        # Handling errors and returning an error message
        return {'status': 'error', 'message': str(e)}

def submit_mongo():
    data = request.get_json()
    mongo_db.create_item(data)

    return ({'status': 'success', 'message': 'Data received successfully'})

def delete_mongo():
    try:
        data = request.get_json()
        spotify_uri = data.get('spotify_uri')

        mongo_db.delete_item(spotify_uri)

        return ({'status': 'success', 'message': 'Track deleted successfully'})
    except Exception as e:
        return ({'status': 'error', 'message': str(e)})

def delete_all_mongo():
    mongo_db.delete_items()