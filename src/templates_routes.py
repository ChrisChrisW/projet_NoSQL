from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bson import ObjectId
import redis
from neo4j import GraphDatabase
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import os

app = Flask(__name__)

# MongoDB configuration
mongo_uri = os.getenv('MONGO_DB_URI')
database_name = os.getenv('DATABASE_NAME')
collection_name = os.getenv('COLLECTION_NAME')

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Redis configuration
redis_host = os.getenv('REDIS_HOST')
redis_port = int(os.getenv('REDIS_PORT'))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# PostgreSQL configuration
postgres_uri = os.getenv('POSTGRES_DB_URI')
engine = create_engine(postgres_uri)
Base = declarative_base()

class PostgresItem(Base):
    __tablename__ = 'postgres_items'
    id = Column(Integer, primary_key=True)
    field1 = Column(String(255), nullable=False)
    field2 = Column(String(255), nullable=False)

# Create tables in PostgreSQL
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Neo4j configuration
class Neo4jDB:
    neo4j_uri = os.getenv('NEO4J_URI')
    neo4j_user = os.getenv('NEO4J_USER')
    neo4j_password = os.getenv('NEO4J_PASSWORD')

    def __init__(self):
        self.driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))

    def close(self):
        self.driver.close()

    def create_item(self, field1, field2):
        with self.driver.session() as session:
            session.write_transaction(self._create_item, field1, field2)

    def get_items(self):
        with self.driver.session() as session:
            try:
                return session.read_transaction(self._get_items)
            except Exception as e:
                print(f"Error retrieving Neo4j data: {e}")
                return []
            
    def get_item_by_id(self, item_id):
        with self.driver.session() as session:
            return session.read_transaction(self._get_item_by_id, item_id)

    def edit_item(self, item_id, new_field1, new_field2):
        with self.driver.session() as session:
            session.write_transaction(self._edit_item, item_id, new_field1, new_field2)

    def delete_item(self, item_id):
        with self.driver.session() as session:
            session.write_transaction(self._delete_item, item_id)

    def delete_items(self):
        with self.driver.session() as session:
            try:
                return session.write_transaction(self._delete_items)
            except Exception as e:
                print(f"Error deleting Neo4j data: {e}")
                return []
            
    def _create_item(self, tx, field1, field2):
        tx.run("CREATE (item:Item {field1: $field1, field2: $field2})", field1=field1, field2=field2)

    def _get_items(self, tx):
        result = tx.run("MATCH (item:Item) RETURN ID(item) AS id, item.field1 AS field1, item.field2 AS field2")
        return [record for record in result]

    def _get_item_by_id(self, tx, item_id):
        result = tx.run(f"MATCH (item:Item) WHERE ID(item) = {item_id} RETURN ID(item) AS id, item.field1 AS field1, item.field2 AS field2")
        return result.single()
            
    def _edit_item(self, tx, item_id, new_field1, new_field2):
        tx.run(f"MATCH (item:Item) WHERE ID(item) = {item_id} SET item.field1 = '{new_field1}', item.field2 = '{new_field2}'")
    
    def _delete_item(self, tx, item_id):
        tx.run(f"MATCH (item:Item) WHERE ID(item) = {item_id} DELETE item")
    
    def _delete_items(self, tx):
        tx.run(f"MATCH (item:Item) DETACH DELETE item")

neo4j_db = Neo4jDB()


# Charge les variables d'environnement
elasticsearch_host = os.getenv('ELASTICSEARCH_HOST')
elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')

# Configuration Elasticsearch
es = Elasticsearch([elasticsearch_host])

def create_elasticsearch_index():
    # Vérifier si l'index existe déjà
    if not es.indices.exists(index=elasticsearch_index):
        # Créer l'index avec une configuration minimale
        es.indices.create(index=elasticsearch_index)

# Appeler la fonction pour créer l'index au démarrage de l'application Flask
create_elasticsearch_index()

