from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect
import requests
from flask_cache import Cache

from application import app
from decorators import login_required, admin_required, crossdomain
import configuration

cache = Cache(app)
@crossdomain(origin='*')
def home(source=None):
    api_url = configuration.lookup('CONTENT_API_URL')
    num_items = 3
    payload = {
        'api-key':              configuration.lookup('CONTENT_API_KEY'),
        'page-size':            num_items,
        'show-editors-picks':   'true',
        'show-elements':        'image',
        'show-fields':          'all',
        'edition':              'US'
    }
    options = {
        'showlinks': False,
        '_copyText': 'We produce hard-hitting, internationally-recognised journalism every day. Here are a sample of stories currently on our US homepage:'
    }

    if not source:
        response = requests.get(api_url, params=payload)
        data = response.json()['response']['editorsPicks']
    elif source == 'popular':
        response = requests.get('http://rrees-experiments.appspot.com/data/most-popular/us/' + str(num_items))
        data = response.json()['most_popular']

    return render_template('index.html', content=data, options=options)

def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
