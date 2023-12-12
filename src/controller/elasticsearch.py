from flask import render_template, request, redirect, url_for
from databases.elasticsearch import ElasticsearchDB

# Création des instances de bd
es_db = ElasticsearchDB()

def send_message():
    data = request.get_json()
    return es_db.create_message(data)

def get_messages():
    return es_db.get_messages()

def delete_message():
    data = request.get_json()
    content = data.get('content')
    timestamp = data.get('timestamp')

    return es_db.delete(content, timestamp)

def delete_all_elasticsearch():
    es_db.delete_items()
