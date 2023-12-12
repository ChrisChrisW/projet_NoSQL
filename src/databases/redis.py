import redis
import os
import requests

# Configuration RedisDB
class RedisDB:
    # Redis configuration
    redis_host = os.getenv('REDIS_HOST')
    redis_port = int(os.getenv('REDIS_PORT'))

    if not redis_host or not redis_port:
        raise ValueError("REDIS_HOST or REDIS_PORT environment variables are not set.")

    def __init__(self):
        self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, decode_responses=True)

    def add_api_data(self):
        imgflip_api_url = 'https://api.imgflip.com/get_memes'
        response = requests.get(imgflip_api_url)
        data = response.json()

        if data['success']:
            memes = data['data']['memes']
            for meme in memes:
                meme_id = self.redis_client.incr('meme_id')
                meme_key = f'meme:{meme_id}'
                self.redis_client.hset(meme_key, 'name', meme['name'])
                self.redis_client.hset(meme_key, 'url', meme['url'])

    def get_items(self):
        try:
            meme_keys = self.redis_client.keys('meme:*')
            memes = []

            for key in meme_keys:
                meme = self.redis_client.hgetall(key)
                memes.append({'id': key.split(':')[-1], 'name': meme['name'], 'url': meme['url']})

            return memes
        except Exception as e:
            print(f"Error during Redis operation: {e}")
            return []

    def create_items(self, meme_name, meme_url):
        try:
            if meme_name and meme_url:
                meme_id = self.redis_client.incr('meme_id')
                meme_key = f'meme:{meme_id}'

                self.redis_client.hset(meme_key, 'name', meme_name)
                self.redis_client.hset(meme_key, 'url', meme_url)

                return {'success': True, 'meme_id': meme_id}
            else:
                return {'success': False, 'error': 'Missing data'}
        except Exception as e:
            print(f"Error creating Redis data: {e}")

    def create_item(self, items):
        # Retrieve existing data from Redis
        redis_data = self.redis_client.hgetall('my_redis_data')
        existing_fields = set(redis_data.keys())

        data = {}
        start = 0
        # Iterate through the form data
        for i in range(len(items) - 1):
            # Find the next available key not present in existing_fields
            while f'{start}' in existing_fields:
                start += 1

            # Add the new data to the dictionary
            data[f'{start}'] = items.get(f'{i}')
            
            # Update existing_fields with the new key
            existing_fields.add(f'{start}')

        self.redis_client.hmset('my_redis_data', data) 

    def edit_item(self, meme_key, meme_name, meme_url):
        if self.redis_client.exists(meme_key):
            self.redis_client.hset(meme_key, 'name', meme_name)
            self.redis_client.hset(meme_key, 'url', meme_url)

    def delete_items(self):
        self.redis_client.flushall()

    def delete_item(self, meme_key):
        if self.redis_client.exists(meme_key):
            self.redis_client.delete(meme_key)
