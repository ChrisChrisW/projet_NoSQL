from flask import Flask

from controller.main import *
from controller.mongo import *
# from controller.redis import *
from controller.postgres import *
# from controller.elasticsearch import *

app = Flask(__name__)

# Routes for main
app.route('/insert_default_values', methods=['POST'])(insert_default_values)
app.route('/delete_all_data', methods=['DELETE'])(delete_all_data)
app.route('/', methods=['GET'])(index)

# Routes for MongoDB - Spotify Playlist
app.route('/get_all_mongo_data', methods=['GET'])(get_all_mongo_data)
app.route('/submit_mongo', methods=['POST'])(submit_mongo)
app.route('/delete_mongo', methods=['DELETE'])(delete_mongo)

# Routes for Postgres - Pokedex
app.route('/update_pokemon_data', methods=['POST'])(update_pokemon_data)
app.route('/get_all_pokemon', methods=['GET'])(get_all_pokemon)
app.route('/add_pokemon', methods=['POST'])(add_pokemon)
app.route('/update_pokemon/<pokemon_id>', methods=['PUT'])(update_pokemon)
app.route('/delete_pokemon/<pokemon_id>', methods=['DELETE'])(delete_pokemon)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)