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
def home(source=None, variant=None, edition=None):
    api_url = configuration.lookup('CONTENT_API_URL')
    num_items = 10
    payload = {
        'api-key':              configuration.lookup('CONTENT_API_KEY'),
        'page-size':            num_items,
        'show-editors-picks':   'true',
        'show-elements':        'image',
        'show-fields':          'all',
        'edition':              edition
    }
    options = {
        'showlinks': False,
        '_copyText': 'We produce hard-hitting, internationally-recognised journalism every day. Here are a sample of stories currently on our US homepage:'
    }

    if source == 'popular':

        if not edition:
            popular_url = 'http://gu-most-popular.appspot.com/api/most-viewed'
        else:
            popular_url = 'http://rrees-experiments.appspot.com/data/most-popular/' + edition + '/' + str(num_items)

        response = requests.get(popular_url)

        # this is annoying: the most popular feed doesn't use a key,
        # but the experimental one uses 'most_popular'
        if not edition:
            data = response.json()
        else:
            data = response.json()['most_popular']

    else:
        response = requests.get(api_url, params=payload)
        data = response.json()['response']['editorsPicks']


    return render_template('index.html', content=data, options=options, variant=variant, edition=edition, source=source)

@crossdomain(origin='*')
def popular(edition='us'):
    num_items = 7
    time_unit = 'hours'
    time_offset = 168 # 1 week
    referrer = 'facebook'
    params = "/".join(str(x) for x in [edition, num_items, time_unit, time_offset, 'referrer', referrer])
    popular_url = 'http://rrees-experiments.appspot.com/data/most-popular/' + params
    response = requests.get(popular_url)
    data = response.json()['most_popular']
    return render_template('popular.html', content=data)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
