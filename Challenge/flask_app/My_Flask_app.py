# My_Flask_app.py

from datetime import datetime
from flask import Flask, render_template
import redis
import os
import socket

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_DB = int(os.getenv('REDIS_DB'))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

app = Flask(__name__) 

@app.route('/')
def Welcome():
    return render_template('index.html')

@app.route('/count')
def count():
    visits = r.incr('visits')
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    r.set('last_visit', datetime_now)
    if r.get('first_visit') == None:
            r.set('first_visit', datetime_now)
    
    if visits == 1:
        message = "First visit! Welcome to CountTrak Pro 🎉"
        
    elif visits == 10:
        message = (
            "10 visits! Thanks for being a loyal user! 🙌 "
            "Keep tracking your visits with CountTrak Pro! 🚀"
        )
    elif visits == 50:
        message = (
            "50 visits! You're a power user! 💪 "
            "CountTrak Pro is here to help you track every visit! 📊"
        )
    elif visits == 100:
        message = "100 visits! You're a CountTrak Pro legend! 🏆"
    else:
        message = "Thanks for visiting CountTrak Pro! Keep tracking your visits! 📈"

    hostname = socket.gethostname()
    return render_template('count.html', visit_count=visits, visit_count_message=message, hostname=hostname)

@app.route('/stats')
def stats():
    visit_count = r.get('visits'). decode('utf-8')
    first_visit = r.get('first_visit'). decode('utf-8')
    last_visit = r.get('last_visit'). decode('utf-8')
    return render_template('stats.html', visit_count=visit_count, first_visit=first_visit, last_visit=last_visit)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)