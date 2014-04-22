from models import Configuration

import logging

def create(key, value):
    config = Configuration(key = key, value = value)
    key = config.put()
    return key

def lookup(key):
    results = Configuration.query(Configuration.key == key)
    if not results.iter().has_next():
        return None

    key_value = results.iter().next().value
    logging.info(key_value)

    return key_value
