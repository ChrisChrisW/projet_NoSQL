from flask import render_template, request, redirect, url_for, jsonify
from databases.redis import RedisDB

# Création des instances de bd
redis_db = RedisDB()

def add_memes_from_api():
    try:
        redis_db.add_api_data()
        return jsonify({'success': True, 'message': 'Memes added from Imgflip API.'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': f'Failed to fetch memes from Imgflip API. {str(e)}'})

def get_memes():
    return jsonify(redis_db.get_items())

def add_meme():
    try:
        meme_name = request.form.get('memeName')
        meme_url = request.form.get('memeURL')
        redis_db.create_items(meme_name, meme_url)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': 'Meme not found'})

def edit_meme(meme_id):
    try:
        meme_key = f'meme:{meme_id}'
        meme_name = request.form.get('memeName')
        meme_url = request.form.get('memeURL')
        redis_db.edit_item(meme_key, meme_name, meme_url)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': 'Meme not found'})

def delete_meme(meme_id):
    try:
        meme_key = f'meme:{meme_id}'
        redis_db.delete_item(meme_key)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': 'Meme not found'})

def delete_all_redis():
    redis_db.delete_items()