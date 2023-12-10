from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import os

# Configuration Elasticsearch
class ElasticsearchDB:
    # Charge les variables d'environnement
    elasticsearch_host = os.getenv('ELASTICSEARCH_HOST')
    elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
    if not elasticsearch_host or not elasticsearch_index:
        raise ValueError("ELASTICSEARCH_HOST or ELASTICSEARCH_INDEX environment variables are not set.")

    def __init__(self):
        self.es = Elasticsearch([self.elasticsearch_host])
        
        # Création de l'index - Vérifier si l'index existe déjà
        if not self.es.indices.exists(index=self.elasticsearch_index):
            # Créer l'index avec une configuration minimale
            self.es.indices.create(index=self.elasticsearch_index)

    def get_items(self):
        try:
            return self.es.search(index=self.elasticsearch_index, body={'query': {'match_all': {}}})
        except NotFoundError as e:
            print(f"Error during Elasticsearch operation: {e}")
            return []
    
    def get_item_by_id(self, item_id):
        return self.es.get(index=self.elasticsearch_index, id=item_id)

    def create_items(self, data):
        try:
            for item in data:   
                self.es.index(index=self.elasticsearch_index, body=item)
        except NotFoundError as e:
            print(f"Error during Elasticsearch operation: {e}")

    def create_item(self, field1, field2):
        data = {'field1': field1, 'field2': field2}
        self.es.index(index=self.elasticsearch_index, body=data)

    def edit_item(self, item_id, new_field1, new_field2):
        updated_data = {
            'field1': new_field1,
            'field2': new_field2
        }
        self.es.update(index=self.elasticsearch_index, id=item_id, body={'doc': updated_data})

    def delete_items(self):
        self.es.indices.delete(index=self.elasticsearch_index, ignore=[400, 404])

    def delete_item(self, item_id):
        self.es.delete(index=self.elasticsearch_index, id=item_id)
