from flask import Flask, render_template
from flask_pymongo import PyMongo
import json
import requests
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://admin:123@mongo:27017/covid_ontario'
mongo = PyMongo(app)


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = datetime.fromtimestamp(date)
    native = date.replace(tzinfo=None)
    format = '%Y-%m-%d'
    return native.strftime(format)


@app.route('/')
def index():
    status = mongo.db.status
    status_data = []
    for s in status.find().sort("date"):
        status_data.append({
            'date': _jinja2_filter_datetime(int(s.get('date'))),
            'deceased': s.get('deceased', 0),
            'confirmed': s.get('confirmed', 0),
            'resolved': s.get('resolved', 0),
            'pending': s.get('pending', 0),
            'total': s.get('total', 0)
        })

    return render_template('home.html', ontario_data=status_data)


@app.route('/bar-chart')
def bar_chart():
    return render_template('barchart.html')


@app.route('/fetch')
def fetch():
    params = {
        'spider_name': 'ontario',
        'start_requests': True
    }
    response = requests.get('http://scrapy:9080/crawl.json', params)
    fetch_result = json.loads(response.text)
    return render_template('fetch.html', content=fetch_result)
