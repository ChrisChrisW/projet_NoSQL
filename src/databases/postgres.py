from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

import requests

# Configuration PostgresDB
class PostgresDB:
    # PostgreSQL configuration
    postgres_uri = os.getenv('POSTGRES_DB_URI')
    if not postgres_uri:
        raise ValueError("POSTGRES_DB_URI environment variable is not set.")
    engine = create_engine(postgres_uri)
    Base = declarative_base()

    def __init__(self):
        self.setup_database()

    def setup_database(self):
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    class Pokemon(Base):
        __tablename__ = 'pokemon_items'
        id = Column(Integer, primary_key=True)
        name = Column(String(50), unique=True, nullable=False)
        type_1 = Column(String(20), nullable=False)
        type_2 = Column(String(20))
        description = Column(String(500))
        image_url = Column(String(500))

    
    # Flask route to fetch data from the API and store it in the database
    def update_pokemon_data(self):
        api_url = 'https://pokeapi.co/api/v2/pokemon?limit=151'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            items = []
            for entry in data['results']:
                pokemon_data = requests.get(entry['url']).json()
                species_data = requests.get(pokemon_data['species']['url']).json()

                # Extract relevant data
                name = pokemon_data['name']
                type_1 = pokemon_data['types'][0]['type']['name']
                type_2 = pokemon_data['types'][1]['type']['name'] if len(pokemon_data['types']) > 1 else None
                flavor_text_entry = next((entry['flavor_text'] for entry in species_data['flavor_text_entries'] if entry['language']['name'] == 'en'), None)
                image_url = pokemon_data['sprites']['front_default']
                
                # Clean up flavor text
                if flavor_text_entry:
                    flavor_text_entry = ' '.join(flavor_text_entry.split())  # Remove excessive whitespace and line breaks

                item = {
                    "name": name,
                    "type_1": type_1,
                    "type_2": type_2,
                    "description": flavor_text_entry,
                    "image_url": image_url
                }
                items.append(item)

            try:  
                for item in items:   
                    pokemon_item = self.Pokemon(**item)
                    self.session.add(pokemon_item)
                self.session.commit()
                return 'Data updated successfully'
            except Exception as e:
                self.session.rollback()
                print(f"Error committing changes: {e}")

        return 'Failed to fetch data from the API'
    
    def find_all(self):
        try:
            # Retrieving all data from MongoDB collection
            pokemons = self.session.query(self.Pokemon).order_by("id").all()
            # Convert each Pokemon instance to a dictionary
            pokemon_data = [
                {
                    "id": pokemon.id,
                    "name": pokemon.name,
                    "type_1": pokemon.type_1,
                    "type_2": pokemon.type_2,
                    "description": pokemon.description,
                    "image_url": pokemon.image_url,
                }
                for pokemon in pokemons
            ]

            return pokemon_data
        except Exception as e:
            print(f"Error during database operation: {e}")
            return []
    
    def add_data(self, item):
        pokemon_data = {
            "id": item.get("id"),
            "name": item.get("name"),
            "type_1": item.get("type1"),
            "type_2": item.get("type2"),
            "description": item.get("description"),
            "image_url": item.get("imageUrl"),
        }

        try:  
            new_pokemon = self.Pokemon(**pokemon_data)
            self.session.add(new_pokemon)
            self.session.commit()
            return 'Data updated successfully'
        except Exception as e:
            self.session.rollback()
            print(f"Error committing changes: {e}")

    def update_data(self, pokemon_id, data):
        item = self.session.query(self.Pokemon).get(pokemon_id)
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.type_1 = data.get('type1', item.type_1)
        item.type_2 = data.get('type2', item.type_2)
        item.image_url = data.get('image_url', item.image_url)

        self.session.commit()

    def delete(self, pokemon_id):
        item = self.session.query(self.Pokemon).get(pokemon_id)
        self.session.delete(item)
        self.session.commit()