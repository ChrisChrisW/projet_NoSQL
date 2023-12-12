from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import os
from datetime import datetime

# Configuration Elasticsearch
class ElasticsearchDB:
    # Charge les variables d'environnement
    elasticsearch_host = os.getenv('ELASTICSEARCH_HOST')
    elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
    index = "chat"
    if not elasticsearch_host or not elasticsearch_index:
        raise ValueError("ELASTICSEARCH_HOST or ELASTICSEARCH_INDEX environment variables are not set.")

    def __init__(self):
        self.es = Elasticsearch([self.elasticsearch_host])
        
        # Création de l'index - Vérifier si l'index existe déjà
        if not self.es.indices.exists(index=self.elasticsearch_index):
            # Créer l'index avec une configuration minimale
            self.es.indices.create(index=self.elasticsearch_index)

    def create_message(self, data):
        try:
            username = data['username']
            message_text = data['message']

            # Enregistrez le message dans Elasticsearch avec un horodatage
            self.es.index(index=self.index, body={
                'username': username,
                'message': message_text,
                'timestamp': datetime.now()
            })

            return {'status': 'OK'}

        except Exception as e:
            return {'status': 'Error', 'error_message': str(e)}

    def get_messages(self):
        try:
            # Récupérez les messages depuis Elasticsearch (limité aux 50 derniers)
            result = self.es.search(index=self.index, body={
                'query': {'match_all': {}},
                'size': 50,
                'sort': [{'timestamp': 'desc'}]
            })

            messages = [{'username': hit['_source']['username'],
                        'message': hit['_source']['message'],
                        'timestamp': hit['_source']['timestamp']}
                        for hit in result['hits']['hits']]

            return {'status': 'OK', 'messages': messages}
        except Exception as e:
            return {'status': 'Error', 'error_message': str(e)}
        
    def delete(self, content, timestamp):
        try:
            # Search for the message based on content and timestamp
            result = self.es.search(index=self.index, body={
                'query': {
                    'bool': {
                        'must': [
                            {'match': {'message': content}},
                            {'match': {'timestamp': timestamp}}
                        ]
                    }
                },
                'size': 1  # Assuming unique combination, limit to 1 result
            })

            if result['hits']['hits']:
                message_id = result['hits']['hits'][0]['_id']
                # Perform the deletion in Elasticsearch
                self.es.delete(index='chat', id=message_id)
                return {'status': 'OK'}
            else:
                return {'status': 'Error', 'error_message': 'Message not found'}

        except Exception as e:
            return {'status': 'Error', 'error_message': str(e)}

    def delete_items(self):
        self.es.indices.delete(index=self.elasticsearch_index, ignore=[400, 404])