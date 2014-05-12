from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)
app.add_url_rule('/source/<source>/', 'home', view_func=views.home)
app.add_url_rule('/source/<source>/<edition>/', 'home', view_func=views.home)
app.add_url_rule('/variant/<variant>/', 'home', view_func=views.home)
app.add_url_rule('/variant/<variant>/<edition>/', 'home', view_func=views.home)

# popular
app.add_url_rule('/popular/', 'popular', view_func=views.popular)
app.add_url_rule('/popular/<edition>/', 'popular', view_func=views.popular)

# editor
app.add_url_rule('/edit/', 'edit', view_func=views.edit, methods=['GET', 'POST'])

app.add_url_rule('/message/', 'message', view_func=views.msg)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

