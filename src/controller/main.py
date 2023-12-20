from flask import render_template, redirect, url_for
import os

# from controller.mongo import delete_all_mongo
from controller.redis import delete_all_redis
from controller.elasticsearch import delete_all_elasticsearch

def insert_default_values():
    return redirect(url_for('index'))

def delete_all_data():
    # delete_all_mongo()
    delete_all_redis()
    delete_all_elasticsearch()

    return redirect(url_for('index'))

def index():

    return render_template('index.html',
                           spotify_clientId=os.getenv('spotify_clientId'), spotify_clientSecret=os.getenv('spotify_clientSecret'))
