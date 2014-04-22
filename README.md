mandrews-experiments
====================

A space for quick hacks and ideas.

This Flask app is built using @kamalgill's https://github.com/kamalgill/flask-appengine-template and uses @rrees' smart https://github.com/guardian/simply-py to manage private config data:

## Creating configuration data

You can use the Configuration model to store private details such as API keys.

To do this you also need to enable the remote shell feature by adding the following to your app.yaml:
````
    builtins:
    - remote_api: on````

You can then [connect to your local shell](http://localhost:8000/console) or [connect to the remote one](https://developers.google.com/appengine/articles/remote_api) and create the first piece of config:
````
    from models import Configuration
    config = Configuration(id="<your lookup key>", key="<your lookup key>", value="<your value>")
    config.put()````

Once this value has been created you can then create other configuration via the [Data Viewer](http://localhost:8000/datastore?kind=Configuration).