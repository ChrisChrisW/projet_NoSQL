from flask import render_template, redirect, url_for
import os

from controller.mongo import delete_all_mongo
from controller.redis import insert_redis, delete_all_redis, get_all_redis
from controller.neo4j import insert_neo4j, delete_all_neo4j, get_all_neo4j
from controller.elasticsearch import insert_elasticsearch, delete_all_elasticsearch, get_all_elasticsearch

def insert_default_values():
    insert_redis()
    insert_neo4j()
    insert_elasticsearch()

    return redirect(url_for('index'))

def delete_all_data():
    delete_all_mongo()
    delete_all_redis()
    delete_all_neo4j()
    delete_all_elasticsearch()

    return redirect(url_for('index'))

def index():
    sorted_redis_data = get_all_redis()
    neo4j_data = get_all_neo4j()
    es_data = get_all_elasticsearch()

    return render_template('index.html', redis_data=sorted_redis_data, neo4j_data=neo4j_data, es_data=es_data,
                           spotify_clientId=os.getenv('spotify_clientId'), spotify_clientSecret=os.getenv('spotify_clientSecret'))