@app.route('/insert_default_values', methods=['POST'])
def insert_default_values():
    # Exemple 1: Insérer des valeurs dans MongoDB
    default_mongo_data = [
        {'field1': 'John Doe', 'field2': 'Software Engineer'},
        {'field1': 'Jane Smith', 'field2': 'Data Scientist'},
        {'field1': 'Bob Johnson', 'field2': 'Product Manager'},
        {'field1': 'Electronics', 'field2': 19.99},
        {'field1': 'Clothing', 'field2': 29.99},
        {'field1': 'Books', 'field2': 9.99},
    ]
    collection.insert_many(default_mongo_data)

    # Exemple 2: Insérer des valeurs dans Redis
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
    redis_client.hmset('my_redis_data', default_redis_data)

    # Example 3: Insert data into PostgreSQL
    complex_postgres_data = [
        {'field1': 'Computer', 'field2': 'Intel Core i7'},
        {'field1': 'Monitor', 'field2': '27-inch 4K'},
        {'field1': 'Keyboard', 'field2': 'Mechanical'},
        {'field1': 'Monitor', 'field2': '32-inch 4K'},
        {'field1': 'Mouse', 'field2': 'Wireless'},
        {'field1': 'Printer', 'field2': 'Color LaserJet'},
    ]
    for data in complex_postgres_data:
        postgres_item = PostgresItem(**data)
        session.add(postgres_item)
    session.commit()

    # Example 4: Insert data into Neo4j
    neo4j_db.create_item('Product1', 'A great product with amazing features.')
    neo4j_db.create_item('Product2', 'An innovative solution for your needs.')
    neo4j_db.create_item('Product3', 'High-quality and reliable product for professionals.')

    # Example 5: Insert data into Elasticsearch
    default_elasticsearch_data = [
        {'field1': 'ProductA', 'field2': 'High-performance gadget for tech enthusiasts.'},
        {'field1': 'ProductB', 'field2': 'Fashionable accessory with cutting-edge design.'},
        {'field1': 'ProductC', 'field2': 'Innovative solution for everyday convenience.'},
    ]

    for data in default_elasticsearch_data:
        es.index(index=elasticsearch_index, body=data)

    return redirect(url_for('index'))

@app.route('/delete_all_data', methods=['DELETE'])
def delete_all_data():
    # Supprimer toutes les données de la collection MongoDB
    collection.drop()

    # Supprimer toutes les données de toutes les bases de données Redis
    redis_client.flushall()

    # Delete all data from PostgreSQL
    session.query(PostgresItem).delete()
    session.commit()

    # TODO : delete for neo4j
    neo4j_db.delete_items()

    # Supprimer toutes les données de toutes les données de Elasticsearch
    es.indices.delete(index=elasticsearch_index, ignore=[400, 404])

    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    # Get data from MongoDB
    mongo_data = collection.find()

    # Get data from Redis
    redis_data = redis_client.hgetall('my_redis_data')
    sorted_redis_data = dict(sorted(redis_data.items(), key=lambda x: int(x[0])))

    # Get data from PostgreSQL
    postgres_data = session.query(PostgresItem).all()

    # Get data from Neo4j
    neo4j_data = neo4j_db.get_items()

    # Get data from Elasticsearch
    try:
        es_data = es.search(index='my_index', body={'query': {'match_all': {}}})
    except NotFoundError:
        es_data = None  

    return render_template('index.html', mongo_data=mongo_data, redis_data=sorted_redis_data, postgres_data=postgres_data, neo4j_data=neo4j_data, es_data=es_data)

@app.route('/submit_mongo', methods=['POST'])
def submit_mongo():
    # Handle MongoDB form submission
    data = {
        'field1': request.form['field1'],
        'field2': request.form['field2']
        # Add other fields as needed
    }

    # Save data to MongoDB
    collection.insert_one(data)

    return redirect(url_for('index'))

@app.route('/submit_redis', methods=['POST'])
def submit_redis():
    # Retrieve existing data from Redis
    redis_data = redis_client.hgetall('my_redis_data')
    existing_fields = set(redis_data.keys())

    data = {}
    start = 0
    # Iterate through the form data
    for i in range(len(request.form) - 1):
        # Find the next available key not present in existing_fields
        while f'{start}' in existing_fields:
            start += 1

        # Add the new data to the dictionary
        data[f'{start}'] = request.form.get(f'{i}')
        
        # Update existing_fields with the new key
        existing_fields.add(f'{start}')

    redis_client.hmset('my_redis_data', data)      


    return redirect(url_for('index'))

@app.route('/submit_postgres', methods=['POST'])
def submit_postgres():
    data = {
        'field1': request.form['field1'],
        'field2': request.form['field2']
    }

    # Save data to PostgreSQL
    postgres_item = PostgresItem(**data)
    session.add(postgres_item)
    session.commit()

    return redirect(url_for('index'))

@app.route('/submit_neo4j', methods=['POST'])
def submit_neo4j():
    field1 = request.form['field1']
    field2 = request.form['field2']

    # Use the Neo4jDB instance to create an item
    neo4j_db.create_item(field1, field2)

    return redirect(url_for('index'))

