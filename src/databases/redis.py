import redis
import os

# Configuration RedisDB
class RedisDB:
    # Redis configuration
    redis_host = os.getenv('REDIS_HOST')
    redis_port = int(os.getenv('REDIS_PORT'))

    if not redis_host or not redis_port:
        raise ValueError("REDIS_HOST or REDIS_PORT environment variables are not set.")

    def __init__(self):
        self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, decode_responses=True)

    def get_items(self):
        try:
            return self.redis_client.hgetall('my_redis_data')
            sorted_redis_data = dict(sorted(redis_data.items(), key=lambda x: int(x[0])))
        except Exception as e:
            print(f"Error during Redis operation: {e}")
            return []
    
    def get_items_sorted(self):
        try:
            redis_data = self.redis_client.hgetall('my_redis_data')
            return dict(sorted(redis_data.items(), key=lambda x: int(x[0])))
        except Exception as e:
            print(f"Error during Redis operation: {e}")
            return []
    
    def get_item_by_id(self, item_id):
        return self.redis_client.hget('my_redis_data', item_id)

    def create_items(self, data):
        try:
            self.redis_client.hmset('my_redis_data', data)
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

    def edit_item(self, item_id, new_field):
        updated_data = {
            item_id : new_field
        }
        self.redis_client.hset('my_redis_data', mapping=updated_data)

    def delete_items(self):
        self.redis_client.flushall()

    def delete_item(self, item_id):
        self.redis_client.hdel('my_redis_data', item_id)
