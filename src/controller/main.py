from flask import render_template, redirect, url_for
import os

from controller.mongo import delete_all_mongo
from controller.redis import delete_all_redis
from controller.neo4j import insert_neo4j, delete_all_neo4j, get_all_neo4j

def insert_default_values():
    insert_neo4j()

    return redirect(url_for('index'))

def delete_all_data():
    delete_all_mongo()
    delete_all_redis()
    delete_all_neo4j()

    return redirect(url_for('index'))

def index():
    neo4j_data = get_all_neo4j()

    return render_template('index.html', neo4j_data=neo4j_data,
                           spotify_clientId=os.getenv('spotify_clientId'), spotify_clientSecret=os.getenv('spotify_clientSecret'))