@app.route('/submit_elasticsearch', methods=['GET', 'POST'])
def submit_elasticsearch():
    field1 = request.form['field1']
    field2 = request.form['field2']

    es.index(index=elasticsearch_index, body={
        'field1': field1,
        'field2': field2
    })

    return redirect(url_for('index'))

@app.route('/edit_mongo/<item_id>', methods=['GET', 'POST'])
def edit_mongo(item_id):
    # Récupérer l'élément à modifier
    item = collection.find_one({'_id': ObjectId(item_id)})

    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
              # Mettez à jour les données avec les nouvelles valeurs
            updated_data = {
                'field1': request.form['field1'],
                'field2': request.form['field2']
                # Ajoutez d'autres champs selon votre formulaire
            }
            collection.update_one({'_id': ObjectId(item_id)}, {'$set': updated_data})
            
            # Redirigez vers la page d'accueil après la modification
            return redirect(url_for('index'))

    return render_template('mongoDB/edit.html', item=item) 

@app.route('/edit_redis/<item_id>', methods=['GET', 'POST'])
def edit_redis(item_id):
    # Find the item in Redis using the provided key
    item = redis_client.hget('my_redis_data', item_id)

    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            updated_data = {
                item_id : request.form['field']
            }
            # Update data in Redis
            redis_client.hset('my_redis_data', mapping=updated_data)

            # Redirigez vers la page d'accueil après la modification
            return redirect(url_for('index'))

    return render_template('redis/edit.html', field=item_id, item=item)

@app.route('/edit_postgres/<item_id>', methods=['GET', 'POST'])
def edit_postgres(item_id):
    item = session.query(PostgresItem).filter_by(id=item_id).first()

    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            # Update data in PostgreSQL
            item.field1 = request.form['field1']
            item.field2 = request.form['field2']
            session.commit()

            return redirect(url_for('index'))

    return render_template('postgres/edit.html', item=item)

@app.route('/edit_neo4j/<item_id>', methods=['GET', 'POST'])
def edit_neo4j(item_id):
    item = neo4j_db.get_item_by_id(item_id)

    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            new_field1 = request.form['field1']
            new_field2 = request.form['field2']
            neo4j_db.edit_item(item_id, new_field1, new_field2)
            return redirect(url_for('index'))

    return render_template('neo4j/edit.html', item=item)

@app.route('/edit_elasticsearch/<item_id>', methods=['GET', 'POST'])
def edit_elasticsearch(item_id):
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            updated_data = {
                'field1': request.form['field1'],
                'field2': request.form['field2']
            }

            es.update(index=elasticsearch_index, 
                      id=item_id, 
                      body={
                          'doc': updated_data
                          })

            return redirect(url_for('index'))

    es_data = es.get(index=elasticsearch_index, id=item_id)

    return render_template('elasticsearch/edit.html', es_data=es_data)

@app.route('/delete_mongo/<item_id>', methods=['DELETE', 'POST'])
def delete_mongo(item_id):
    if request.form.get('_method') == 'DELETE':
        # Delete item from MongoDB
        collection.delete_one({'_id': ObjectId(item_id)})

    # Redirect to the index page after deletion
    return redirect(url_for('index'))

@app.route('/delete_redis/<item_id>', methods=['DELETE', 'POST'])
def delete_redis(item_id):
    if request.form.get('_method') == 'DELETE':
        # Delete item from Redis
        redis_client.hdel('my_redis_data', item_id)

    # Redirect to the index page after deletion
    return redirect(url_for('index'))

@app.route('/delete_postgres/<item_id>', methods=['DELETE', 'POST'])
def delete_postgres(item_id):
    if request.form.get('_method') == 'DELETE':
        item = session.query(PostgresItem).filter_by(id=item_id).first()

        if 'delete_postgres' in request.form:
            # Delete item from PostgreSQL
            session.delete(item)
            session.commit()

    return redirect(url_for('index'))

@app.route('/delete_neo4j/<item_id>', methods=['POST'])
def delete_neo4j(item_id):
    if request.form.get('_method') == 'DELETE':
        if 'delete_neo4j' in request.form:
            neo4j_db.delete_item(item_id)

    return redirect(url_for('index'))

@app.route('/delete_elasticsearch/<item_id>', methods=['POST'])
def delete_elasticsearch(item_id):
    if request.form.get('_method') == 'DELETE':
        es.delete(index=elasticsearch_index, id=item_id)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)