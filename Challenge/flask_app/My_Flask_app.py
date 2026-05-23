# My_Flask_app.py

from flask import Flask
import redis
import os

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_DB = int(os.getenv('REDIS_DB'))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

app = Flask(__name__) 

@app.route('/')
def Welcome():
    return 'Welcome to My Flask App!'

@app.route('/count')
def count():
    visits = r.incr('visits')
    return f'This page has been visited {visits} times.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)