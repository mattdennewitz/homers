from flask import render_template, request

from homers import app, db


@app.route('/')
def index():
    """Displays list of homers"""

    return render_template('index.html')


@app.route('/api/v1/homers')
def api_v1_homers():
    """Returns a JSON list of homers for a date"""

    
