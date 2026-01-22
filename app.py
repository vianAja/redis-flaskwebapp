from flask import Flask, render_template, request, jsonify
import redis
import os
import json
from datetime import datetime

app = Flask(__name__)

# Redis configuration from environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'host.docker.internal')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_USER = os.getenv('REDIS_USER', 'default')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Connect to Redis
try:
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        username=REDIS_USER,
        password=REDIS_PASSWORD,
        db=REDIS_DB,
        decode_responses=True
    )
    r.ping()
    print("Successfully connected to Redis!")
except Exception as e:
    print(f"Error connecting to Redis: {e}")
    r = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    try:
        r.ping()
        return jsonify({'status': 'healthy', 'redis': 'connected'}), 200
    except:
        return jsonify({'status': 'unhealthy', 'redis': 'disconnected'}), 500

@app.route('/set', methods=['POST'])
def set_value():
    try:
        data = request.json
        key = data.get('key')
        value = data.get('value')
        
        if not key or value is None:
            return jsonify({'error': 'Key and value are required'}), 400
        
        r.set(key, value)
        return jsonify({'message': 'Value set successfully', 'key': key, 'value': value}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get/<key>')
def get_value(key):
    try:
        value = r.get(key)
        if value is None:
            return jsonify({'message': 'Key not found', 'key': key}), 404
        return jsonify({'key': key, 'value': value}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<key>', methods=['DELETE'])
def delete_value(key):
    try:
        result = r.delete(key)
        if result == 0:
            return jsonify({'message': 'Key not found', 'key': key}), 404
        return jsonify({'message': 'Key deleted successfully', 'key': key}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/all')
def get_all():
    try:
        keys = r.keys('*')
        data = {}
        for key in keys:
            data[key] = r.get(key)
        return jsonify({'count': len(keys), 'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/counter/increment', methods=['POST'])
def increment_counter():
    try:
        data = request.json
        key = data.get('key', 'counter')
        value = r.incr(key)
        return jsonify({'key': key, 'value': value}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list/push', methods=['POST'])
def push_to_list():
    try:
        data = request.json
        key = data.get('key')
        value = data.get('value')
        
        if not key or value is None:
            return jsonify({'error': 'Key and value are required'}), 400
        
        length = r.rpush(key, value)
        return jsonify({'message': 'Value pushed to list', 'key': key, 'length': length}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list/get/<key>')
def get_list(key):
    try:
        values = r.lrange(key, 0, -1)
        return jsonify({'key': key, 'values': values, 'length': len(values)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)