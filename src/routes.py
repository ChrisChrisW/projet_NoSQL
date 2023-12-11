from flask import Flask

from controller.main import *
from controller.mongo import *
from controller.redis import *
from controller.postgres import *
from controller.neo4j import *
from controller.elasticsearch import *

app = Flask(__name__)

# Routes for main
app.route('/insert_default_values', methods=['POST'])(insert_default_values)
app.route('/delete_all_data', methods=['DELETE'])(delete_all_data)
app.route('/', methods=['GET'])(index)

# Routes for MongoDB - Spotify Playlist
app.route('/get_all_mongo_data', methods=['GET'])(get_all_mongo_data)
app.route('/submit_mongo', methods=['POST'])(submit_mongo)
app.route('/delete_mongo', methods=['DELETE', 'POST'])(delete_mongo)

# Routes for Redis
app.route('/submit_redis', methods=['POST'])(submit_redis)
app.route('/edit_redis/<item_id>', methods=['GET', 'POST'])(edit_redis)
app.route('/delete_redis/<item_id>', methods=['DELETE', 'POST'])(delete_redis)

# Routes for Postgres - Pokedex
app.route('/get_all_pokemon', methods=['GET'])(get_all_pokemon)
app.route('/update_pokemon_data', methods=['POST'])(update_pokemon_data)
app.route('/add_pokemon', methods=['POST'])(add_pokemon)
app.route('/update_pokemon/<pokemon_id>', methods=['PUT'])(update_pokemon)
app.route('/delete_pokemon/<pokemon_id>', methods=['DELETE'])(delete_pokemon)

# Routes for Neo4j
app.route('/submit_neo4j', methods=['POST'])(submit_neo4j)
app.route('/edit_neo4j/<item_id>', methods=['GET', 'POST'])(edit_neo4j)
app.route('/delete_neo4j/<item_id>', methods=['DELETE', 'POST'])(delete_neo4j)

# Routes for Elasticsearch
app.route('/submit_elasticsearch', methods=['POST'])(submit_elasticsearch)
app.route('/edit_elasticsearch/<item_id>', methods=['GET', 'POST'])(edit_elasticsearch)
app.route('/delete_elasticsearch/<item_id>', methods=['DELETE', 'POST'])(delete_elasticsearch)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
